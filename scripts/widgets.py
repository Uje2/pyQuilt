import pygame
import sys


class Slider:
    def __init__(self, range, pos, value=0,size=[16, 8], colors=["blue", "aqua"], alpha=0):
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
        #self.icon.blit(self.text, [int(self.size[0] // padding[0]), 1])
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
        '''for dummy in self.dummies:
            self.surf.blit(dummy.surf, [0,0])'''
        surf.blit(self.surf, [self.pos[0] - offset[0], self.pos[1] - offset[1]])

    def get_type(self, typee):
        self.type = typee