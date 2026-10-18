import pygame
import sys

from scripts.utils import (
    draw_rect, organise_poses, add_lists, multiply_lists, scroll_control,
    WIDGET_FIELDS, save_widget_config, load_widget_config, fill_dummy_data,
)
from scripts.widgets import TitleBar, Dummy, text_input, text_input2
from scripts.registry import resolve
import scripts.widgets  # noqa: F401
import scripts.types    # noqa: F401


WINDOWSIZE = [640, 480]


# ============================================================
# widget building — every preset the dummy carries flows in
# ============================================================

def _default_colors(entry):
    c = entry.get("colors")
    if c:
        return list(c)
    return ["blue", "aqua"]


def _construct_widget(entry, font):
    t = entry["type"]
    size = list(entry.get("size", [16, 16]))
    colors = _default_colors(entry)
    cls = resolve(f"widget.{t}")

    if t in ("Label", "TextBox"):
        return cls(entry.get("text", "..."), [0, 0], font, colors)
    if t in ("Button", "RectedButton"):
        return cls([0, 0], entry.get("color", "aqua"), size)
    if t == "Button2":
        return cls(font, [0, 0], text=entry.get("txt", "..."))
    if t in ("Slider", "VerticalSlider"):
        rng = entry.get("range", [entry.get("range_min", 0),
                                   entry.get("range_max", 100)])
        return cls(rng, [0, 0], size=size)
    if t == "Table":
        return cls(font, [0, 0], entry.get("columns", 3), entry.get("rows", 3))
    if t == "Custom_Table":
        return cls(font, [0, 0], size,
                   entry.get("columns", 3), entry.get("rows", 3))
    if t == "Dialog":
        return cls(font, entry.get("text", "..."), [0, 0], size, colors,
                   rate=entry.get("rate", 2))
    if t == "TitleBar":
        w = cls(font, pygame.Surface(size), entry.get("text", "Title"))
        w.pos = [0, 0]
        w.size = size
        return w
    if t == "Checkbox":
        return cls([0, 0], entry.get("label", "..."),
                   entry.get("checked", False), size, colors, font)
    if t == "ProgressBar":
        return cls([0, 0], size,
                   entry.get("value", 50), entry.get("max_value", 100), colors)
    if t == "ToggleSwitch":
        return cls([0, 0], size, entry.get("state", False), colors)
    if t == "ImageWidget":
        return cls([0, 0], entry.get("image_path", ""), size)
    if t == "Panel":
        return cls([0, 0], size, entry.get("color", "blue"),
                   entry.get("border_color", None), entry.get("border", 0))
    if t == "Dropdown":
        opts = entry.get("options")
        if isinstance(opts, str):
            opts = [o.strip() for o in opts.split(",") if o.strip()]
        if not opts:
            opts = ["...", "..."]
        return cls([0, 0], opts, entry.get("selected", 0), size, colors, font)
    return cls()


def _resize_table(w, pos, size):
    """Force a Table / Custom_Table to sit at pos/size with visible cells.
    Builds its own surface so font-driven sizing doesn't fight the dummy."""
    cols = max(1, int(w.columns))
    rows = max(1, int(w.rows))
    cell_w = max(1, size[0] // cols)
    cell_h = max(1, size[1] // rows)

    w.text_items = dict(getattr(w, "text_items", {}))
    for c in range(cols):
        for r in range(rows):
            key = f"{c};{r}"
            v = w.text_items.get(key)
            if v in (None, ""):
                w.text_items[key] = "..."
    w.items = {k: w.font.render(v, False, w.font_color)
               for k, v in w.text_items.items()}

    surf = pygame.Surface(size)
    surf.fill(w.color)
    # faint cell borders so the grid is visible even if text is small
    for c in range(cols + 1):
        pygame.draw.line(surf, "aqua",
                         [c * cell_w, 0], [c * cell_w, size[1]], 1)
    for r in range(rows + 1):
        pygame.draw.line(surf, "aqua",
                         [0, r * cell_h], [size[0], r * cell_h], 1)
    for c in range(cols):
        for r in range(rows):
            cell_surf = w.items.get(f"{c};{r}")
            if cell_surf is not None:
                surf.blit(cell_surf, [c * cell_w + 3, r * cell_h + 3])

    w.surface = surf
    w.pos = list(pos)
    w.size = list(size)
    w.draw_onto_surf = lambda: None
    w.get_rect = lambda p=list(pos), s=list(size): pygame.Rect(p[0], p[1], s[0], s[1])


def _apply_geometry(w, entry):
    """Force the widget to sit exactly where the dummy was drawn, at
    the exact size the user drew. Resizes any internal surfaces too."""
    t = type(w).__name__
    pos = list(entry.get("pos", [0, 0]))
    size = list(entry.get("size", [16, 16]))

    if t in ("Table", "Custom_Table"):
        _resize_table(w, pos, size)
        return
    if t == "Panel":
        w.pos, w.size = pos, size
        return
    if t == "ProgressBar":
        w.pos, w.size = pos, size
        return
    if t == "ToggleSwitch":
        w.pos, w.size = pos, size
        return
    if t == "Dropdown":
        w.pos, w.size = pos, size
        return
    if t == "Checkbox":
        w.pos, w.size = pos, size
        w.surf = pygame.Surface(size)
        w.surf.set_colorkey("black")
        return
    if t == "Dialog":
        w.pos, w.size = pos, size
        w.now_size = [5, size[1]]
        return
    if t == "ImageWidget":
        w.pos, w.size = pos, size
        if w.image and w.scale:
            w.image = pygame.transform.scale(w.image, size)
        return
    if t in ("Button", "RectedButton"):
        w.pos, w.size = pos, size
        w.surf = pygame.Surface(size)
        w.icon = pygame.Surface(size)
        w.set_color(w.color)
        return
    if t == "Slider":
        w.pos, w.size = pos, size
        w.img = pygame.Surface(size)
        w.fg_size = [8, size[1]]
        w.fg_img = pygame.Surface(w.fg_size)
        w.set_colors([w.bkg_color, w.fg_color])
        return
    if t == "VerticalSlider":
        w.pos, w.size = pos, size
        w.img = pygame.Surface(size)
        w.fg_size = [size[1], 8]
        w.fg_img = pygame.Surface(w.fg_size)
        w.set_colors([w.bkg_color, w.fg_color])
        return
    if t == "TitleBar":
        w.pos, w.size = pos, size
        w.surf = pygame.Surface(size)
        w.set_color([w.surf_color, w.text_color])
        return
    if t in ("Label", "TextBox", "Button2"):
        if hasattr(w, "pos"):
            w.pos = pos
        return
    try:
        w.pos = pos
    except Exception:
        pass
    try:
        w.size = size
    except Exception:
        pass


def build_widget_from_entry(entry, font):
    t = entry.get("type", "")
    if not t or t == "widget":
        return None
    entry = fill_dummy_data(entry)
    try:
        w = _construct_widget(entry, font)
    except Exception as e:
        print(f"[menuEditor] build failed for {t}: {e}")
        return None
    if hasattr(w, "deserialize"):
        try:
            w.deserialize(entry)
        except Exception as e:
            print(f"[menuEditor] deserialize failed for {t}: {e}")
    _apply_geometry(w, entry)
    w.id = entry.get("id", None)
    return w


def build_widgets_from_entries(entries, font):
    out = []
    for e in entries:
        w = build_widget_from_entry(e, font)
        if w is not None:
            out.append(w)
    return out


# ============================================================
# type-aware preview drawing
# ============================================================

def _draw_widget_live(widget, surf, offset=[0, 0]):
    t = type(widget).__name__

    if t == "TitleBar":
        surf.blit(widget.surf, [widget.pos[0] - offset[0],
                                widget.pos[1] - offset[1]])
        return
    if t in ("Slider", "VerticalSlider"):
        widget.update3(surf, offset)
        return
    if t == "Button2":
        widget.rected()
        widget.draw(surf, offset)
        return
    if t in ("Button", "RectedButton", "Dummy"):
        widget.draw(surf, offset)
        return
    if t in ("Table", "Custom_Table"):
        rect = widget.get_rect()
        surf.blit(widget.surface, [rect.x - offset[0], rect.y - offset[1]])
        return
    if t == "Dialog":
        if widget.active:
            widget.update(surf, offset)
        else:
            widget.draw(surf, offset)
        return
    if hasattr(widget, "draw"):
        try:
            widget.draw(surf, offset)
            return
        except TypeError:
            try:
                widget.draw(surf)
                return
            except TypeError:
                pass
    if hasattr(widget, "update"):
        try:
            widget.update(surf, offset)
            return
        except TypeError:
            try:
                widget.update()
                return
            except TypeError:
                pass


# ============================================================
# toolbar button
# ============================================================

class UIBtn:
    def __init__(self, text, pos, size, font, bkg="blue", fg="aqua"):
        self.text = text
        self.pos = list(pos)
        self.size = list(size)
        self.font = font
        self.bkg = bkg
        self.fg = fg
        self.hot = False
        self.surf = pygame.Surface(size)

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def update_hover(self, mouse_screen, scale):
        mx, my = mouse_screen[0] // scale, mouse_screen[1] // scale
        self.hot = self.rect().collidepoint(mx, my)

    def was_clicked(self, event, scale):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos[0] // scale, event.pos[1] // scale
            return self.rect().collidepoint(mx, my)
        return False

    def draw(self, surf):
        bkg = "aqua" if self.hot else self.bkg
        fg = "black" if self.hot else self.fg
        self.surf.fill(bkg)
        txt = self.font.render(self.text, False, fg)
        self.surf.blit(txt, [(self.size[0] - txt.get_width()) // 2,
                             (self.size[1] - txt.get_height()) // 2])
        surf.blit(self.surf, self.pos)


WIDGET_TYPES = [
    "Label", "TextBox", "Button", "RectedButton", "Button2",
    "Slider", "VerticalSlider", "Table", "Custom_Table",
    "Dialog", "Checkbox", "ProgressBar", "ToggleSwitch",
    "ImageWidget", "Panel", "Dropdown",
]


class MenuEditor:
    def __init__(self, scale=2):
        pygame.init()
        self.renderscale = scale
        pygame.display.set_caption("Menu Editor")
        self.screen = pygame.display.set_mode(WINDOWSIZE)
        self.display = pygame.Surface(
            [int(self.screen.get_width() // self.renderscale),
             int(self.screen.get_height() // self.renderscale)])
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("data/fonts/at01.ttf")
        self.bkg_color = (0, 10, 30)

        self.menus = []
        self.tiled = True
        self.tilesize = 16
        self.theresActive = False
        self.grid = True

        self.stage = "draw"
        self.status = "Right-click twice to place a new widget box."
        self.selected = 0
        self._list_start = 0
        self.ui_visible = True

        self._build_toolbar()
        self._build_palette()

    # ---------- UI construction ----------
    def _build_toolbar(self):
        f = self.font
        W = self.display.get_width()
        y = 2
        h = 14
        self.tab_draw    = UIBtn("Draw",    [2, y],   [36, h], f)
        self.tab_assign  = UIBtn("Assign",  [40, y],  [44, h], f)
        self.tab_preview = UIBtn("Preview", [86, y],  [50, h], f)
        self.btn_grid    = UIBtn("Grid",    [W - 190, y], [36, h], f)
        self.btn_tiled   = UIBtn("Tiled",   [W - 152, y], [36, h], f)
        self.btn_ui      = UIBtn("Hide UI", [W - 114, y], [52, h], f)
        self.btn_save    = UIBtn("Save",    [W - 60, y],  [28, h], f)
        self.btn_load    = UIBtn("Load",    [W - 30, y],  [28, h], f)

    def _build_palette(self):
        self.palette = []
        for i, t in enumerate(WIDGET_TYPES):
            col = i % 4
            row = i // 4
            bx = 106 + col * 52
            by = 24 + row * 16
            self.palette.append((t, UIBtn(t, [bx, by], [50, 14], self.font)))

    def toolbar_buttons(self):
        return [self.tab_draw, self.tab_assign, self.tab_preview,
                self.btn_grid, self.btn_tiled, self.btn_ui,
                self.btn_save, self.btn_load]

    def draw_toolbar(self):
        if not self.ui_visible:
            return
        W = self.display.get_width()
        pygame.draw.rect(self.display, "black", [0, 0, W, 18])
        pygame.draw.line(self.display, "aqua", [0, 18], [W, 18])
        for b in self.toolbar_buttons():
            b.draw(self.display)
        active = {"draw": self.tab_draw, "assign": self.tab_assign,
                  "preview": self.tab_preview}.get(self.stage)
        if active:
            pygame.draw.rect(self.display, "yellow", active.rect(), 2)
        if self.grid:
            pygame.draw.rect(self.display, "yellow", self.btn_grid.rect(), 1)
        if self.tiled:
            pygame.draw.rect(self.display, "yellow", self.btn_tiled.rect(), 1)

    def draw_status(self):
        if not self.ui_visible:
            return
        W = self.display.get_width()
        H = self.display.get_height()
        bar_h = 30
        pygame.draw.rect(self.display, "black", [0, H - bar_h, W, bar_h])
        pygame.draw.line(self.display, "yellow", [0, H - bar_h], [W, H - bar_h])
        pygame.draw.line(self.display, "yellow", [0, H - 1], [W, H - 1])
        self.display.blit(self.font.render(self.status[:70], False, "yellow"),
                          [6, H - bar_h + 3])
        hint = "F1 / TAB: hide UI   |   ESC on Draw: quit   |   S: next stage"
        self.display.blit(self.font.render(hint, False, "aqua"),
                          [6, H - 13])

    def draw_ui_indicator(self):
        if self.ui_visible:
            return
        self.display.blit(
            self.font.render("[UI: OFF]  F1/TAB to show", False, "pink"),
            [2, 1])

    def draw_grid_overlay(self):
        if not self.grid:
            return
        tile = self.tilesize
        W, H = self.display.get_size()
        color = (0, 80, 0)
        for x in range(0, W + 1, tile):
            pygame.draw.line(self.display, color, [x, 0], [x, H])
        for y in range(0, H + 1, tile):
            pygame.draw.line(self.display, color, [0, y], [W, y])

    def toggle_ui(self):
        self.ui_visible = not self.ui_visible
        self.status = f"UI {'shown' if self.ui_visible else 'hidden'} (F1/TAB to toggle)"

    def handle_toolbar_click(self, event):
        if not self.ui_visible:
            return False
        for b in self.toolbar_buttons():
            if b.was_clicked(event, self.renderscale):
                if b is self.tab_draw:
                    self.stage = "draw"
                    self.status = "Right-click twice to place a new widget box."
                elif b is self.tab_assign:
                    self.stage = "assign"
                    self.status = "Click a dummy on the left, then pick a widget type."
                elif b is self.tab_preview:
                    self.stage = "preview"
                elif b is self.btn_save:
                    self._do_save()
                elif b is self.btn_load:
                    self._do_load()
                elif b is self.btn_grid:
                    self.grid = not self.grid
                    self.status = f"Grid: {'ON' if self.grid else 'OFF'}"
                elif b is self.btn_tiled:
                    self.tiled = not self.tiled
                    self.status = f"Tiled snap: {'ON' if self.tiled else 'OFF'}"
                elif b is self.btn_ui:
                    self.toggle_ui()
                return True
        return False

    def _do_save(self):
        name = text_input2([self.display, self.screen], self.font, "", "Config Name")
        if not name:
            return
        entries = [d.serialize() for d in self.menus]
        save_widget_config(f"data/menus/{name}.json", entries)
        self.status = f"Saved {len(entries)} widgets -> data/menus/{name}.json"

    def _do_load(self):
        name = text_input2([self.display, self.screen], self.font, "", "Config Name")
        if not name:
            return
        try:
            data = load_widget_config(f"data/menus/{name}.json")
        except FileNotFoundError:
            self.status = f"No file: data/menus/{name}.json"
            return
        entries = data.get("widgets", [])
        self.menus = []
        for e in entries:
            d = Dummy([0, 0], [16, 16], "aqua")
            d.deserialize(e)
            self.menus.append(d)
        self.selected = 0
        self.status = f"Loaded {len(self.menus)} widgets."

    # ---------- helpers ----------
    def _box_from(self, temp, tilesize):
        if self.tiled:
            return organise_poses(
                multiply_lists(temp[0], tilesize),
                add_lists(multiply_lists(temp[1], tilesize), tilesize))
        return organise_poses(temp[0], temp[1])

    def _draw_temp_box(self, temp, tilesize, scroll):
        if self.tiled:
            draw_rect(multiply_lists(temp[0], tilesize),
                      add_lists(multiply_lists(temp[1], tilesize), tilesize),
                      self.display, offset=scroll)
        else:
            draw_rect(temp[0], temp[1], self.display, offset=scroll)

    def _draw_single_cursor(self, t0, tilesize, scroll):
        mouse = pygame.mouse.get_pos()
        ms = [mouse[0] // self.renderscale, mouse[1] // self.renderscale]
        if self.tiled:
            ms = [int((ms[0] + scroll[0]) // self.tilesize),
                  int((ms[1] + scroll[1]) // self.tilesize)]
            draw_rect(multiply_lists(t0, tilesize),
                      add_lists(multiply_lists(ms, tilesize), tilesize),
                      self.display, offset=scroll)
        else:
            ms = [(ms[0] + scroll[0]), (ms[1] + scroll[1])]
            draw_rect(t0, ms, self.display, offset=scroll)

    def _handle_draw_click(self, pos, temp, scroll, tilesize):
        if len(temp) >= 2:
            return
        ms = [pos[0] // self.renderscale, pos[1] // self.renderscale]
        if self.tiled:
            ms = [int((ms[0] + scroll[0]) // self.tilesize),
                  int((ms[1] + scroll[1]) // self.tilesize)]
        else:
            ms = [(ms[0] + scroll[0]), (ms[1] + scroll[1])]

        if len(temp) == 0:
            temp.append(ms)
        elif len(temp) == 1:
            hit = None
            for d in self.menus:
                if self.tiled:
                    if d.get_rect().collidepoint(multiply_lists(ms, tilesize)):
                        hit = d
                else:
                    if d.get_rect().collidepoint(ms):
                        hit = d
            if hit is not None and not self.theresActive:
                self.status = f"Clicked existing dummy: {hit.type}"
                temp.clear()
                return
            temp.append(ms)

    def _common_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_F1, pygame.K_TAB):
                self.toggle_ui()
                return True
        if self.handle_toolbar_click(event):
            return True
        return False

    # =================================================================
    # STAGE 1 — draw
    # =================================================================
    def stage_draw(self):
        temp = []
        tilesize = [self.tilesize, self.tilesize]
        scroll = [0, 0]
        name = ""
        color = ""

        while self.stage == "draw":
            self.display.fill(self.bkg_color)
            self.draw_grid_overlay()

            for d in self.menus:
                d.draw(self.display, scroll)
            scroll_control(scroll, self.tilesize if self.grid else 4)

            if len(temp) > 1:
                if self.theresActive:
                    for d in self.menus:
                        if d.active:
                            info = self._box_from(temp, tilesize)
                            info = [[info[0][0] - d.pos[0], info[0][1] - d.pos[1]],
                                    info[1], info[2]]
                            col = text_input([self.display, self.screen], self.font,
                                             color, "Enter Color") or "red"
                            d.add_dummy(info[0], info[2], col)
                            d.active = False
                            self.theresActive = False
                            temp = []
                else:
                    self._draw_temp_box(temp, tilesize, scroll)
                    name = text_input2([self.display, self.screen], self.font,
                                       name, "Enter Identifier")
                    info = self._box_from(temp, tilesize)
                    dum = Dummy(info[0], info[2], color or "aqua")
                    dum.get_type(name or "widget")
                    dum.params = {}
                    self.menus.append(dum)
                    self.status = f"Added box (type pending). Total: {len(self.menus)}"
                    name = ""
                    color = ""
                    temp = []

            if len(temp) == 1:
                self._draw_single_cursor(temp[0], tilesize, scroll)

            self.draw_toolbar()
            self.draw_status()
            self.draw_ui_indicator()

            self.screen.blit(pygame.transform.scale(self.display,
                                                    self.screen.get_size()), [0, 0])

            mp = pygame.mouse.get_pos()
            for b in self.toolbar_buttons():
                b.update_hover(mp, self.renderscale)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if self._common_event(event):
                    continue
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    if self.ui_visible and event.pos[1] // self.renderscale < 18:
                        continue
                    self._handle_draw_click(event.pos, temp, scroll, tilesize)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit(); sys.exit()
                    if event.key == pygame.K_s:
                        self.stage = "assign"
                        self.status = "Click a dummy on the left, then pick a widget type."

            pygame.display.flip()
            self.clock.tick(60)

    # =================================================================
    # STAGE 2 — assign
    # =================================================================
    def stage_assign(self):
        while self.stage == "assign":
            self.display.fill(self.bkg_color)

            if self.ui_visible:
                pygame.draw.rect(self.display, "black",
                                 [0, 20, 102, self.display.get_height() - 50])
                pygame.draw.line(self.display, "aqua", [102, 20],
                                 [102, self.display.get_height() - 30])
                self.display.blit(self.font.render("Dummies", False, "yellow"), [4, 22])
                visible_rows = (self.display.get_height() - 72) // 14
                self._list_start = max(0, self.selected - visible_rows + 1)
                end = self._list_start + visible_rows
                for i in range(self._list_start, min(end, len(self.menus))):
                    d = self.menus[i]
                    color = "yellow" if i == self.selected else "aqua"
                    line = f"{i:>2} {d.type[:10]}"
                    self.display.blit(self.font.render(line, False, color),
                                      [4, 36 + (i - self._list_start) * 14])

                self.display.blit(self.font.render("Widget Types", False, "yellow"),
                                  [106, 22])
                for t, b in self.palette:
                    b.draw(self.display)

                if self.menus:
                    d = self.menus[self.selected]
                    palette_rows = (len(WIDGET_TYPES) + 3) // 4
                    yy = 24 + palette_rows * 16 + 6
                    self.display.blit(
                        self.font.render(f"Params: {d.type}", False, "yellow"),
                        [106, yy])
                    yy += 14
                    self.display.blit(
                        self.font.render(f"pos: {d.pos}  size: {d.size}",
                                         False, "pink"), [106, yy])
                    yy += 14
                    params = getattr(d, "params", {}) or {}
                    for k, v in params.items():
                        line = f"{k}: {str(v)[:24]}"
                        self.display.blit(self.font.render(line, False, "aqua"),
                                          [106, yy])
                        yy += 12
                else:
                    self.display.blit(
                        self.font.render("No dummies yet. Go to Draw tab.",
                                         False, "pink"), [106, 30])
            else:
                self.display.blit(
                    self.font.render("(UI hidden — F1/TAB to show panel)",
                                     False, "pink"), [8, 24])

            self.draw_toolbar()
            self.draw_status()
            self.draw_ui_indicator()

            self.screen.blit(pygame.transform.scale(self.display,
                                                    self.screen.get_size()), [0, 0])

            mp = pygame.mouse.get_pos()
            if self.ui_visible:
                for b in self.toolbar_buttons():
                    b.update_hover(mp, self.renderscale)
                for _, b in self.palette:
                    b.update_hover(mp, self.renderscale)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if self._common_event(event):
                    continue

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 \
                        and self.ui_visible:
                    mx = event.pos[0] // self.renderscale
                    my = event.pos[1] // self.renderscale

                    if mx < 102 and my > 30:
                        row = (my - 36) // 14
                        idx = self._list_start + row
                        if 0 <= idx < len(self.menus):
                            self.selected = idx
                            self.status = f"Selected dummy {idx} ({self.menus[idx].type})"
                            continue

                    for t, b in self.palette:
                        if b.was_clicked(event, self.renderscale):
                            if self.menus:
                                self._edit_dummy(self.menus[self.selected], preset=t)
                            else:
                                self.status = "No dummy selected. Draw one first."
                            break

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.stage = "draw"
                        self.status = "Right-click twice to place a new widget box."
                    elif event.key == pygame.K_UP and self.menus:
                        self.selected = (self.selected - 1) % len(self.menus)
                    elif event.key == pygame.K_DOWN and self.menus:
                        self.selected = (self.selected + 1) % len(self.menus)
                    elif event.key == pygame.K_RETURN and self.menus:
                        self._edit_dummy(self.menus[self.selected])

            pygame.display.flip()
            self.clock.tick(30)

    def _edit_dummy(self, d, preset=None):
        type_name = preset
        if not type_name:
            type_name = text_input2([self.display, self.screen], self.font,
                                    d.type if d.type != "widget" else "", "Widget Type")
        if not type_name:
            return
        d.type = type_name

        fields = WIDGET_FIELDS.get(type_name, [])
        params = {}
        for key, caster in fields:
            raw = text_input2([self.display, self.screen], self.font, "", key)
            if raw == "":
                continue
            try:
                if key == "options":
                    params[key] = [o.strip() for o in raw.split(",") if o.strip()]
                else:
                    params[key] = caster(raw)
            except Exception:
                params[key] = raw

        if "range_min" in params and "range_max" in params:
            params["range"] = [params.pop("range_min"), params.pop("range_max")]
        d.params = params
        self.status = f"Edited dummy -> {d.type}"

    # =================================================================
    # STAGE 3 — preview (same scale as draw, with scroll)
    # =================================================================
    def stage_preview(self):
        entries = [d.serialize() for d in self.menus
                   if getattr(d, "type", "") and d.type != "widget"]
        live = build_widgets_from_entries(entries, self.font)
        if not live:
            self.status = "Nothing to preview — assign types first."
            self.stage = "assign"
            return

        scroll = [0, 0]
        scroll_speed = 8
        running = True
        while running:
            self.display.fill(self.bkg_color)

            for w in live:
                _draw_widget_live(w, self.display, scroll)

            hint = self.font.render(
                f"Preview — scroll: Wheel / Arrows  |  Home: reset  |  "
                f"Scroll: {scroll[0]},{scroll[1]}  |  ESC to exit",
                False, "yellow")
            self.display.blit(hint, [4, self.display.get_height() - 14])

            self.screen.blit(pygame.transform.scale(self.display,
                                                    self.screen.get_size()), [0, 0])
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.MOUSEWHEEL:
                    scroll[1] -= event.y * 20
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        scroll[1] += event.y * 20
                        scroll[0] -= event.y * 20
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_UP:
                        scroll[1] -= scroll_speed
                    if event.key == pygame.K_DOWN:
                        scroll[1] += scroll_speed
                    if event.key == pygame.K_LEFT:
                        scroll[0] -= scroll_speed
                    if event.key == pygame.K_RIGHT:
                        scroll[0] += scroll_speed
                    if event.key == pygame.K_HOME:
                        scroll[0] = 0
                        scroll[1] = 0
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx = event.pos[0] // self.renderscale
                    my = event.pos[1] // self.renderscale
                    if self.ui_visible and self.tab_preview.rect().collidepoint(mx, my):
                        running = False

            self.clock.tick(60)

        self.stage = "assign"

    # =================================================================
    def run(self):
        while True:
            if self.stage == "draw":
                self.stage_draw()
            elif self.stage == "assign":
                self.stage_assign()
            elif self.stage == "preview":
                self.stage_preview()
            else:
                break
        pygame.quit()


if __name__ == "__main__":
    MenuEditor(2).run()