import pygame
import sys
import os 
import json

from scripts.utils import draw_rect, organise_poses, add_lists, multiply_lists, scroll_control, make_dummy_dict, Timer
from scripts.widgets import TitleBar, Dummy, text_input2, text_input, Dialog, Table



WINDOWSIZE = [640, 480]
class MenuEditor:
    def __init__(self, scale):
        pygame.init()
        self.renderscale = scale
        pygame.display.set_caption("Menu Editor")
        self.screen = pygame.display.set_mode(WINDOWSIZE)
        self.display = pygame.Surface((int(self.screen.get_width() // self.renderscale), int(self.screen.get_height() // self.renderscale)))
        self.clock = pygame.time.Clock()
        self.menus = []
        self.bkg_color = (0, 10, 30)
        self.font = pygame.font.Font("data/fonts/at01.ttf")
        self.tiled = True
        self.tilesize = 16
        self.theresActive = False
        self.grid_surface = pygame.Surface(self.screen.get_size())
        self.draw_grid(multiply_lists([self.tilesize, self.tilesize], [self.renderscale, self.renderscale]), "green")
        self.grid = True
        self.config = {}

    def draw_grid(self, size, color):
        for i in range(0, self.screen.get_height()*2, size[0]):
            pygame.draw.line(self.grid_surface, color, [i, 0], [i, int(self.screen.get_height())])
        for i in range(0, self.screen.get_width()*2, size[0]):
            pygame.draw.line(self.grid_surface, color, [0, i], [int(self.screen.get_width()), i])
        self.grid_surface.set_colorkey("black")

    def save_config(self, name):
        PATH = "data/menus/"
        f = open(f"{PATH}{name}.json", "w")
        data = {"config": self.config}
        json.dump(data, f)
        f.close()
    
    def load_config(self, name):
        PATH = "data/menus/"
        f = open(f"{PATH}{name}.json", "r")
        data = json.load(f)
        self.config = data["config"]
        f.close()

    def convert_to_config_format(self):
        ...
    
    def save(self):
        name = ""
        name = text_input2([self.display, self.screen], self.font, name, "Config Name")
        self.save_config(name)
    
    def load(self):
        name = ""
        name = text_input2([self.display, self.screen], self.font, name, "Config Name")
        self.load_config(name)

    def settings(self):
        running = True
        title_bar = TitleBar(self.font, self.display, "Settings")
        settings = {
            "tiled": self.tiled,
            "grid": self.grid
        }
        bools = {
            "false": False,
            "true": True,
            "0": False,
            "1": True
        }
        settings_table = Table(self.font, [0, 0], 2, len(settings))
        set_timer = Timer(60, 1)
        for i, setting in enumerate(settings):
            settings_table.add_item(str(setting), [0, i])
            settings_table.add_item(str(settings[setting]), [1, i])
        set_timer.done = True
        while running:
            self.display.fill(self.bkg_color)
            settings_table.draw(self.display)
            temp = settings_table.mouse_select2(0, self.renderscale)
            set_timer.update()
            if temp != "":
                if not temp[0] == "..." and not temp[0] == "":
                    if set_timer.done:
                        if temp[0] == "tiled":
                            value = ""
                            value = text_input2([self.display, self.screen], self.font, "", temp[0].upper())
                            settings_table.add_item(value, [1, temp[1][1]])
                            settings[temp[0]] = bools[value.lower()]
                            self.tiled = bools[value.lower()]
                            set_timer.start()
                        if temp[0] == "grid":
                            value = ""
                            value = text_input2([self.display, self.screen], self.font, "", temp[0].upper())
                            settings_table.add_item(value, [1, temp[1][1]])
                            settings[temp[0]] = bools[value.lower()]
                            self.grid = bools[value.lower()]
                            set_timer.start()
            title_bar.update()
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), [0, 0])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            pygame.display.flip()
            self.clock.tick(30)

    def run(self):
        running = True
        title_bar = TitleBar(self.font, self.display, "Menu Editor")
        temp = []
        name = ""
        color = ""
        tilesize = [self.tilesize, self.tilesize]
        scroll = [0, 0]
        while running:
            self.display.fill(self.bkg_color)
            for dummy in self.menus:
                dummy.draw(self.display, scroll)
            scroll_control(scroll, self.tilesize if self.grid else 4)

            if len(temp) > 1:
                if self.theresActive:
                    for dummy in self.menus:
                        if dummy.active:
                            if self.tiled:
                                info = organise_poses(multiply_lists(temp[0], tilesize), add_lists(multiply_lists(temp[1], tilesize), tilesize))
                            else:
                                info = organise_poses(temp[0], temp[1])
                            info = [[info[0][0] - dummy.pos[0], info[0][1] - dummy.pos[1]], info[1], info[2]]
                            color = text_input([self.display, self.screen], self.font, color, "Enter Color")
                            if color == "":
                                color = "red"
                            dummy.add_dummy(info[0], info[2], color)
                            dummy.active = False
                            self.theresActive = False
                            temp = []
                else:
                    if self.tiled:
                        draw_rect(multiply_lists(temp[0], tilesize), add_lists(multiply_lists(temp[1], tilesize), tilesize), self.display)
                    else:
                        draw_rect(temp[0], temp[1], self.display)
                    name = text_input2([self.display, self.screen], self.font, name, "Enter Name")
                    color = text_input2([self.display, self.screen], self.font, color, "Enter Color")
                    #print(f"colortype{type(color)} , {color}")
                    if self.tiled:
                        info = organise_poses(multiply_lists(temp[0], tilesize), add_lists(multiply_lists(temp[1], tilesize), tilesize))
                    else:
                        info = organise_poses(temp[0], temp[1])
                    dum = Dummy(info[0], info[2], color)
                    dum.get_type(name)
                    self.menus.append(dum)
                    name = ""
                    color = ""
                    temp = []
                    
            if len(temp) == 1:
                
                mouse = pygame.mouse.get_pos()
                ms = [(mouse[0] // self.renderscale), (mouse[1] // self.renderscale)]
                if self.tiled:
                    ms = [int((ms[0] + scroll[0]) // self.tilesize), int((ms[1] + scroll[1])// self.tilesize)]
                    draw_rect(multiply_lists(temp[0], tilesize), add_lists(multiply_lists(ms, tilesize), tilesize), self.display, offset=scroll)
                else:
                    ms = [(ms[0] + scroll[0]), (ms[1] + scroll[1])]
                    draw_rect(temp[0], ms, self.display, offset=scroll)

            title_bar.update()
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), [0, 0])
            if self.grid:
                self.screen.blit(self.grid_surface, [0, 0])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 3:
                        if len(temp) < 2:
                            mouse = event.pos
                            ms = [(mouse[0] // self.renderscale), (mouse[1] // self.renderscale)]
                            if self.tiled:
                                ms = [int((ms[0] + scroll[0]) // self.tilesize), int((ms[1] + scroll[1])// self.tilesize)]
                            else:
                                ms = [(ms[0] + scroll[0]), (ms[1] + scroll[1])]
                            if len(temp) == 0 or len(temp) == 1:
                                for dummy in self.menus:
                                    if self.tiled:
                                        if dummy.get_rect().collidepoint(multiply_lists(ms, tilesize)):
                                            if not self.theresActive:
                                                dummy.active = True
                                                self.theresActive = True
                                    else:
                                        if dummy.get_rect().collidepoint(ms):
                                            if not self.theresActive:
                                                dummy.active = True
                                                self.theresActive = True
                            temp.append(ms)
                        elif len(temp) == 2:
                            mouse = event.pos
                            ms = [(mouse[0] // self.renderscale), (mouse[1] // self.renderscale)]
                            if self.tiled:
                                ms = [int((ms[0] + scroll[0]) // self.tilesize), int((ms[1] + scroll[1]) // self.tilesize)]
                            else:
                                ms = [(ms[0] + scroll[0]), (ms[1] + scroll[1])]
                            temp[1] = ms

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_KP_PLUS:
                        dict_menus = []
                        dict_menus = make_dummy_dict(self.menus, dict_menus)
                        self.config["new"] = dict_menus
                        self.save()
                    if event.key == pygame.K_KP_MINUS:
                        self.load()
                    if event.key == pygame.K_KP_MULTIPLY:
                        self.settings()


            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    MenuEditor(2).run()