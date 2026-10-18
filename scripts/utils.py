import pygame
import json
import os

from scripts.registry import resolve, register_type

THEME_COLOR = (0, 10, 30)

def load_image(path):
    image = pygame.image.load(path)
    image.convert()
    return image

def extract_image(source, size, pos):
    surf = pygame.Surface(size)
    surf.blit(source, [0, 0], [pos[0] * size[0], pos[1] * size[0], size[0], size[1]])
    surf.convert()
    return surf

def join(*args):
    joined = []
    for lis in args:
        if lis:
            for item in lis:
                joined.append(item)
    return joined

def join_dict(*args):
    joined = {}
    for dic in args:
        if dic:
            for key in dic:
                if not key in joined:
                    joined[key] = dic[key]
                elif type(dic[key]).__name__ == "list":
                    joined[key] = join(joined[key], dic[key])
                else:
                    joined[key] = [joined[key], dic[key]]
    return joined

def mouse_scroll(slider):
    mp = pygame.mouse.get_pressed()
    if mp[0]:
        mpos = pygame.mouse.get_pos()
        mpos = [int(mpos[0] // 2), int(mpos[1] //2)]
        slider_rect = slider.get_rects()[0]
        if slider_rect.collidepoint(mpos):
            slider.active = True
    
    if slider.active:
        rect = slider.get_rects()[0]
        mpos = pygame.mouse.get_pos()
        mpos = [int(mpos[0] // 2), int(mpos[1] //2)]
        if rect.collidepoint(mpos):
            slider.set_value([int((int(mpos[0] - slider.pos[0]) / slider.size[0]) * (slider.range[1] - slider.range[0])), int((int(mpos[1] - slider.pos[1]) / slider.size[1]) * (slider.range[1] - slider.range[0]))])
        '''else:
            mpos = pygame.mouse.get_pos()
            mpos = [int(mpos[0] // 2), int(mpos[1] //2)]
            slider.incriment_value(mpos[0])
            #slider.set_value(mpos[0] // int(640 // slider.size[0]))'''
            
    if mp[2]:
        #slider.reset_range()
        slider.active = False

def mouse_scroll_silders(sliders):
    mp = pygame.mouse.get_pressed()
    if mp[0]:
        mpos = pygame.mouse.get_pos()
        mpos = [int(mpos[0] // 2), int(mpos[1] //2)]
        for slider in sliders:
            slider_rect = slider.get_rects()[0]
            if slider_rect.collidepoint(mpos):
                slider.active = True
    for slider in sliders:
        if slider.active:
            rect = slider.get_rects()[0]
            mpos = pygame.mouse.get_pos()
            mpos = [int(mpos[0] // 2), int(mpos[1] //2)]
            if rect.collidepoint(mpos):
                slider.set_value([int((int(mpos[0] - slider.pos[0]) / slider.size[0]) * (slider.range[1] - slider.range[0])), int((int(mpos[1] - slider.pos[1]) / slider.size[1]) * (slider.range[1] - slider.range[0]))])
            '''else:
                mpos = pygame.mouse.get_pos()
                mpos = [int(mpos[0] // 2), int(mpos[1] //2)]
                slider.incriment_value(mpos[0])
                #slider.set_value(mpos[0] // int(640 // slider.size[0]))'''
                
        if mp[2]:
            #slider.reset_range()
            slider.active = False

def give_player_id(player, variable):
    player.id = variable
    variable += 1
    return variable

def give_ids(players, variable):
    for player in players:
        variable = give_player_id(player, variable)
    return variable


class Timer:
    def __init__(self, max, rate):
        self.max = max
        self.unorm_rate = rate
        self.rate = 1 / self.unorm_rate
        self.done = False
        self.now = 0
        self.running = False
    
    def copy(self):
        return Timer(self.max, self.unorm_rate)
    
    def start(self):
        self.running = True
        self.done = False
        self.now = 0

    def update(self):
        if self.running:
            if self.now >= self.max:
                self.now = self.max
                self.running = False
                self.done = True
            else:
                self.now += self.rate

timer = Timer(30, 1)
timer.done = True

def btn_control(btn):
    mp = pygame.mouse.get_pressed()
    timer.update()
    if mp[0]:
        mpos = pygame.mouse.get_pos()
        mpos = [int(mpos[0] // 2), int(mpos[1] //2)]
        btn_rect = btn.get_rect()
        if btn_rect.collidepoint(mpos):
            if timer.done:
                btn.set_state()
                timer.start()

def button_control(buttons):
    mp = pygame.mouse.get_pressed()
    timer.update()
    if mp[0]:
        mpos = pygame.mouse.get_pos()
        mpos = [int(mpos[0] // 2), int(mpos[1] //2)]
        for btn in buttons:
            btn_rect = btn.get_rect()
            if btn_rect.collidepoint(mpos):
                if timer.done:
                    btn.set_state()
                    timer.start()

def button_control2(buttons, offset=[0, 0]):
    mp = pygame.mouse.get_pressed()
    timer.update()
    if mp[0]:
        mpos = pygame.mouse.get_pos()
        mpos = [int((mpos[0] // 2)+ offset[0]), int((mpos[1]  //2)+ offset[1])]
        for btn in buttons:
            btn_rect = btn.get_rect()
            if btn_rect.collidepoint(mpos):
                if timer.done:
                    btn.set_state()
                    timer.start()

def draw_rect(pos1, pos2, surf, color="lime", offset= [0, 0], fill=False):
    dists = [abs(pos1[0] - pos2[0]), abs(pos1[1] - pos2[1])]
    top_left = False
    top_right = False
    bottom_left = False
    bottom_right = False
    if pos1[0] < pos2[0]:#top left
        if pos1[1] < pos2[1]:
            top_left = True
        if pos1[1] > pos2[1]:
            bottom_left = True
    if pos1[0] > pos2[0]:
        if pos1[1] < pos2[1]:
            top_right = True
        if pos1[1] > pos2[1]:
            bottom_right = True
    pos = pos1
    if top_left:
        pos = list(pos1)
    if bottom_right:
        pos = list(pos2)
    if not bottom_left or not top_right:
        #rect = pygame.Rect(pos[0]* 16 - offset[0], pos[1]*16- offset[1], dists[0], dists[1])
        rect = pygame.Rect(pos[0]- offset[0], pos[1]- offset[1], dists[0], dists[1])
        pygame.draw.rect(surf, color, rect, 0 if fill else 2, 4)

def get_game_assets(path, dicty):
    f = open(path, "r")
    data = json.load(f)
    assets = data["assets"]
    for asset in assets:
        images = assets[asset]
        temp = []
        for image in images:
            temp.append(extract_image(load_image(image["path"]), image["size"], image["pos"]))
        dicty[asset] = temp
    return dicty

def get_the_other_assets(path, dicty):
    f = open(path, "r")
    data = json.load(f)
    assets = data["other_assets"]
    for asset in assets:
            images = assets[asset]
            temp = []
            for image in images:
                temp.append(extract_image(load_image(image["path"]), image["size"], image["pos"]))
            dicty[asset] = temp
    return dicty
    

def multiply_lists(list1, list2):
    return [list1[0] * list2[0], list1[1] * list2[1]]

def add_lists(list1, list2):
    return [list1[0] + list2[0], list1[1] + list2[1]]

def load_image2(path, setcolorkey= True,color="black"):
    image = pygame.image.load(path)
    image.convert_alpha()
    if setcolorkey:
        image.set_colorkey(color)
    return image

def load_images(path, setcolorkey= True,color="black"):
    images = []
    for image in os.listdir(path):
        images.append(load_image2(path + "/" + image, setcolorkey,color))
    return images

def load_loadable_images(path):
    images = []
    for image in os.listdir(path):
        img = load_image(path + "/" + image)
        images.append({"path": path + "/" + image, "size": img.get_size(), "pos": [0, 0]})
    return images

def scroll_control(variable, amnt=4):
    key = pygame.key.get_pressed()
    if key[pygame.K_UP]:
        variable[1] -= amnt
    if key[pygame.K_DOWN]:
        variable[1] += amnt
    if key[pygame.K_LEFT]:
        variable[0] -= amnt
    if key[pygame.K_RIGHT]:
        variable[0] += amnt

def wasd_scroll_control(variable, amnt=4):
    key = pygame.key.get_pressed()
    if key[pygame.K_w]:
        variable[1] -= amnt
    if key[pygame.K_s]:
        variable[1] += amnt
    if key[pygame.K_a]:
        variable[0] -= amnt
    if key[pygame.K_d]:
        variable[0] += amnt

def organise_poses(pos1, pos2):
    dists = [abs(pos1[0] - pos2[0]), abs(pos1[1] - pos2[1])]
    top_left = False
    top_right = False
    bottom_left = False
    bottom_right = False
    if pos1[0] < pos2[0]:#top left
        if pos1[1] < pos2[1]:
            top_left = True
        if pos1[1] > pos2[1]:
            bottom_left = True
    if pos1[0] > pos2[0]:
        if pos1[1] < pos2[1]:
            top_right = True
        if pos1[1] > pos2[1]:
            bottom_right = True
    pos = pos1
    if top_left:
        pos = [list(pos1), list(pos2)]
    if bottom_right:
        pos = [list(pos2), list(pos1)]
    return [pos[0], pos[1], dists]

def slider_handle(sliders, surf, draw_func=3, control_func=2):
    for slider in sliders:
        if draw_func <= 1:
            slider.update(surf)
        elif draw_func == 2:
            slider.update2(surf)
        elif draw_func >= 3:
            slider.update3(surf)
    match control_func:
        case 1:
            mouse_scroll(sliders)
        case _:
            mouse_scroll_silders(sliders)

def offseted_slider_handle(sliders, surf,offset=[0, 0], draw_func=3):
    for slider in sliders:
        if draw_func <= 1:
            slider.update(surf, offset)
        elif draw_func == 2:
            slider.update2(surf, offset)
        elif draw_func >= 3:
            slider.update3(surf, offset)

def button_handle(buttons, surf, offset=[0, 0], control_func=2):
    for button in buttons:
        button.update(surf, offset)
    match control_func:
        case 1:
            button_control(buttons)
        case _:
            button_control2(buttons, offset)

def label_handle(labels, surf, offset=[0, 0], setables=[]):
    if setables:
        for x, text in enumerate(setables):
            for y, label in enumerate(labels):
                if x == y:
                    label.set_text(text)
    for label in labels:
        label.update(surf, offset)

def timer_handle(timers):
    for timer in timers:
        timer.update()
        if timer.done:
            timer.start()

def make_dummy_dict(list1, save_list):
    for dummy in list1:
        temp = {}
        temp["name"] = dummy.type
        temp["size"] = dummy.size
        temp["color"] = dummy.color
        temp["pos"] = dummy.pos
        if dummy.dummies:
            tmp = []
            temp["dummies"] = make_dummy_dict(dummy.dummies, tmp)
        else:
            temp["dummies"] = []
        save_list.append(temp)
    return save_list


def dists(point1, point2):
    return [abs(point1[0] - point2[0]), abs(point1[1] - point2[1])]

# ============================================================
# widget config building
# ============================================================
WIDGET_FIELDS = {
    "Label":          [("text", str)],
    "TextBox":        [("text", str)],
    "Button":         [("text", str)],
    "RectedButton":   [("text", str)],
    "Button2":        [("txt", str)],
    "Slider":         [("range_min", int), ("range_max", int), ("value", int)],
    "VerticalSlider": [("range_min", int), ("range_max", int), ("value", int)],
    "Table":          [("columns", int), ("rows", int)],
    "Custom_Table":   [("columns", int), ("rows", int)],
    "Dialog":         [("text", str), ("rate", int)],
    "Checkbox":       [("label", str), ("checked", str)],
    "ProgressBar":    [("value", int), ("max_value", int)],
    "ToggleSwitch":   [("state", str)],
    "ImageWidget":    [("image_path", str)],
    "Panel":          [("border", int), ("color", str)],
    "Dropdown":       [("options", str), ("selected", int)],
}

DEFAULT_WIDGET_COLORS = ("blue", "aqua")


def widget_config_entries(config):
    if isinstance(config, dict):
        if "widgets" in config:
            return config["widgets"]
        if "config" in config and "new" in config["config"]:
            return config["config"]["new"]
        if "new" in config:
            return config["new"]
        return []
    return list(config)


def load_widget_config(path):
    with open(path, "r") as f:
        return json.load(f)


def save_widget_config(path, entries):
    with open(path, "w") as f:
        json.dump({"widgets": entries}, f, indent=2)


def fill_dummy_data(entry):
    e = dict(entry)
    t = e.get("type", "")
    if t in ("Label", "TextBox") and not e.get("text"):
        e["text"] = "Sample Text"
    if t == "Button" and not e.get("text"):
        e["text"] = "Button"
    if t == "Button2" and not e.get("txt"):
        e["txt"] = "Button2"
    if t == "Dialog" and not e.get("text"):
        e["text"] = "Dialog text"
    if t in ("Table", "Custom_Table"):
        e.setdefault("columns", 3)
        e.setdefault("rows", 3)
        if "text_items" not in e:
            e["text_items"] = {
                f"{c};{r}": f"c{c}r{r}"
                for c in range(e["columns"]) for r in range(e["rows"])
            }
    if t == "Checkbox":
        e.setdefault("label", "Check me")
    if t == "ProgressBar":
        e.setdefault("value", 45)
        e.setdefault("max_value", 100)
    if t == "Dropdown":
        e.setdefault("options", ["Option A", "Option B", "Option C"])
    if t in ("Slider", "VerticalSlider"):
        e.setdefault("range_min", 0)
        e.setdefault("range_max", 100)
        e.setdefault("value", 50)
    return e


def _placeholder_surface():
    return pygame.Surface([1, 1])


def _bare_widget(cls, entry, font):
    t = entry.get("type", "")
    pos = entry.get("pos", [0, 0])
    size = entry.get("size", [16, 16])
    color = entry.get("color", "aqua")
    colors = entry.get("colors", list(DEFAULT_WIDGET_COLORS))

    if t in ("Label", "TextBox"):
        return cls(entry.get("text", ""), pos, font, colors)
    if t in ("Button", "RectedButton"):
        return cls(pos, color, size)
    if t == "Button2":
        return cls(font, pos)
    if t == "Slider":
        return cls([entry.get("range_min", 0), entry.get("range_max", 100)], pos)
    if t == "VerticalSlider":
        return cls([entry.get("range_min", 0), entry.get("range_max", 100)], pos)
    if t == "Table":
        return cls(font, pos, entry.get("columns", 2), entry.get("rows", 2))
    if t == "Custom_Table":
        return cls(font, pos, size, entry.get("columns", 2), entry.get("rows", 2))
    if t == "Dialog":
        return cls(font, entry.get("text", ""), pos, size,
                   entry.get("colors", ["aqua", "blue"]))
    if t == "TitleBar":
        return cls(font, _placeholder_surface(), entry.get("text", "Title"))
    if t == "Checkbox":
        return cls(pos, entry.get("label", ""), False, size, colors, font)
    if t == "ProgressBar":
        return cls(pos, size, entry.get("value", 0),
                   entry.get("max_value", 100), colors)
    if t == "ToggleSwitch":
        return cls(pos, size, False, colors)
    if t == "ImageWidget":
        return cls(pos, entry.get("image_path", ""), size)
    if t == "Panel":
        return cls(pos, size, entry.get("color", "blue"))
    if t == "Dropdown":
        opts = entry.get("options")
        if isinstance(opts, str):
            opts = [o.strip() for o in opts.split(",") if o.strip()]
        return cls(pos, opts, entry.get("selected", 0), size, colors, font)
    return cls()


def build_widget(entry, font=None):
    t = entry.get("type", "")
    if not t or t == "widget":
        return None
    cls = resolve(f"widget.{t}")
    w = _bare_widget(cls, entry, font)
    if hasattr(w, "deserialize"):
        w.deserialize(entry)
    return w


def build_widgets(config, font=None):
    return [w for w in (build_widget(e, font)
                        for e in widget_config_entries(config))
            if w is not None]


def build_widgets_from_dummies(dummies, font=None):
    entries = [fill_dummy_data(d.serialize()) for d in dummies
               if getattr(d, "type", "") and d.type != "widget"]
    return build_widgets(entries, font)


def preview_widgets(widgets, font, resolution=(640, 480),
                    scale=2, background=(0, 10, 30)):
    """Standalone preview loop. ESC or window close exits."""
    pygame.init()
    screen = pygame.display.set_mode(resolution)
    display = pygame.Surface((resolution[0] // scale, resolution[1] // scale))
    clock = pygame.time.Clock()
    running = True
    while running:
        display.fill(background)
        for w in widgets:
            w.update(display, [0, 0])
        screen.blit(pygame.transform.scale(display, resolution), (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


def preview_menu(config, font_path="data/fonts/at01.ttf",
                 resolution=(640, 480), scale=2):
    """Preview directly from a config (path or dict)."""
    raw = load_widget_config(config) if isinstance(config, str) else config
    entries = [fill_dummy_data(e) for e in widget_config_entries(raw)]
    font = pygame.font.Font(font_path, 16)
    widgets = build_widgets(entries, font=font)
    preview_widgets(widgets, font, resolution, scale)