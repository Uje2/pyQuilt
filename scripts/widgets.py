import pygame
import sys

from scripts.registry import resolve, register_type


# ============================================================
# ================ EXISTING WIDGETS (unchanged) ==============
# ============================================================

class Slider:
    def __init__(self, range, pos, value=0,size=[16, 8], colors=["blue", "aqua"], alpha=0):
        self.id = None
        self.range = list(range)
        self.value = value
        self.size = list(size)
        self.fg_size = [8, self.size[1]]
        self.pos = list(pos)
        self.img = pygame.Surface(self.size)
        self.fg_img = pygame.Surface(self.fg_size)
        self.set_colors(colors)
        self.alpha = alpha
        self.init_range = self.range
        self.active = False

    def set_transparency(self, value):
        self.img.set_alpha(value)

    def get_rects(self):
        return self.img.get_rect(topleft=self.pos), pygame.Rect(self.value, self.pos[1], self.fg_size[0], self.fg_size[1])

    def set_pos(self, pos):
        self.pos = list(pos)

    def set_value(self, value):
        self.value = value[0]

    def incriment_value(self, value):
        self.value = value
        self.range = [0, 320]
    def reset_range(self):
        self.range = self.init_range

    def set_size(self, size):
        self.size = list(size)
        self.img = pygame.Surface(self.size)

    def set_colors(self, colors):
        self.bkg_color = colors[0]
        self.fg_color = colors[1]
        self.img.fill(self.bkg_color)
        self.fg_img.fill(self.fg_color)

    def normalized_value(self):
        value = int(self.value // (self.range[1] / self.size[0]))
        return value

    def draw(self, surf, offset=[0, 0]):
        self.img.blit(self.fg_img, [self.normalized_value(), 0])
        surf.blit(self.img, (self.pos[0] - offset[0], self.pos[1] - offset[1]))
        self.set_colors([self.bkg_color, self.fg_color])

    def draw2(self, surf, offset=[0, 0]):
        self.img.fill("black")
        self.fg_img.fill("black")
        pygame.draw.rect(self.fg_img, self.fg_color, [0, 0 , self.fg_img.get_width(), self.fg_img.get_height()], 2)
        self.img.blit(self.fg_img, [self.normalized_value(), 0])
        pygame.draw.rect(self.img, self.bkg_color, [0, 0 , self.img.get_width(), self.img.get_height()], 2)
        surf.blit(self.img, (self.pos[0] - offset[0], self.pos[1] - offset[1]))
        self.set_colors([self.bkg_color, self.fg_color])

    def draw3(self, surf, offset=[0, 0]):
        var = 4
        self.img.fill("black")
        self.img.set_colorkey("black")
        self.fg_img.fill("black")
        pygame.draw.rect(self.img, self.bkg_color, [0, int(self.img.get_height() // 2) - (int(self.img.get_height() // var)// 2), self.img.get_width(), int(self.img.get_height() // var)], 2)
        pygame.draw.rect(self.fg_img, self.fg_color, [0, 0 , self.fg_img.get_width(), self.fg_img.get_height()], 2)
        self.img.blit(self.fg_img, [self.normalized_value(), 0])
        surf.blit(self.img, (self.pos[0] - offset[0], self.pos[1] - offset[1]))
        self.set_colors([self.bkg_color, self.fg_color])

    def update(self, surf, offset=[0, 0]):
        self.draw(surf, offset)

    def update2(self, surf, offset=[0, 0]):
        self.draw2(surf, offset)

    def update3(self, surf, offset=[0, 0]):
        self.draw3(surf, offset)


class VerticalSlider(Slider):
    def __init__(self, range, pos, value=0,size=[8, 16], colors=["blue", "aqua"], alpha=0):
        super().__init__(range, pos, value, size, colors, alpha)
        self.fg_size = [self.size[1], 8]
        self.fg_img = pygame.Surface(self.fg_size)

    def set_value(self, value):
        self.value = value[1]

    def normalized_value(self):
        value = int(self.value // (self.range[1] / self.size[1]))
        return value

    def draw(self, surf, offset=[0, 0]):
        self.img.blit(self.fg_img, [0, self.normalized_value()])
        surf.blit(self.img, (self.pos[0] - offset[0], self.pos[1] - offset[1]))
        self.set_colors([self.bkg_color, self.fg_color])

    def draw2(self, surf, offset=[0, 0]):
        self.img.fill("black")
        self.fg_img.fill("black")
        pygame.draw.rect(self.fg_img, self.fg_color, [0, 0 , self.fg_img.get_width(), self.fg_img.get_height()], 2)
        self.img.blit(self.fg_img, [0, self.normalized_value()])
        pygame.draw.rect(self.img, self.bkg_color, [0, 0 , self.img.get_width(), self.img.get_height()], 2)
        surf.blit(self.img, (self.pos[0] - offset[0], self.pos[1] - offset[1]))
        self.set_colors([self.bkg_color, self.fg_color])

    def draw3(self, surf, offset=[0, 0]):
        var = 4
        self.img.fill("black")
        self.img.set_colorkey("black")
        self.fg_img.fill("black")
        pygame.draw.rect(self.img, self.bkg_color, [int(self.img.get_width() // 2) - (int(self.img.get_width() // var)// 2), 0, int(self.img.get_width() // var), self.img.get_height()], 2)
        pygame.draw.rect(self.fg_img, self.fg_color, [0, 0 , self.fg_img.get_width(), self.fg_img.get_height()], 2)
        self.img.blit(self.fg_img, [0, self.normalized_value()])
        surf.blit(self.img, (self.pos[0] - offset[0], self.pos[1] - offset[1]))
        self.set_colors([self.bkg_color, self.fg_color])

    def update(self, surf, offset=[0, 0]):
        self.draw(surf, offset)

    def update2(self, surf, offset=[0, 0]):
        self.draw2(surf, offset)

    def update3(self, surf, offset=[0, 0]):
        self.draw3(surf, offset)


class Label:
    def __init__(self, text, pos, font, colors, secondary="black", transp=False):
        self.id = None
        self.font = font
        self.transp = transp
        self.secondary_color = secondary
        self.text = text
        self.pos = list(pos)
        self.colors = colors
        self.r_width = 2
        self.set_text(text)

    def set_text(self, text):
        self.text = text
        txt = self.font.render(text, False, self.colors[1])
        self.surf = pygame.Surface(txt.get_size())
        self.surf.fill(self.secondary_color)
        pygame.draw.rect(self.surf, self.colors[0], [0, 0, self.surf.get_width(), self.surf.get_height()], self.r_width)
        if self.transp:
            self.surf.set_colorkey(self.secondary_color)
        self.surf.blit(txt, (0, 0))

    def draw(self, surf, offset=[0, 0]):
        surf.blit(self.surf, [self.pos[0] - offset[0], self.pos[1] - offset[1]])

    def update(self, surf, offset=[0, 0]):
        self.draw(surf, offset)


class TextBox(Label):
    def __init__(self, text, pos, font, colors, secondary="black", transp=False):
        self.limit = 12
        self.w = 7
        self.h = 16
        super().__init__(text, pos, font, colors, secondary, transp)

    def set_text(self, text):
        self.text = text
        txts = []
        maxs = len(self.text)
        cols = int(maxs // self.limit)
        if cols != 0:
            for i in range(self.limit, maxs + self.limit, self.limit):
                txts.append(self.text[i-self.limit:i])
            if maxs % self.limit != 0:
                txts.append(self.text[cols:])
        else:
            txts.append(self.text)
        print(txts)
        self.surf = pygame.Surface([(self.limit + 1) * self.w, len(txts) * self.h])
        self.surf.fill(self.secondary_color)
        pygame.draw.rect(self.surf, self.colors[0], [0, 0, self.surf.get_width(), self.surf.get_height()], self.r_width)
        if self.transp:
            self.surf.set_colorkey(self.secondary_color)
        for i, txt in enumerate(txts):
            fon = self.font.render(txt, False, self.colors[1])
            self.surf.blit(fon, [self.r_width, i * self.h])


class Button:
    def __init__(self, pos, color, size=[16, 16]):
        self.id = None
        self.pos = list(pos)
        self.color = color
        self.active = False
        self.size = list(size)
        self.surf = pygame.Surface(self.size)
        self.set_color(self.color)
        self.text = ""
        self.icon = pygame.Surface(self.size)
        self.has_icon = False
        self.bkg = ""

    def get_rect(self):
        return self.surf.get_rect(topleft=self.pos)

    def set_state(self):
        self.active = not self.active

    def get_state(self):
        return self.active

    def get_bkg(self, image):
        self.bkg = image

    def set_text(self, font, text, color, padding=[4, 8]):
        self.text = font.render(text, False, color)
        self.icon.fill("black")
        self.icon.blit(self.text, [int(self.size[0] // padding[0]), int(self.size[1] // padding[1])])
        self.icon.set_colorkey("black")

    def set_color(self, color):
        self.color = color
        self.surf.fill(self.color)

    def set_icon(self, icon, color, padding=[2, 1]):
        self.has_icon = True
        self.icon.blit(icon, [int(self.size[0] // padding[0]), int(self.size[1] // padding[1])])

    def rected(self):
        rect = self.get_rect()
        pygame.draw.rect(self.surf, self.color, [0, 0, rect.width, rect.height], 2, 3)

    def draw(self, surf, offset=[0, 0]):
        if self.bkg != "":
            self.surf.blit(self.bkg, [0, 0])
        if self.has_icon:
            self.surf.blit(self.icon, [0, 0])
        elif self.text != "":
            self.surf.blit(self.icon, [0, 0])
        surf.blit(self.surf, [self.pos[0] - offset[0], self.pos[1] - offset[1]])

    def update(self, surf, offset=[0, 0]):
        self.draw(surf, offset)


class RectedButton(Button):
    def __init__(self, pos, color, size=[16, 16]):
        super().__init__(pos, color, size)

    def set_color(self, color):
        self.color = color
        self.surf.set_colorkey("black")

    def draw(self, surf, offset=[0, 0]):
        self.rected()
        super().draw(surf, offset)


class Button2:
    def __init__(self, font, pos, padding=[8, 1], colors=["aqua", "yellow"], text="Button2"):
        self.id = None
        self.font = font
        self.pos = list(pos)
        self.txt = text
        self.color = colors[1]
        self.text_color = colors[0]
        self.padding = list(padding)
        self.text = self.font.render(self.txt, False, self.text_color)
        self.size = [self.text.get_width()+ (self.padding[0] * 2), self.text.get_height() + (self.padding[1] * 2)]
        self.surf = pygame.Surface(self.size)
        self.surf.fill("black")
        self.surf.set_colorkey("black")
        self.active = False

    def set_text(self, text):
        self.txt = text
        self.text = self.font.render(self.txt, False, self.color)

    def set_padding(self, padding):
        self.padding = list(padding)

    def set_colors(self, colors):
        self.set_color(colors[1])
        self.text_color = colors[0]
        self.set_text(self.txt)
        self.surf.fill("black")
        self.surf.set_colorkey("black")

    def get_rect(self):
        return self.surf.get_rect(topleft=self.pos)

    def set_state(self):
        self.active = not self.active

    def get_state(self):
        return self.active

    def draw(self, surf, offset=[0, 0]):
        self.surf.blit(self.text, [self.padding[0], 0])
        surf.blit(self.surf, [self.pos[0] - offset[0], self.pos[1] - offset[1]])

    def rected(self):
        rect = self.get_rect()
        pygame.draw.rect(self.surf, self.color, [0, 0, rect.width, rect.height], 2, 3)

    def update(self, surf, offset=[0, 0]):
        self.rected()
        self.draw(surf, offset)


class TitleBar:
    def __init__(self, font: pygame.font.Font, display: pygame.Surface, text="TitleBar"):
        self.id = None
        self.display = display
        self.font = font
        self.text = text
        self.surf = pygame.Surface([self.display.get_width(), 30])
        self.surf_color = "magenta"
        self.text_color = "blue"
        self.set_text(self.text)
        self.set_color([self.surf_color, self.text_color])

    def set_text(self, text):
        self.text = text
        self.title = self.font.render(self.text, False, self.text_color)
        self.surf.blit(self.title, [self.surf.get_width() // 2 - self.title.get_width() // 2, 5])

    def set_color(self, colors):
        self.surf_color = colors[0]
        self.text_color = colors[1]
        self.surf.fill(self.surf_color)
        self.set_text(self.text)
        self.surf.set_alpha(50)

    def draw(self):
        self.display.blit(self.surf, [0, 0])

    def update(self):
        self.draw()


def make_font(text: str, font: pygame.font.Font, color: tuple | str ):
    fon = font.render(text, False, color)
    return fon


WIDTH = 32


class Table:
    def __init__(self, font, pos, columns, rows, font_color="aqua"):
        self.id = None
        self.columns = columns
        self.rows = rows
        self.pos = list(pos)
        self.font = font
        self.index = [0, 0]
        self.font_color = font_color
        self.items = {}
        self.text_items = {}
        self.color = "blue"
        for column in range(self.columns):
            for row in range(self.rows):
                self.items[str(column) + ";" + str(row)] = make_font("...", self.font, self.font_color)
                self.text_items[str(column) + ";" + str(row)] = "..."
        self.biggest = "0;0"
        self.draw_onto_surf()

    def add_item(self, item: str, index):
        cell = str(index[0]) + ";" + str(index[1])
        cell_item = make_font(item, self.font, self.font_color)
        self.items[cell] = cell_item
        self.text_items[cell] = item
        if cell_item.width > self.items[self.biggest].width:
            self.biggest = cell
        self.draw_onto_surf()

    def add_items(self, items):
        for item in items:
            self.add_item(item[0], item[1])

    def get_rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], (self.items[self.biggest].width + 5) * self.columns, self.rows * WIDTH)

    def draw_onto_surf(self):
        table_rect = self.get_rect()
        self.surface = pygame.Surface((table_rect.width, table_rect.height))
        self.surface.fill(self.color)
        for item in self.items:
            cell_item = self.items[item]
            pos = item.split(";")
            pos = [int(pos[0]), int(pos[1])]
            blit_pos = [int(pos[0] * self.items[self.biggest].width), int(pos[1] * WIDTH)]
            self.surface.blit(cell_item, blit_pos)

    def get_table_color(self, color: tuple | str):
        self.color = color
        self.surface.fill(self.color)
        self.draw_onto_surf()

    def make_table_transparent(self):
        self.get_table_color(self.color)
        self.surface.set_colorkey(self.color)

    def set_table_opacity(self, alpha: int):
        self.get_table_color(self.color)
        self.surface.set_alpha(alpha)

    def set_row_font_color(self, row_num, color):
        for item in self.text_items:
            cell_item = make_font(self.text_items[item], self.font, color)
            self.items[item] = cell_item
            pos = item.split(";")
            pos = [int(pos[0]), int(pos[1])]
            if pos[1] == row_num:
                blit_pos = [int(pos[0] * self.items[self.biggest].width), int(pos[1] * WIDTH)]
                self.surface.blit(cell_item, blit_pos)

    def set_column_font_color(self, column_num, color):
        for item in self.text_items:
            cell_item = make_font(self.text_items[item], self.font, color)
            self.items[item] = cell_item
            pos = item.split(";")
            pos = [int(pos[0]), int(pos[1])]
            if pos[0] == column_num:
                blit_pos = [int(pos[0] * self.items[self.biggest].width), int(pos[1] * WIDTH)]
                self.surface.blit(cell_item, blit_pos)

    def mouse_select(self, index, scale, offset=[0, 0]):
        mc = pygame.mouse.get_pressed()
        if mc[index]:
            mp = pygame.mouse.get_pos()
            mp = [int(mp[0] // scale), int(mp[1] // scale)]
            check_pos = [(mp[0]  + offset[0]- self.pos[0])// self.items[self.biggest].width,( mp[1]  + offset[1] - self.pos[1]) // WIDTH]
            check_pos = str(check_pos[0]) + ";" + str(check_pos[1])
            if check_pos in self.text_items:
                return self.text_items[check_pos]
            return ""
        return ""

    def mouse_select2(self, index, scale, offset=[0, 0]):
        mc = pygame.mouse.get_pressed()
        if mc[index]:
            mp = pygame.mouse.get_pos()
            mp = [int(mp[0] // scale), int(mp[1] // scale)]
            this_pos = [(mp[0]  + offset[0]- self.pos[0])// self.items[self.biggest].width,( mp[1]  + offset[1] - self.pos[1]) // WIDTH]
            check_pos = str(this_pos[0]) + ";" + str(this_pos[1])
            if check_pos in self.text_items:
                return [self.text_items[check_pos], this_pos]
            return ""
        return ""

    def prompted_select(self, prompt, scale, offset=[0, 0]):
        if prompt:
            mp = pygame.mouse.get_pos()
            mp = [int(mp[0] // scale), int(mp[1] // scale)]
            check_pos = [(mp[0]  + offset[0]- self.pos[0])// self.items[self.biggest].width,( mp[1]  + offset[1] - self.pos[1]) // WIDTH]
            check_pos = str(check_pos[0]) + ";" + str(check_pos[1])
            if check_pos in self.text_items:
                return self.text_items[check_pos]
            return ""
        return ""

    def set_table_pos(self, pos):
        self.pos = list(pos)

    def draw(self, surf, offset=[0, 0]):
        table_rect = self.get_rect()
        surf.blit(self.surface, [table_rect.x - offset[0], table_rect.y - offset[1]])


class Dialog:
    def __init__(self, font, text, pos, size, colors, rate=2):
        self.id = None
        self.pos = list(pos)
        self.text = text
        self.font = font
        self.size = size
        self.now_size = [5, size[1]]
        self.rate = rate
        self.colors = colors
        self.done = False
        self.active = False

    def draw(self, surf, offset=[0, 0]):
        self.surface = pygame.Surface(self.now_size)
        text = self.font.render(self.text, False, self.colors[0])
        self.surface.fill(self.colors[1])
        self.surface.blit(text, [int((self.size[0] // 2) - text.width), int((self.size[1] // 2) - text.height)])
        surf.blit(self.surface, [self.pos[0] - offset[0], self.pos[1] - offset[1]])

    def update(self, surf, offset=[0, 0]):
        if self.active:
            self.now_size[0] += self.rate
            self.now_size = [int(self.now_size[0]), int(self.now_size[1])]
            self.draw(surf, offset)
            if self.now_size[0] >= self.size[0]:
                self.now_size[0] = self.size[0]
                self.done = True
                self.active = False
    def reset(self):
        self.done = False
        self.now_size = [5, self.size[1]]

    def start_with_text(self, text):
        self.text = text
        self.active = True
        self.reset()

    def start(self):
        self.active = True
        self.reset()


class Custom_Table:
    def __init__(self, font, pos, size, columns, rows, font_color="aqua"):
        self.id = None
        self.columns = columns
        self.rows = rows
        self.size = list(size)
        self.pos = list(pos)
        self.font = font
        self.index = [0, 0]
        self.font_color = font_color
        self.items = {}
        self.text_items = {}
        self.color = "blue"
        for column in range(self.columns):
            for row in range(self.rows):
                self.items[str(column) + ";" + str(row)] = make_font("...", self.font, self.font_color)
                self.text_items[str(column) + ";" + str(row)] = "..."
        self.biggest = "0;0"
        self.draw_onto_surf()

    def set_size(self, new_size):
        self.size = list(new_size)

    def add_item(self, item: str, index):
        cell = str(index[0]) + ";" + str(index[1])
        cell_item = make_font(item, self.font, self.font_color)
        self.items[cell] = cell_item
        self.text_items[cell] = item
        if cell_item.width > self.items[self.biggest].width:
            self.biggest = cell
        self.draw_onto_surf()

    def add_items(self, items):
        for item in items:
            self.add_item(item[0], item[1])

    def get_rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], (self.size[0] + 5) * self.columns, self.rows * self.size[1])

    def draw_onto_surf(self):
        table_rect = self.get_rect()
        self.surface = pygame.Surface((table_rect.width, table_rect.height))
        self.surface.fill(self.color)
        for item in self.items:
            cell_item = self.items[item]
            pos = item.split(";")
            pos = [int(pos[0]), int(pos[1])]
            blit_pos = [int(pos[0] * self.size[0]), int(pos[1] * self.size[1])]
            self.surface.blit(cell_item, blit_pos)

    def get_table_color(self, color: tuple | str):
        self.color = color
        self.surface.fill(self.color)
        self.draw_onto_surf()

    def make_table_transparent(self):
        self.get_table_color(self.color)
        self.surface.set_colorkey(self.color)

    def set_table_opacity(self, alpha: int):
        self.get_table_color(self.color)
        self.surface.set_alpha(alpha)

    def set_row_font_color(self, row_num, color):
        for item in self.text_items:
            cell_item = make_font(self.text_items[item], self.font, color)
            self.items[item] = cell_item
            pos = item.split(";")
            pos = [int(pos[0]), int(pos[1])]
            if pos[1] == row_num:
                blit_pos = [int(pos[0] * self.size[0]), int(pos[1] * self.size[1])]
                self.surface.blit(cell_item, blit_pos)

    def set_column_font_color(self, column_num, color):
        for item in self.text_items:
            cell_item = make_font(self.text_items[item], self.font, color)
            self.items[item] = cell_item
            pos = item.split(";")
            pos = [int(pos[0]), int(pos[1])]
            if pos[0] == column_num:
                blit_pos = [int(pos[0] * self.size[0]), int(pos[1] * self.size[1])]
                self.surface.blit(cell_item, blit_pos)
    def empty(self):
        for column in range(self.columns):
            for row in range(self.rows):
                self.items[str(column) + ";" + str(row)] = make_font("...", self.font, self.font_color)
                self.text_items[str(column) + ";" + str(row)] = "..."
        self.biggest = "0;0"
        self.draw_onto_surf()

    def set_table_pos(self, pos):
        self.pos = list(pos)

    def draw(self, surf, offset=[0, 0]):
        table_rect = self.get_rect()
        surf.blit(self.surface, [table_rect.x - offset[0], table_rect.y - offset[1]])

    def mouse_select(self, index, scale, offset=[0, 0]):
        mc = pygame.mouse.get_pressed()
        if mc[index]:
            mp = pygame.mouse.get_pos()
            mp = [int(mp[0] // scale), int(mp[1] // scale)]
            check_pos = [(mp[0]  + offset[0]- self.pos[0])// self.size[0],( mp[1]  + offset[1] - self.pos[1]) // self.size[1]]
            check_pos = str(check_pos[0]) + ";" + str(check_pos[1])
            if check_pos in self.text_items:
                return self.text_items[check_pos]
            return ""
        return ""

    def prompted_select(self, prompt, scale, offset=[0, 0]):
        if prompt:
            mp = pygame.mouse.get_pos()
            mp = [int(mp[0] // scale), int(mp[1] // scale)]
            check_pos = [(mp[0]  + offset[0]- self.pos[0])// self.size[0],( mp[1]  + offset[1] - self.pos[1]) // self.size[1]]
            check_pos = str(check_pos[0]) + ";" + str(check_pos[1])
            if check_pos in self.text_items:
                return self.text_items[check_pos]
            return ""
        return ""


def text_input(surfs, font, text_store, name= "Text Input", color="blue", font_color="aqua"):
    running = True
    title_bar = TitleBar(font, surfs[0], name)
    pos = [int(surfs[0].get_width() // 2), int(surfs[0].get_height() // 2)]
    display_text = font.render(text_store, False, font_color)

    while running:
        surfs[0].fill((0, 10, 30))
        surfs[0].blit(display_text, [pos[0] - display_text.width, pos[1]])
        title_bar.update()
        surfs[1].blit(pygame.transform.scale(surfs[0], surfs[1].get_size()), (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return text_store
                if event.key == pygame.K_TAB:
                    text_store = ""
                    display_text = font.render(text_store, False, font_color)
                if event.key == pygame.K_BACKSPACE:
                    text_store = text_store[:-1]
                    display_text = font.render(text_store, False, font_color)
            if event.type == pygame.TEXTINPUT:
                text_store += event.text
                display_text = font.render(text_store, False, font_color)
        pygame.display.update()


def text_input2(surfs, font, text_store, name= "Text Input", color="blue", font_color="aqua"):
    running = True
    max = 26
    title_bar = TitleBar(font, surfs[0], name)
    pos = [int(surfs[0].get_width() // 2), int(surfs[0].get_height() // 2)]
    texts = []
    size = 16

    while running:
        surfs[0].fill((0, 10, 30))
        texts = []
        x = int(len(text_store) // max)
        y = len(text_store) % max
        if x != 0:
            for i in range(x):
                texts.append(text_store[i * max:(i * max) + max])
            if y > 0:
                texts.append(text_store[x * max:(x * max) + y])
        else:
            texts.append(text_store)
        list1 = texts.copy()
        list1.reverse()
        if len(texts) > 1:
            for i, text in enumerate(list1):
                txt = font.render(text, False, font_color)
                surfs[0].blit(txt, [pos[0] - txt.width, pos[1] - (i * size)])
        else:
            txt = font.render(texts[0], False, font_color)
            surfs[0].blit(txt, [pos[0] - txt.width, pos[1]])
        title_bar.update()
        surfs[1].blit(pygame.transform.scale(surfs[0], surfs[1].get_size()), (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return text_store
                if event.key == pygame.K_TAB:
                    text_store = ""
                if event.key == pygame.K_BACKSPACE:
                    text_store = text_store[:-1]
            if event.type == pygame.TEXTINPUT:
                text_store += event.text
        pygame.display.update()


class Dummy:
    def __init__(self, pos, size, color="aqua"):
        self.id = None
        self.size = list(size)
        self.pos = list(pos)
        self.color = color
        self.dummies = []
        self.surf = pygame.Surface(self.size)
        self.surf.fill(self.color)
        self.active = False
        self.type = ""

    def get_rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def set_color(self, color):
        self.color = color
        self.surf.fill(color)

    def set_size(self, size):
        self.size = list(size)

    def set_pos(self, pos):
        self.pos = list(pos)

    def add_dummy(self, pos, size, color="pink"):
        dummy = Dummy(pos, size, color)
        self.dummies.append(dummy)
        self.surf.blit(dummy.surf, dummy.pos)

    def activate(self):
        self.active = not self.active

    def draw(self, surf, offset=[0, 0]):
        surf.blit(self.surf, [self.pos[0] - offset[0], self.pos[1] - offset[1]])

    def get_type(self, typee):
        self.type = typee


# ============================================================
# ============ SERIALIZE / DESERIALIZE PATCHES ===============
# ============================================================

def _slider_ser(self):
    return {
        "type": type(self).__name__,
        "id": self.id,
        "range": list(self.range),
        "pos": list(self.pos),
        "value": self.value,
        "size": list(self.size),
        "colors": [self.bkg_color, self.fg_color],
        "alpha": self.alpha,
    }

def _slider_deser(self, data):
    d = dict(data); d.pop("type", None)
    self.id = d.get("id", None)
    self.range = list(d.get("range", [0, 100]))
    self.init_range = list(self.range)
    self.value = d.get("value", 0)
    self.pos = list(d.get("pos", [0, 0]))
    self.size = list(d.get("size", self.size))
    self.alpha = d.get("alpha", 0)
    self.img = pygame.Surface(self.size)
    self.fg_size = [8, self.size[1]]
    self.fg_img = pygame.Surface(self.fg_size)
    self.set_colors(d.get("colors", ["blue", "aqua"]))
    self.active = False
    return self

def _vslider_deser(self, data):
    _slider_deser(self, data)
    self.fg_size = [self.size[1], 8]
    self.fg_img = pygame.Surface(self.fg_size)
    self.set_colors([self.bkg_color, self.fg_color])
    return self

Slider.serialize = _slider_ser
Slider.deserialize = _slider_deser
VerticalSlider.serialize = _slider_ser
VerticalSlider.deserialize = _vslider_deser


def _label_ser(self):
    return {
        "type": type(self).__name__,
        "id": self.id,
        "text": self.text,
        "pos": list(self.pos),
        "colors": list(self.colors),
        "secondary": self.secondary_color,
        "transp": self.transp,
    }

def _label_deser(self, data):
    d = dict(data); d.pop("type", None)
    self.id = d.get("id", None)
    self.text = d.get("text", "")
    self.pos = list(d.get("pos", [0, 0]))
    self.colors = list(d.get("colors", ["blue", "aqua"]))
    self.secondary_color = d.get("secondary", "black")
    self.transp = d.get("transp", False)
    self.r_width = 2
    self.set_text(self.text)
    return self

Label.serialize = _label_ser
Label.deserialize = _label_deser


def _textbox_ser(self):
    d = _label_ser(self); d["type"] = "TextBox"
    d["limit"] = self.limit; d["w"] = self.w; d["h"] = self.h
    return d

def _textbox_deser(self, data):
    d = dict(data); d.pop("type", None)
    self.id = d.get("id", None)
    self.limit = d.get("limit", 12)
    self.w = d.get("w", 7)
    self.h = d.get("h", 16)
    self.text = d.get("text", "")
    self.pos = list(d.get("pos", [0, 0]))
    self.colors = list(d.get("colors", ["blue", "aqua"]))
    self.secondary_color = d.get("secondary", "black")
    self.transp = d.get("transp", False)
    self.r_width = 2
    self.set_text(self.text)
    return self

TextBox.serialize = _textbox_ser
TextBox.deserialize = _textbox_deser


def _button_ser(self):
    d = {
        "type": type(self).__name__,
        "id": self.id,
        "pos": list(self.pos),
        "color": self.color,
        "size": list(self.size),
        "active": self.active,
    }
    if isinstance(self.text, str):
        d["text"] = self.text
    return d

def _button_deser(self, data):
    d = dict(data); d.pop("type", None)
    self.id = d.get("id", None)
    self.pos = list(d.get("pos", [0, 0]))
    self.size = list(d.get("size", self.size))
    self.active = d.get("active", False)
    self.color = d.get("color", "aqua")
    self.surf = pygame.Surface(self.size)
    self.set_color(self.color)
    self.text = d.get("text", "")
    self.icon = pygame.Surface(self.size)
    self.has_icon = False
    self.bkg = ""
    return self

Button.serialize = _button_ser
Button.deserialize = _button_deser
RectedButton.serialize = _button_ser
RectedButton.deserialize = _button_deser


def _button2_ser(self):
    return {
        "type": "Button2",
        "id": self.id,
        "txt": self.txt,
        "pos": list(self.pos),
        "padding": list(self.padding),
        "colors": [self.text_color, self.color],
        "active": self.active,
    }

def _button2_deser(self, data):
    d = dict(data); d.pop("type", None)
    self.id = d.get("id", None)
    self.txt = d.get("txt", d.get("text", "Button2"))
    self.pos = list(d.get("pos", [0, 0]))
    self.padding = list(d.get("padding", [8, 1]))
    colors = d.get("colors", ["aqua", "yellow"])
    self.text_color = colors[0]
    self.color = colors[1]
    self.text = self.font.render(self.txt, False, self.text_color)
    self.size = [self.text.get_width() + self.padding[0] * 2,
                 self.text.get_height() + self.padding[1] * 2]
    self.surf = pygame.Surface(self.size)
    self.surf.fill("black")
    self.surf.set_colorkey("black")
    self.active = d.get("active", False)
    return self

Button2.serialize = _button2_ser
Button2.deserialize = _button2_deser


def _table_ser(self):
    return {
        "type": type(self).__name__,
        "id": self.id,
        "pos": list(self.pos),
        "columns": self.columns,
        "rows": self.rows,
        "font_color": self.font_color,
        "color": self.color,
        "text_items": dict(self.text_items),
        "biggest": self.biggest,
    }

def _table_fill(self, d):
    self.id = d.get("id", None)
    self.pos = list(d.get("pos", [0, 0]))
    self.columns = d.get("columns", 2)
    self.rows = d.get("rows", 2)
    self.font_color = d.get("font_color", "aqua")
    self.color = d.get("color", "blue")
    self.text_items = dict(d.get("text_items", {}))
    for c in range(self.columns):
        for r in range(self.rows):
            self.text_items.setdefault(f"{c};{r}", "...")
    self.items = {k: self.font.render(v, False, self.font_color)
                  for k, v in self.text_items.items()}
    self.biggest = d.get("biggest", "0;0")
    self.draw_onto_surf()

def _table_deser(self, data):
    d = dict(data); d.pop("type", None)
    _table_fill(self, d)
    return self

Table.serialize = _table_ser
Table.deserialize = _table_deser


def _ctable_ser(self):
    d = _table_ser(self); d["type"] = "Custom_Table"
    d["size"] = list(self.size)
    return d

def _ctable_deser(self, data):
    d = dict(data); d.pop("type", None)
    self.size = list(d.get("size", self.size))
    _table_fill(self, d)
    return self

Custom_Table.serialize = _ctable_ser
Custom_Table.deserialize = _ctable_deser


def _dialog_ser(self):
    return {
        "type": "Dialog",
        "id": self.id,
        "text": self.text,
        "pos": list(self.pos),
        "size": list(self.size),
        "colors": list(self.colors),
        "rate": self.rate,
    }

def _dialog_deser(self, data):
    d = dict(data); d.pop("type", None)
    self.id = d.get("id", None)
    self.text = d.get("text", "")
    self.pos = list(d.get("pos", [0, 0]))
    self.size = list(d.get("size", self.size))
    self.colors = list(d.get("colors", ["aqua", "blue"]))
    self.rate = d.get("rate", 2)
    self.now_size = [5, self.size[1]]
    self.done = False
    self.active = False
    return self

Dialog.serialize = _dialog_ser
Dialog.deserialize = _dialog_deser


def _titlebar_ser(self):
    return {"type": "TitleBar", "id": self.id, "text": self.text,
            "colors": [self.surf_color, self.text_color]}

def _titlebar_deser(self, data):
    d = dict(data); d.pop("type", None)
    self.id = d.get("id", None)
    self.text = d.get("text", self.text)
    self.set_color(d.get("colors", [self.surf_color, self.text_color]))
    return self

TitleBar.serialize = _titlebar_ser
TitleBar.deserialize = _titlebar_deser


def _dummy_ser(self):
    d = {
        "type": self.type or "widget",
        "id": self.id,
        "pos": list(self.pos),
        "size": list(self.size),
        "color": self.color,
    }
    for k, v in getattr(self, "params", {}).items():
        d[k] = v
    return d

def _dummy_deser(self, data):
    d = dict(data)
    self.type = d.pop("type", "widget")
    self.id = d.pop("id", None)
    self.pos = list(d.pop("pos", [0, 0]))
    self.size = list(d.pop("size", [16, 16]))
    self.color = d.pop("color", "aqua")
    self.surf = pygame.Surface(self.size)
    self.surf.fill(self.color)
    self.params = d
    self.active = False
    return self

Dummy.serialize = _dummy_ser
Dummy.deserialize = _dummy_deser


# ============================================================
# ================ NEW WIDGETS (serde baked in) ==============
# ============================================================

class Checkbox:
    def __init__(self, pos, label="", checked=False, size=[12, 12],
                 colors=["aqua", "blue", "black"], font=None):
        self.id = None
        self.pos = list(pos)
        self.label = label
        self.checked = bool(checked)
        self.size = list(size)
        self.colors = list(colors)
        self.font = font
        self.surf = pygame.Surface(self.size)
        self.surf.set_colorkey("black")
        self.active = False

    def get_rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def set_checked(self, v):
        self.checked = bool(v)

    def draw(self, surf, offset=[0, 0]):
        self.surf.fill("black")
        pygame.draw.rect(self.surf, self.colors[0], [0, 0, self.size[0], self.size[1]], 2)
        if self.checked:
            pygame.draw.rect(self.surf, self.colors[1],
                             [2, 2, self.size[0] - 4, self.size[1] - 4])
        surf.blit(self.surf, [self.pos[0] - offset[0], self.pos[1] - offset[1]])
        if self.label and self.font:
            txt = self.font.render(self.label, False, self.colors[0])
            surf.blit(txt, [self.pos[0] + self.size[0] + 4 - offset[0],
                            self.pos[1] + self.size[1] // 2 - txt.get_height() // 2 - offset[1]])

    def update(self, surf, offset=[0, 0]):
        self.draw(surf, offset)

    def serialize(self):
        return {"type": "Checkbox", "id": self.id, "pos": list(self.pos),
                "label": self.label, "checked": self.checked,
                "size": list(self.size), "colors": list(self.colors)}

    def deserialize(self, data):
        d = dict(data); d.pop("type", None)
        self.id = d.get("id", None)
        self.pos = list(d.get("pos", [0, 0]))
        self.label = d.get("label", "")
        self.checked = bool(d.get("checked", False))
        self.size = list(d.get("size", [12, 12]))
        self.colors = list(d.get("colors", ["aqua", "blue", "black"]))
        self.surf = pygame.Surface(self.size); self.surf.set_colorkey("black")
        self.active = False
        return self


class ProgressBar:
    def __init__(self, pos, size=[64, 8], value=0, max_value=100,
                 colors=["blue", "aqua"]):
        self.id = None
        self.pos = list(pos)
        self.size = list(size)
        self.value = value
        self.max_value = max_value or 1
        self.colors = list(colors)
        self.active = False

    def get_rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def set_value(self, v):
        self.value = v

    def draw(self, surf, offset=[0, 0]):
        pygame.draw.rect(surf, self.colors[0],
                         [self.pos[0] - offset[0], self.pos[1] - offset[1],
                          self.size[0], self.size[1]])
        ratio = max(0.0, min(1.0, self.value / self.max_value))
        pygame.draw.rect(surf, self.colors[1],
                         [self.pos[0] - offset[0], self.pos[1] - offset[1],
                          int(self.size[0] * ratio), self.size[1]])

    def update(self, surf, offset=[0, 0]):
        self.draw(surf, offset)

    def serialize(self):
        return {"type": "ProgressBar", "id": self.id, "pos": list(self.pos),
                "size": list(self.size), "value": self.value,
                "max_value": self.max_value, "colors": list(self.colors)}

    def deserialize(self, data):
        d = dict(data); d.pop("type", None)
        self.id = d.get("id", None)
        self.pos = list(d.get("pos", [0, 0]))
        self.size = list(d.get("size", [64, 8]))
        self.value = d.get("value", 0)
        self.max_value = d.get("max_value", 100) or 1
        self.colors = list(d.get("colors", ["blue", "aqua"]))
        self.active = False
        return self


class ToggleSwitch:
    def __init__(self, pos, size=[24, 12], state=False, colors=["blue", "aqua"]):
        self.id = None
        self.pos = list(pos)
        self.size = list(size)
        self.state = bool(state)
        self.colors = list(colors)
        self.active = False

    def get_rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def toggle(self):
        self.state = not self.state

    def draw(self, surf, offset=[0, 0]):
        x, y = self.pos[0] - offset[0], self.pos[1] - offset[1]
        pygame.draw.rect(surf, self.colors[0], [x, y, self.size[0], self.size[1]], 2, 4)
        knob_w = self.size[0] // 2 - 2
        knob_x = x + (self.size[0] - knob_w - 2 if self.state else 2)
        pygame.draw.rect(surf, self.colors[1], [knob_x, y + 2, knob_w, self.size[1] - 4], 0, 3)

    def update(self, surf, offset=[0, 0]):
        self.draw(surf, offset)

    def serialize(self):
        return {"type": "ToggleSwitch", "id": self.id, "pos": list(self.pos),
                "size": list(self.size), "state": self.state,
                "colors": list(self.colors)}

    def deserialize(self, data):
        d = dict(data); d.pop("type", None)
        self.id = d.get("id", None)
        self.pos = list(d.get("pos", [0, 0]))
        self.size = list(d.get("size", [24, 12]))
        self.state = bool(d.get("state", False))
        self.colors = list(d.get("colors", ["blue", "aqua"]))
        self.active = False
        return self


class ImageWidget:
    def __init__(self, pos, image_path="", size=None, scale=True):
        self.id = None
        self.pos = list(pos)
        self.image_path = image_path
        self.size = list(size) if size else None
        self.scale = scale
        self.image = None
        self.active = False
        if image_path:
            self._load()

    def _load(self):
        try:
            self.image = pygame.image.load(self.image_path).convert_alpha()
            if self.scale and self.size:
                self.image = pygame.transform.scale(self.image, self.size)
            elif self.size is None:
                self.size = list(self.image.get_size())
        except Exception:
            self.image = None

    def get_rect(self):
        w, h = self.size if self.size else (0, 0)
        return pygame.Rect(self.pos[0], self.pos[1], w, h)

    def draw(self, surf, offset=[0, 0]):
        if self.image:
            surf.blit(self.image, [self.pos[0] - offset[0], self.pos[1] - offset[1]])
        else:
            r = self.get_rect()
            pygame.draw.rect(surf, "magenta",
                             [r.x - offset[0], r.y - offset[1], r.w, r.h], 1)

    def update(self, surf, offset=[0, 0]):
        self.draw(surf, offset)

    def serialize(self):
        return {"type": "ImageWidget", "id": self.id, "pos": list(self.pos),
                "image_path": self.image_path,
                "size": list(self.size) if self.size else None,
                "scale": self.scale}

    def deserialize(self, data):
        d = dict(data); d.pop("type", None)
        self.id = d.get("id", None)
        self.pos = list(d.get("pos", [0, 0]))
        self.image_path = d.get("image_path", "")
        self.size = list(d["size"]) if d.get("size") else None
        self.scale = d.get("scale", True)
        self.active = False
        self.image = None
        if self.image_path:
            self._load()
        return self


class Panel:
    def __init__(self, pos, size=[64, 32], color="blue",
                 border_color=None, border=0):
        self.id = None
        self.pos = list(pos)
        self.size = list(size)
        self.color = color
        self.border_color = border_color
        self.border = border
        self.active = False

    def get_rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def draw(self, surf, offset=[0, 0]):
        r = [self.pos[0] - offset[0], self.pos[1] - offset[1],
             self.size[0], self.size[1]]
        if self.border == 0:
            surf.fill(self.color, r)
        else:
            pygame.draw.rect(surf, self.border_color or self.color, r, self.border)

    def update(self, surf, offset=[0, 0]):
        self.draw(surf, offset)

    def serialize(self):
        return {"type": "Panel", "id": self.id, "pos": list(self.pos),
                "size": list(self.size), "color": self.color,
                "border_color": self.border_color, "border": self.border}

    def deserialize(self, data):
        d = dict(data); d.pop("type", None)
        self.id = d.get("id", None)
        self.pos = list(d.get("pos", [0, 0]))
        self.size = list(d.get("size", [64, 32]))
        self.color = d.get("color", "blue")
        self.border_color = d.get("border_color", None)
        self.border = d.get("border", 0)
        self.active = False
        return self


class Dropdown:
    def __init__(self, pos, options=None, selected=0, size=[64, 14],
                 colors=["blue", "aqua", "black"], font=None):
        self.id = None
        self.pos = list(pos)
        self.options = list(options) if options else ["Option A", "Option B", "Option C"]
        self.selected = selected
        self.size = list(size)
        self.colors = list(colors)
        self.font = font
        self.open = False
        self.active = False

    def get_rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def current(self):
        if 0 <= self.selected < len(self.options):
            return self.options[self.selected]
        return ""

    def draw(self, surf, offset=[0, 0]):
        x, y = self.pos[0] - offset[0], self.pos[1] - offset[1]
        pygame.draw.rect(surf, self.colors[0], [x, y, self.size[0], self.size[1]])
        if self.font:
            txt = self.font.render(self.current(), False, self.colors[1])
            surf.blit(txt, [x + 4, y + 2])
        if self.open:
            for i, opt in enumerate(self.options):
                ry = y + self.size[1] * (i + 1)
                pygame.draw.rect(surf, self.colors[2],
                                 [x, ry, self.size[0], self.size[1]])
                if self.font:
                    t = self.font.render(opt, False, self.colors[1])
                    surf.blit(t, [x + 4, ry + 2])

    def update(self, surf, offset=[0, 0]):
        self.draw(surf, offset)

    def serialize(self):
        return {"type": "Dropdown", "id": self.id, "pos": list(self.pos),
                "options": list(self.options), "selected": self.selected,
                "size": list(self.size), "colors": list(self.colors)}

    def deserialize(self, data):
        d = dict(data); d.pop("type", None)
        self.id = d.get("id", None)
        self.pos = list(d.get("pos", [0, 0]))
        self.options = list(d.get("options", ["Option A", "Option B", "Option C"]))
        self.selected = d.get("selected", 0)
        self.size = list(d.get("size", [64, 14]))
        self.colors = list(d.get("colors", ["blue", "aqua", "black"]))
        self.open = False
        self.active = False
        return self


# ============================================================
# ======================= TOOLBAR ============================
# ============================================================
#
# A horizontally scrollable strip that holds other widgets.
# Type-aware drawing and input (see _draw_widget_in_toolbar
# and _handle_widget_click below).
#
# Enable / disable at runtime:
#   bar.toggle()          -> flips enabled, returns new state
#   bar.enable()          -> sets enabled = True
#   bar.disable()         -> sets enabled = False
#   bar.is_enabled()      -> bool
#
# While disabled:
#   - update() does nothing (no draw, no input)
#   - handle_event() returns False and consumes nothing
#   - scroll position and widget states are preserved
# ============================================================


def _widget_size(w):
    """Best-effort natural size for any widget."""
    if hasattr(w, "size") and w.size:
        return list(w.size)
    if hasattr(w, "surf"):
        return list(w.surf.get_size())
    if hasattr(w, "get_rect"):
        r = w.get_rect()
        return [r.width, r.height]
    return [16, 16]


def _draw_widget_in_toolbar(widget, surf, scroll_x):
    """Draw a widget into a toolbar surface. Type-aware."""
    t = type(widget).__name__
    offset = [scroll_x, 0]

    if t in ("Label", "TextBox", "ImageWidget", "Panel",
             "ProgressBar", "Table", "Custom_Table"):
        widget.draw(surf, offset)
    elif t in ("Button", "RectedButton"):
        widget.draw(surf, offset)
    elif t == "Button2":
        widget.rected()
        widget.draw(surf, offset)
    elif t in ("Slider", "VerticalSlider"):
        widget.update3(surf, offset)
    elif t == "Dialog":
        if widget.active:
            widget.update(surf, offset)
        else:
            widget.draw(surf, offset)
    elif t == "Checkbox":
        widget.draw(surf, offset)
    elif t == "ToggleSwitch":
        widget.draw(surf, offset)
    elif t == "Dropdown":
        widget.draw(surf, offset)
    elif t == "TitleBar":
        # TitleBar draws to its own self.display normally.
        # Inside a toolbar we blit its surface directly.
        surf.blit(widget.surf, [widget.pos[0] - scroll_x, widget.pos[1]])
    else:
        if hasattr(widget, "draw"):
            try:
                widget.draw(surf, offset)
            except TypeError:
                widget.draw()


def _handle_widget_click(widget, local_pos):
    """Returns True if the widget consumed the click at local_pos
    (toolbar-local, scroll already applied)."""
    t = type(widget).__name__

    if t in ("Button", "RectedButton", "Button2"):
        if widget.get_rect().collidepoint(local_pos):
            widget.set_state()
            return True

    elif t == "Checkbox":
        if widget.get_rect().collidepoint(local_pos):
            widget.checked = not widget.checked
            return True

    elif t == "ToggleSwitch":
        if widget.get_rect().collidepoint(local_pos):
            widget.toggle()
            return True

    elif t in ("Slider", "VerticalSlider"):
        if widget.get_rects()[0].collidepoint(local_pos):
            widget.active = True
            return True

    elif t == "Dropdown":
        rect = widget.get_rect()
        if rect.collidepoint(local_pos):
            widget.open = not widget.open
            return True
        if widget.open:
            for i in range(len(widget.options)):
                opt_rect = pygame.Rect(
                    rect.x, rect.y + widget.size[1] * (i + 1),
                    widget.size[0], widget.size[1])
                if opt_rect.collidepoint(local_pos):
                    widget.selected = i
                    widget.open = False
                    return True

    return False


class Toolbar:
    def __init__(self, pos, size, font=None,
                 bkg="black", border_color="aqua",
                 padding=4, spacing=4, scroll_speed=8,
                 show_scrollbar=True, wheel_speed=20, enabled=True):
        self.id = None
        self.pos = list(pos)
        self.size = list(size)
        self.font = font
        self.bkg = bkg
        self.border_color = border_color
        self.padding = padding
        self.spacing = spacing
        self.scroll_speed = scroll_speed
        self.wheel_speed = wheel_speed
        self.show_scrollbar = show_scrollbar
        self.widgets = []
        self.scroll = 0
        self.max_scroll = 0
        self.content_width = 0
        self.active = False
        self.enabled = bool(enabled)
        self.surf = pygame.Surface(self.size)

    # ---------- enable / disable ----------
    def enable(self):
        self.enabled = True
        return self.enabled

    def disable(self):
        self.enabled = False
        return self.enabled

    def toggle(self):
        self.enabled = not self.enabled
        return self.enabled

    def is_enabled(self):
        return self.enabled

    # ---------- management ----------
    def add(self, widget, id=None):
        if id is not None:
            widget.id = id
        elif not getattr(widget, "id", None):
            widget.id = f"w{len(self.widgets)}"
        self.widgets.append(widget)
        self._layout()
        return widget

    def remove(self, id):
        self.widgets = [w for w in self.widgets if getattr(w, "id", None) != id]
        self._layout()

    def get(self, id):
        for w in self.widgets:
            if getattr(w, "id", None) == id:
                return w
        return None

    def clear(self):
        self.widgets = []
        self._layout()

    def _layout(self):
        """Place widgets left-to-right inside the toolbar and compute scroll bounds."""
        bar_h = self.size[1]
        if self.show_scrollbar:
            bar_h -= 6
        cursor = self.padding
        for w in self.widgets:
            ws = _widget_size(w)
            w.pos = [cursor, max(self.padding, (bar_h - ws[1]) // 2)]
            cursor += ws[0] + self.spacing
        self.content_width = cursor + self.padding
        self.max_scroll = max(0, self.content_width - self.size[0])
        self.scroll = max(0, min(self.scroll, self.max_scroll))

    # ---------- input ----------
    def handle_event(self, event, offset=[0, 0]):
        """Call for each pygame event. Returns True if consumed.
        Does nothing and returns False while disabled."""
        if not self.enabled:
            return False

        if event.type == pygame.MOUSEWHEEL:
            mp = pygame.mouse.get_pos()
            local_x = mp[0] - self.pos[0] + offset[0]
            local_y = mp[1] - self.pos[1] + offset[1]
            if 0 <= local_x < self.size[0] and 0 <= local_y < self.size[1]:
                self.scroll -= event.y * self.wheel_speed
                self.scroll = max(0, min(self.scroll, self.max_scroll))
                return True

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    if event.key == pygame.K_LEFT:
                        self.scroll -= self.scroll_speed
                    else:
                        self.scroll += self.scroll_speed
                    self.scroll = max(0, min(self.scroll, self.max_scroll))
                    return True
            if event.key == pygame.K_HOME:
                self.scroll = 0
                return True
            if event.key == pygame.K_END:
                self.scroll = self.max_scroll
                return True

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mp = pygame.mouse.get_pos()
            local_x = mp[0] - self.pos[0] + offset[0]
            local_y = mp[1] - self.pos[1] + offset[1]
            if 0 <= local_x < self.size[0] and 0 <= local_y < self.size[1]:
                content_pos = [local_x + self.scroll, local_y]
                # dispatch in reverse so top-most (last added) wins
                for w in reversed(self.widgets):
                    if _handle_widget_click(w, content_pos):
                        return True

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            for w in self.widgets:
                if isinstance(w, Slider):
                    w.active = False

        if event.type == pygame.MOUSEMOTION:
            mp = pygame.mouse.get_pos()
            local_x = mp[0] - self.pos[0] + offset[0]
            local_y = mp[1] - self.pos[1] + offset[1]
            content_x = local_x + self.scroll
            for w in self.widgets:
                if isinstance(w, (Slider, VerticalSlider)) and w.active:
                    rect = w.get_rects()[0]
                    if rect.collidepoint([content_x, local_y]):
                        try:
                            if isinstance(w, VerticalSlider):
                                w.set_value([content_x, int(
                                    (local_y - w.pos[1]) / max(1, w.size[1])
                                    * (w.range[1] - w.range[0]))])
                            else:
                                w.set_value([int(
                                    (content_x - w.pos[0]) / max(1, w.size[0])
                                    * (w.range[1] - w.range[0])), local_y])
                        except Exception:
                            pass

        return False

    def update(self, surf, offset=[0, 0], events=None):
        """Draw the toolbar onto surf at self.pos - offset.
        Pass events to handle input in one call.
        Does nothing while disabled."""
        if not self.enabled:
            return

        # clamp scroll
        self.scroll = max(0, min(self.scroll, self.max_scroll))

        # handle events
        if events:
            for e in events:
                self.handle_event(e, offset)

        # background
        self.surf.fill(self.bkg)
        pygame.draw.rect(self.surf, self.border_color,
                         [0, 0, self.size[0], self.size[1]], 1)

        # clip so scrolling widgets don't bleed
        old_clip = self.surf.get_clip()
        self.surf.set_clip(pygame.Rect(1, 1, self.size[0] - 2, self.size[1] - 2))

        for w in self.widgets:
            _draw_widget_in_toolbar(w, self.surf, self.scroll)

        self.surf.set_clip(old_clip)

        # scrollbar
        if self.show_scrollbar and self.max_scroll > 0:
            self._draw_scrollbar()

        # blit onto screen
        surf.blit(self.surf, [self.pos[0] - offset[0], self.pos[1] - offset[1]])

    def _draw_scrollbar(self):
        bar_h = 4
        bar_y = self.size[1] - bar_h - 1
        track = pygame.Rect(self.padding, bar_y,
                            self.size[0] - 2 * self.padding, bar_h)
        pygame.draw.rect(self.surf, "gray", track)
        ratio = self.size[0] / max(1, self.content_width)
        handle_w = max(12, int(track.width * ratio))
        if self.max_scroll > 0:
            t = self.scroll / self.max_scroll
            handle_x = track.x + int((track.width - handle_w) * t)
            handle = pygame.Rect(handle_x, bar_y, handle_w, bar_h)
            pygame.draw.rect(self.surf, self.border_color, handle)


# ============================================================
# ================== REGISTER EVERYTHING =====================
# ============================================================

register_type("widget.Label",          "scripts.widgets:Label")
register_type("widget.TextBox",        "scripts.widgets:TextBox")
register_type("widget.Button",         "scripts.widgets:Button")
register_type("widget.RectedButton",   "scripts.widgets:RectedButton")
register_type("widget.Button2",        "scripts.widgets:Button2")
register_type("widget.Slider",         "scripts.widgets:Slider")
register_type("widget.VerticalSlider", "scripts.widgets:VerticalSlider")
register_type("widget.Table",          "scripts.widgets:Table")
register_type("widget.Custom_Table",   "scripts.widgets:Custom_Table")
register_type("widget.Dialog",         "scripts.widgets:Dialog")
register_type("widget.TitleBar",       "scripts.widgets:TitleBar")
register_type("widget.Dummy",          "scripts.widgets:Dummy")

register_type("widget.Checkbox",     "scripts.widgets:Checkbox")
register_type("widget.ProgressBar",  "scripts.widgets:ProgressBar")
register_type("widget.ToggleSwitch", "scripts.widgets:ToggleSwitch")
register_type("widget.ImageWidget",  "scripts.widgets:ImageWidget")
register_type("widget.Panel",        "scripts.widgets:Panel")
register_type("widget.Dropdown",     "scripts.widgets:Dropdown")

register_type("widget.Toolbar",      "scripts.widgets:Toolbar")