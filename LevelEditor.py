import pygame
import sys
import os
import json

from scripts.utils import load_image, extract_image, join, draw_rect, multiply_lists, add_lists, scroll_control,Timer, load_images, load_image2, load_loadable_images, get_game_assets, get_the_other_assets
from scripts.tilemap import Tilemp
from scripts.widgets import TitleBar, Table, Dialog, text_input, Custom_Table, text_input2

class LevelEditor:
    def __init__(self):
        self.render_scale = 2

        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        self.clock = pygame.time.Clock()
        self.display = pygame.Surface((int(self.screen.get_width() // self.render_scale), int(self.screen.get_height() // self.render_scale)))
        self.assets = {}
        self.savable_assets = {}
        self.asset_path = ""
        self.dt = 0.1
        self.font = pygame.font.Font("data/fonts/at01.ttf")
        self.scroll = [0, 0]
        self.loaded = False
        self.image = None
        self.tilesize = [16, 16]
        self.types = []
        self.type_index = 0
        self.type = self.types[self.type_index] if self.loaded else []
        self.current_index = 0
        self.current = self.assets[self.type] if self.loaded else []
        self.level = Tilemp(self, self.tilesize)
        self.level.physics = {"grass", "sand"}
        self.path = ""
        self.current_layer = 0
        self.used = []
        self.bkg_color = (0, 10, 30)
        self.other_assets = {}
    
    def load_assets(self):
        runn = True
        title_bar = TitleBar(self.font, self.display, "Asset Loader")
        path = "data/images/spritesheets"
        images = {}
        for i, image in enumerate(os.listdir(path=path)):
            images[image] = {"path": path + "/"+ image, "font": self.font.render(image, False, "blue"), "rect": pygame.Rect(50, (i + 1) * 25, 100, 30)}

        while runn:
            self.dt = self.clock.tick(60) / 1000
            self.display.fill((0, 10, 30))
            mclick = pygame.mouse.get_pressed()
            if self.loaded:
                self.display.blit(self.image, [0-self.scroll[0], 0-self.scroll[1]])
            for image in images:
                i = images[image]
                self.display.blit(i["font"], i["rect"])
                if mclick[0]:
                    mpos = pygame.mouse.get_pos()
                    mpos = [int(mpos[0] // self.render_scale), int(mpos[1] // self.render_scale)]
                    if i["rect"].collidepoint(mpos):
                        if os.path.exists(i["path"]):
                            self.asset_path = i["path"]
                            self.image = load_image(i["path"])
                            self.path = self.asset_path
                            self.loaded = True
                            
            title_bar.update()
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        runn = False
                    if event.key == pygame.K_e:
                        self.extract_assets()
            pygame.display.update()
    def load_json_file(self, path):
        f = open(path, "r")
        data = json.load(f)
        f.close()
        return data

    def help_menu(self):
        rrun = True
        title_bar = TitleBar(self.font, self.display, "Help")
        scroll = [0, 0]
        help = self.load_json_file("data/settings/help.json")
        tables: Table = []
        for setting in help:
            table = Table(self.font, [0, 0], 2, len(help[setting]) + 1)
            table.add_item(setting, [0, 0])
            for i, settin in enumerate(help[setting]):
                value = help[setting][settin]
                table.add_item(settin, [0, i + 1])
                table.add_item(value, [1, i + 1])
            tables.append(table)
        for i, table in enumerate(tables):
            if i != 0:
                prev_table = tables[i-1]
                prev_rect = prev_table.get_rect()
                table.set_table_pos(prev_rect.bottomleft)
            table.make_table_transparent()
            table.set_row_font_color(0, "orange")
            table.set_column_font_color(1, "green")
            
        
        
        while rrun:
            self.display.fill((0, 10, 30))
            
            for table in tables:
                table.draw(self.display, scroll)
                    
            title_bar.update()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                scroll[1] += -5
            if keys[pygame.K_DOWN]:
                scroll[1] += 5
            if keys[pygame.K_LEFT]:
                scroll[0] += -5
            if keys[pygame.K_RIGHT]:
                scroll[0] += 5
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        rrun = False
            pygame.display.flip()
            self.clock.tick(60)

    def get_asset(self):
        running = True
        title_bar = TitleBar(self.font, self.display, "Asset Importer")
        load_text = self.font.render("LOAD", False, "green")
        loadbtn = pygame.Surface((40, 20))
        loadbtn.fill("yellow")
        loadrect = loadbtn.get_rect(center=[160, 200])
        texting = True
        loaded = False
        image = None
        
        
        while running:
            self.dt = self.clock.tick(60) / 1000
            asset_path = self.font.render(self.asset_path, None, "aqua")
            self.display.fill((0, 10, 30))
            self.display.blit(asset_path, [160 - len(self.asset_path) *3, 120])
            title_bar.update()
            self.display.blit(loadbtn, loadrect)
            self.display.blit(load_text, [loadrect.x + 6, loadrect.y])
            if loaded:
                self.display.blit(image, [0, 0])
                self.loaded = loaded
                self.image = image
            mclick = pygame.mouse.get_pressed()
            if mclick[0]:
                mpos = pygame.mouse.get_pos()
                mpos = [int(mpos[0] // self.render_scale), int(mpos[1] // self.render_scale)]
                if loadrect.collidepoint(mpos):
                    texting = False
                    if os.path.exists(self.asset_path):
                        image = load_image(self.asset_path)
                        self.path = self.asset_path
                        loaded = True

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), [0, 0])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.TEXTINPUT:
                    if texting:
                        self.asset_path += event.text
                    #print(self.asset_path)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_BACKSPACE:
                        self.asset_path = self.asset_path[:-1]
                    if event.key == pygame.K_e:
                        if self.loaded:
                            self.extract_assets()
            pygame.display.update()
    def savable_image(self, lis):
        mpos = pygame.mouse.get_pos()
        mpos = [int(mpos[0] // self.render_scale), int(mpos[1] // self.render_scale)]
        tile_pos = [int((mpos[0] + self.scroll[0]) // self.tilesize[0]), int((mpos[1] + self.scroll[1])// self.tilesize[1])]
        if self.loaded:
            image = {"path": self.path, "size": self.tilesize,"pos": tile_pos}
            lis[str(tile_pos[0]) + ";" + str(tile_pos[1])] = image
    def add_image(self, lis):
        mpos = pygame.mouse.get_pos()
        mpos = [int(mpos[0] // self.render_scale), int(mpos[1] // self.render_scale)]
        tile_pos = [int((mpos[0] + self.scroll[0]) // self.tilesize[0]), int((mpos[1] + self.scroll[1])// self.tilesize[1])]
        if self.loaded:
            image = extract_image(self.image, self.tilesize, tile_pos)
            lis[str(tile_pos[0]) + ";" + str(tile_pos[1])] = image
        #self.savable_image(self.savable_assets[self.])
    
    def save_asset_path(self):
        tt = ""
        text = text_input2([self.display, self.screen], self.font, tt, "Asset FileName")
        f = open("data/extracted_data/" + text + ".json", "w")
        data = {"assets": self.savable_assets, "physics": list(self.level.physics), "tilesize": self.tilesize, "img_path": self.path, "asset_path": self.asset_path, "other_assets": self.other_assets, "blocks": list(self.level.blocks), "spawners":list(self.level.spawners)}
        json.dump(data, f)
        f.close()
    
    def save_tilemap(self, name):
        f = open(f"data/allied/{name}.json", "w")
        data = {"tilemap": self.level.tilemap, "spawners": self.level.spawners,"ongrid": self.level.ongrid, "offgrid": self.level.offgrid, "tilesize": self.tilesize, "physics": list(self.level.physics), "img_path": self.path, "assets": self.savable_assets, "imgs": self.used, "blocks": list(self.level.blocks), "phys_blocks": self.level.phys_blocks}
        pack = {}
        json.dump(data, f)
        f.close() 

    def save_map(self):
        running = True
        typing = False
        name = "map0"
        title_bar = TitleBar(self.font, self.display, "Save Map")
        save_dialog = Dialog(self.font, "Map Saved", [0, self.display.get_height() - 64], [self.display.get_width(), 32], ["red", "aqua"], 10)
        

        while running:
            name_font = self.font.render(name, False, "aqua")
            self.display.fill((0, 10, 30))
            self.display.blit(name_font, [self.display.get_width() // 2, self.display.get_height() // 2])
            if save_dialog.active:
                save_dialog.update(self.display)
            if save_dialog.done:
                save_dialog.active = False
            title_bar.update()
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        typing = True
                    if event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_TAB:
                        name = ""
                    if event.key == pygame.K_s:
                        self.save_tilemap(name)
                        save_dialog.active = True
                if event.type == pygame.TEXTINPUT:
                    if typing:
                        name += event.text
            pygame.display.update()
            self.clock.tick(60)
    
    def add_block(self):
        running = True
        typing = False
        name = "#ffffff"
        title_bar = TitleBar(self.font, self.display, "Add Block")
        add_dialog = Dialog(self.font, "Block Added", [0, self.display.get_height() - 64], [self.display.get_width(), 32], ["green", "aqua"], 5)
        

        while running:
            name_font = self.font.render(name, False, "aqua")
            self.display.fill((0, 10, 30))
            self.display.blit(name_font, [self.display.get_width() // 2, self.display.get_height() // 2])
            add_dialog.update(self.display)
            title_bar.update()
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        typing = True
                    if event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_TAB:
                        name = ""
                    if event.key == pygame.K_RETURN:
                        if name == "":
                            name = "#ffffff"
                        self.level.blocks.add(name)
                        self.assets[name] = [name, name]
                        self.types = list(self.assets)
                        self.loaded = True
                        add_dialog.active = True
                        add_dialog.reset()
                if event.type == pygame.TEXTINPUT:
                    if typing:
                        name += event.text
            pygame.display.update()
            self.clock.tick(60)


    def settings(self):
        runner = True
        title_bar = TitleBar(self.font, self.display, "Settings")
        settings = {"tilesize": self.tilesize, "more":"more", "what": 50, "test":2}
        set_rects = {}
        for i, setting in enumerate(settings):
            set_rects[setting] = pygame.Rect(50, (i + 1) * 25, 100, 30)

        while runner:
            self.display.fill((0, 10, 30))
            mclick = pygame.mouse.get_pressed()
            if mclick[0]:
                mpos = pygame.mouse.get_pos()
                mpos = [int(mpos[0] // self.render_scale), int(mpos[1] // self.render_scale)]
                for setting in set_rects:
                    rect = set_rects[setting]
                    if rect.collidepoint(mpos):
                        if setting == "tilesize":
                            next_size = [(self.tilesize[0] + 16) % 48, (self.tilesize[1] + 16) % 48]
                            if next_size == [0, 0]:
                                next_size = [16, 16]
                            self.tilesize = next_size
                            settings["tilesize"] = self.tilesize
                            self.level.tilesize = settings["tilesize"]
            for setting in settings:
                font = self.font.render(setting, False, "blue")
                font2 = self.font.render(str(settings[setting]), False, "blue")
                self.display.blit(font, set_rects[setting])
                self.display.blit(font2, set_rects[setting].topright)
            title_bar.update()
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        runner = False
            
            pygame.display.update()
            self.clock.tick(60)

    def select_assets(self):
        title = TitleBar(self.font, self.display, "Asset Selector")
        run = True
        pillars = []
        if self.loaded:
            self.types = list(self.assets).copy()
            columns = [self.font.render(typ, False, "green") for typ in self.types]
            for i in range(len(self.types)):
                lis = self.assets[self.types[i]].copy()
                #print(f'lis {lis}')
                #lis.insert(0, columns[i])
                pillars.append(lis)
        offset = [0, 0]
        spread = [4, 4]
            
        while run:
            self.display.fill(self.bkg_color)
            keys = pygame.key.get_pressed()
            scrol = 2
            if keys[pygame.K_UP]:
                offset[1] -= scrol
            if keys[pygame.K_DOWN]:
                offset[1] += scrol
            if keys[pygame.K_LEFT]:
                offset[0] -= scrol
            if keys[pygame.K_RIGHT]:
                offset[0] += scrol
            if pillars:
                for i, pillar in enumerate(pillars):
                    #pillar = pillar[:int(len(pillar) // 2)]
                    #pillar = set(pillar)
                    #pillar = list(pillar)
                    for x, img in enumerate(pillar):
                        #pos = [(i + offset[0]) * (self.tilesize[0]+ spread[0]), (x + offset[1]) * (self.tilesize[1]+ spread[1])]
                        pos = [i * (self.tilesize[0]+ spread[0]), x * (self.tilesize[1]+ spread[1])]
                        #pos = [i * (self.tilesize[0]+ offset[0] + spread[0]), x * (self.tilesize[1]+ offset[1] + spread[1])]
                        #pos = [(i * (self.tilesize[0]+ 2)) // self.render_scale, (x * (self.tilesize[1]+ 2)) // self.render_scale]
                        #rect = pygame.Rect(pos[0] , pos[1], self.tilesize[0], self.tilesize[1])
                        rect = pygame.Rect(pos[0] + offset[0] , pos[1] + offset[1], self.tilesize[0], self.tilesize[1])
                        #rect = pygame.Rect(pos[0] * self.tilesize[0], pos[1] * self.tilesize[1], self.tilesize[0], self.tilesize[1])
                        mclick = pygame.mouse.get_pressed()
                        if mclick[1]:
                            mpos = pygame.mouse.get_pos()
                            #if rect.collidepoint([int(mpos[0] // self.render_scale), int(mpos[1] // self.render_scale)]):
                            po = [int(mpos[0] // self.render_scale), int(mpos[1] // self.render_scale)]
                            if rect.collidepoint(po):
                                self.type_index = i
                                self.current_index = x 
                                run = False
                        if img not in self.level.blocks: 
                            #self.display.blit(img, [pos[0] - offset[0], pos[1]- offset[1]])
                            self.display.blit(img, [rect.x, rect.y])
                        else:
                            #pygame.draw.rect(self.display, img, [pos[0] - offset[0], pos[1]- offset[1], 16, 16], 2 if x == 1 else 0)
                            pygame.draw.rect(self.display, img, rect, 2 if x == 1 else 0)

            title.update()
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), [0, 0])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False

            pygame.display.flip()
            self.clock.tick(60)

    
    def extract_assets(self):
        running = True
        title_bar = TitleBar(self.font, self.display, "Image Extractor")
        selected = False
        
        self.images = []
        self.s_images = []
        images = {}
        savable_images = {}
        ti_sel = []
        image = None
        savable_image = None
        show_case = False
        index = 0
        texting = False
        text = ""
        selecting = False
        select = False
        add_physics_dialog = Dialog(self.font, "Added to physics", [0, self.display.get_height() - 96], [200, 32], ["green", "aqua"], 5)
        add_spawner_dialog = Dialog(self.font, "Added to Spawners", [0, self.display.get_height() - 96], [200, 32], ["green", "aqua"], 5)
        add_decor_dialog = Dialog(self.font, "Added to Decor", [0, self.display.get_height() - 64], [200, 32], ["green", "aqua"], 5)
        add_offgrid_dialog = Dialog(self.font, "Added to offgrid", [0, self.display.get_height() - 32], [200, 32], ["green", "aqua"], 5)
        add_select_dialog = Dialog(self.font, "Added to Selection", [0, self.display.get_height() - 96], [200, 32], ["green", "aqua"], 5)
        add_asset_dialog = Dialog(self.font, "Added to assets", [0, self.display.get_height() - 96], [200, 32], ["green", "aqua"], 5)
        add_images_dialog = Dialog(self.font, "Added to images", [0, self.display.get_height() - 96], [200, 32], ["green", "aqua"], 5)
        while running:
            self.dt = self.clock.tick(60) / 1000
            asset_path = self.font.render(self.asset_path, None, "aqua")
            self.display.fill((0, 10, 30))
            if self.loaded and not show_case:
                self.display.blit(self.image, [0-self.scroll[0], 0-self.scroll[1]])
            elif show_case:
                index = (index + 0.01) % len(self.images)
                self.display.blit(self.images[int(index)], [160-self.scroll[0], 200-self.scroll[1]])
            if selecting:
                if not select:
                    mpos = pygame.mouse.get_pos()
                    mpos = [int(mpos[0] // self.render_scale), int(mpos[1] // self.render_scale)]
                    tile_pos = [int((mpos[0] + self.scroll[0]) // self.tilesize[0]), int((mpos[1] + self.scroll[1])// self.tilesize[1])]
                    draw_rect(multiply_lists(ti_sel[0], self.tilesize), add_lists(multiply_lists(tile_pos, self.tilesize), self.tilesize), self.display, offset=self.scroll)
                else:
                    draw_rect(multiply_lists(ti_sel[0], self.tilesize), add_lists(multiply_lists(ti_sel[1], self.tilesize), self.tilesize), self.display, "blue", offset=self.scroll)
            add_spawner_dialog.update(self.display)
            add_physics_dialog.update(self.display)
            add_offgrid_dialog.update(self.display)
            add_decor_dialog.update(self.display)
            add_select_dialog.update(self.display)
            add_asset_dialog.update(self.display)
            add_images_dialog.update(self.display)
            title_bar.update()
            if images:
                selected = True
            else:
                selected = False
            mclick = pygame.mouse.get_pressed()
            if mclick[0]:
                self.add_image(images)
                self.savable_image(savable_images)
                    
            if mclick[2]:
                mpos = pygame.mouse.get_pos()
                mpos = [int(mpos[0] // self.render_scale), int(mpos[1] // self.render_scale)]
                tile_pos = [int((mpos[0] + self.scroll[0]) // self.tilesize[0]), int((mpos[1] + self.scroll[1])// self.tilesize[1])]
                if self.loaded:
                    if len(ti_sel) < 2:
                        if not tile_pos in ti_sel:
                            ti_sel.append(tile_pos)
                            selecting = True
                    elif len(ti_sel) == 2:
                        ti_sel[1] = tile_pos
                        select = True
            key = pygame.key.get_pressed()
            if key[pygame.K_UP]:
                self.scroll[1] -= 4
            if key [pygame.K_DOWN]:
                self.scroll[1] += 4
            if key [pygame.K_LEFT]:
                self.scroll[0] -= 4
            if key [pygame.K_RIGHT]:
                self.scroll[0] += 4
            mpos = pygame.mouse.get_pos()
            mpos = [int(mpos[0] // self.render_scale), int(mpos[1] // self.render_scale)]
            mpfont = self.font.render(f"{mpos}", False, "white")
            text_font = self.font.render(text, False, "aqua")
            
            self.display.blit(mpfont, [250, 5])
            self.display.blit(text_font, [160- len(text) * 3 , 120])
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), [0, 0])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                '''
                if event.type == pygame.TEXTINPUT:
                    self.asset_path += event.text
                    #print(self.asset_path)
                '''
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_BACKSPACE:
                        self.asset_path = self.asset_path[:-1]
                
                    if event.key == pygame.K_s:
                        if selected:
                            for key in images:
                                self.images.append(images[key])
                            images = {}
                            for key in savable_images:
                                self.s_images.append(savable_images[key])
                            savable_images = {}
                            add_images_dialog.active = True
                            add_images_dialog.reset()
                    if event.key == pygame.K_c:
                        show_case = True
                        self.scroll = [0, 0]
                    if event.key == pygame.K_x:
                        mpos = pygame.mouse.get_pos()
                        mpos = [int(mpos[0] // self.render_scale), int(mpos[1] // self.render_scale)]
                        tile_pos = [int((mpos[0] + self.scroll[0]) // self.tilesize[0]), int((mpos[1] + self.scroll[1])// self.tilesize[1])]
                        if len(ti_sel) > 1:
                            for x in range(min(ti_sel[0][0], ti_sel[1][0]), max(ti_sel[0][0], ti_sel[1][0]) + 1):
                                for y in range(min(ti_sel[0][1], ti_sel[1][1]), max(ti_sel[0][1], ti_sel[1][1]) + 1):
                                    if self.loaded:
                                        image = extract_image(self.image, self.tilesize, [x, y])
                                        images[str(x) + ";" + str(y)] = image
                                        savable_image = {"path": self.path, "size": self.tilesize,"pos": [x, y]}
                                        savable_images[str(x) + ";" + str(y)] = savable_image
                        if len(ti_sel) == 1:
                            if self.loaded:
                                        image = extract_image(self.image, self.tilesize, tile_pos)
                                        images[str(tile_pos[0]) + ";" + str(tile_pos[1])] = image
                                        savable_image = {"path": self.path, "size": self.tilesize,"pos": [x, y]}
                                        savable_images[str(x) + ";" + str(y)] = savable_image
                        selecting = False
                        ti_sel = []
                        add_select_dialog.active = True
                        add_select_dialog.reset()
                    if event.key == pygame.K_q:
                        if self.images:
                            if show_case:
                                texting = True
                    if event.key == pygame.K_TAB:
                        text = ""
                    if event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    if event.key == pygame.K_F1:
                        self.level.physics.add(text)
                        add_physics_dialog.active = True
                        add_physics_dialog.reset()
                    if event.key == pygame.K_F2:
                        self.level.decor.add(text)
                        add_decor_dialog.active = True
                        add_decor_dialog.reset()
                    if event.key == pygame.K_F5:
                        self.level.offgrid_decor.add(text)
                        add_offgrid_dialog.active = True
                        add_offgrid_dialog.reset()
                    if event.key == pygame.K_F6:
                        self.level.spawners.add(text)
                        add_spawner_dialog.active = True
                        add_spawner_dialog.reset()
                    if event.key == pygame.K_RETURN:
                        if text in self.assets:
                            new = join(self.assets[text], self.images)
                            new = set(new)
                            new = list(new)
                            self.assets[text] = new
                            self.types = list(self.assets)
                        else:
                            self.images = set(self.images)
                            self.images = list(self.images)
                            self.assets[text] = self.images
                        if text in self.savable_assets:
                            new = join(self.savable_assets[text], self.s_images)
                            self.savable_assets[text] = new
                        else:
                            self.savable_assets[text] = self.s_images
                        texting = False
                        if text in self.assets:
                            self.types = list(self.assets)
                            add_asset_dialog.active = True
                            add_asset_dialog.reset()
                if event.type == pygame.TEXTINPUT:
                    if texting:
                        text += event.text
                

            pygame.display.flip()

    def get_other_assets(self):
        running = True
        PATH = "data/images/other"
        used_path = PATH
        pressed = False
        scroll = [0, 0]
        timer = Timer(60, 1)
        path_list = [PATH]
        hist = PATH
        timer.start()
        name = ""

        title_bar = TitleBar(self.font, self.display, "Other Assets")
        #tab = Custom_Table(self.font, [int(self.display.get_width() // 3), 32], [200, 16], 1, 20)
        tab = Custom_Table(self.font, [0, 32], [self.display.get_width(), 16], 1, 20)
        saveImageDialog = Dialog(self.font, "Image added", [0, self.display.get_height() - 64], [200, 32], ["green", "aqua"], 5)
        saveImagesDialog = Dialog(self.font, "Images added", [0, self.display.get_height() - 64], [200, 32], ["green", "aqua"], 5)
        saveSoundDialog = Dialog(self.font, "Sound added", [0, self.display.get_height() - 64], [200, 32], ["green", "aqua"], 5)
        while running:
            self.display.fill(self.bkg_color)
            scroll_control(scroll)
            tab.add_item(hist, [0, 0])
            for i, folder in enumerate(os.listdir(used_path)):
                tab.add_item(folder, [0, i+1])
            tab.set_row_font_color(0, "red")
            selec = tab.mouse_select(0, self.render_scale, scroll)
            if selec != "" and selec != "...":
                if timer.done:
                    pt = os.path.join(used_path, selec)
                    if os.path.isdir(pt):
                        used_path = os.path.join(used_path, selec)
                        hist = used_path
                        path_list.append("/"+selec)
                        tab.empty()
                        timer.start()
            selec2 = tab.mouse_select(2, self.render_scale, scroll)
            if selec2 != "" and selec2 != "...":
                if timer.done:
                    imgs = ["png", "jpeg", "jpg"]
                    sounds = ["wav", "mp3"]
                    temp = selec2.split(".")
                    if len(temp) > 1:
                        if temp[-1].lower() in imgs:
                            name = text_input2([self.display, self.screen], self.font, name, "Image label")
                            img = load_image(os.path.join(used_path, selec2))
                            self.savable_assets[name] = [{"path": os.path.join(used_path, selec2), "size": img.get_size(), "pos": [0, 0]}]
                            self.assets[name] = [img]
                            saveImageDialog.active = True
                            saveImageDialog.reset()
                        elif temp[-1].lower() in sounds:
                            text_input2([self.display, self.screen], self.font, name, "Sound Label")
                            self.other_assets[name] = [{"type": "sound", "path": os.path.join(used_path, selec2)}]
                            saveSoundDialog.active = True
                            saveSoundDialog.reset()
                            
                    else:
                        name = text_input2([self.display, self.screen], self.font, name, "Images Label")
                        imgs = load_images(os.path.join(used_path, selec2))
                        self.assets[name] = imgs
                        self.savable_assets[name] = load_loadable_images(os.path.join(used_path, selec2))
                        saveImagesDialog.active = True
                        saveImagesDialog.reset()
            timer.update()
            #tab.set_table_opacity(100)
            tab.draw(self.display, scroll)
            saveImageDialog.update(self.display)
            saveImagesDialog.update(self.display)
            saveSoundDialog.update(self.display)
            title_bar.update()
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), [0, 0])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_l:
                        pressed = True
                    if event.key == pygame.K_RETURN:
                        running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 2:
                        if len(path_list) > 1:
                            path_list.pop(-1)
                            used_path = ""
                            for i, part in enumerate(path_list):
                                if i == 0:
                                    used_path += part.strip("/")
                                else:
                                    used_path += part
                                hist = used_path
                        tab.empty()
                        
                        
            pygame.display.flip()
            self.clock.tick(60)

    def categorise_assets(self):
        title_bar = TitleBar(self.font, self.display, "Categorise Assets")
        categories = ["spawners", "decor", "physics", "ongrid", "offgrid_decor", "blocks", "fluid"]
        if self.assets:
            types = list(self.assets)
            assets_tab = Custom_Table(self.font, [0, 32], [int(self.display.get_width() // 2) - 20, 16], 1, len(types) + 1)
            assets_tab.add_item("ASSETS", [0, 0])
            assets_tab.set_row_font_color(0, "orange")
            for i ,t in enumerate(types):
                assets_tab.add_item(t, [0, i + 1])
        else:
            assets_tab = Custom_Table(self.font, [0, 32], [int(self.display.get_width() // 2) - 20, 16], 1, 10)
            assets_tab.add_item("ASSETS", [0, 0])
            assets_tab.set_row_font_color(0, "orange")
        category_tab = Custom_Table(self.font, [int(self.display.get_width() // 2), 32], [int(self.display.get_width() // 2), 16], 1, len(categories) + 1)
        category_tab.add_item("CATEGORIES", [0, 0])
        category_tab.set_row_font_color(0, "orange")
        for i, cat in enumerate(categories):
            category_tab.add_item(cat, [0, i + 1])
        running = True
        scroll = [0, 0]
        asset = ""
        section_dialog = Dialog(self.font, "Text", [10, int(self.display.get_width() // 2)], [400, 32], ["green", "aqua"], 5)
        while running:
            self.display.fill(self.bkg_color)
            assets_tab.draw(self.display, scroll)
            category_tab.draw(self.display)
            asset_selec = assets_tab.mouse_select(0, self.render_scale, scroll)
            cat_selec = category_tab.mouse_select(0, self.render_scale)
            if asset_selec != "" and asset_selec != "...":
                asset = asset_selec
            if cat_selec != "" and cat_selec != "...":
                if asset != "":
                    match cat_selec:
                        case  "spawners":
                            self.level.spawners.add(asset)
                            section_dialog.start_with_text(f"{asset} added to {cat_selec}")
                        case "decor":
                            self.level.decor.add(asset)
                            section_dialog.start_with_text(f"{asset} added to {cat_selec}")
                        case "physics":
                            self.level.physics.add(asset)
                            section_dialog.start_with_text(f"{asset} added to {cat_selec}")
                        case "ongrid_decor":
                            self.level.ongrid_decor.add(asset)
                            section_dialog.start_with_text(f"{asset} added to {cat_selec}")
                        case "offgrid_decor":
                            self.level.offgrid_decor.add(asset)
                            section_dialog.start_with_text(f"{asset} added to {cat_selec}")
                        case "blocks":
                            self.level.blocks.add(asset)
                            section_dialog.start_with_text(f"{asset} added to {cat_selec}")
                        case "fluid":
                            self.level.fluid.add(asset)
                            section_dialog.start_with_text(f"{asset} added to {cat_selec}")
                    asset = ""
            for spawner in self.level.spawners:
                if spawner in self.level.blocks:
                    self.level.blocks.remove(spawner)
                if spawner in self.level.fluid:
                    self.level.fluid.remove(spawner)
            for fluid in self.level.fluid:
                if fluid in self.level.blocks:
                    self.level.blocks.remove(fluid)

            scroll_control(scroll, 4)
            section_dialog.update(self.display)
            title_bar.update()
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            pygame.display.flip()
            self.clock.tick(60)

    def get_saved_assets(self):
        title_bar = TitleBar(self.font, self.display, "GET SAVED ASSETS")
        PATH = "data/"
        used_path = PATH
        pressed = False
        scroll = [0, 0]
        timer = Timer(60, 1)
        path_list = [PATH]
        hist = PATH
        timer.start()
        name = "a"
        tab = Custom_Table(self.font, [0, 32], [self.display.get_width(), 16], 1, 20)
        saveAssetsDialog = Dialog(self.font, "Images added", [0, 200], [200, 32], ["green", "aqua"])
        running = True
        while running:
            timer.update()
            self.display.fill(self.bkg_color)
            scroll_control(scroll)
            tab.add_item(hist, [0, 0])
            for i, folder in enumerate(os.listdir(used_path)):
                tab.add_item(folder, [0, i+1])
            tab.set_row_font_color(0, "red")
            selec = tab.mouse_select(0, self.render_scale, scroll)
            selec2 = tab.mouse_select(2, self.render_scale, scroll)
            
            if selec != "" and selec != "...":
                if timer.done:
                    pt = os.path.join(used_path, selec)
                    if os.path.isdir(pt):
                        used_path = os.path.join(used_path, selec)
                        hist = used_path
                        path_list.append("/"+selec)
                        tab.empty()
                        timer.start()
            if selec2 != "" and selec2 != "...":
                if timer.done:
                    ext = ["json"]
                    temp = selec2.split(".")
                    if len(temp) > 1:
                        if temp[-1].lower() in ext:
                            name = text_input2([self.display, self.screen], self.font, name, "Type of assets to import")
                            if name == "o":
                                get_game_assets(os.path.join(used_path, selec2), self.other_assets)
                                saveAssetsDialog.start_with_text(f"{name} other assets extracted")
                            else:
                                get_game_assets(os.path.join(used_path, selec2), self.assets)
                                saveAssetsDialog.start_with_text(f"{name} assets extracted")
                                self.types = list(self.assets)
                                self.loaded = True
                
            tab.draw(self.display, scroll)
            saveAssetsDialog.update(self.display)
            title_bar.update()
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), [0, 0])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_TAB:
                        typ = text_input2([self.display, self.screen], self.font, typ, "Type of Assets to Load.")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 2:
                        if len(path_list) > 1:
                            path_list.pop(-1)
                            used_path = ""
                            for i, part in enumerate(path_list):
                                if i == 0:
                                    used_path += part.strip("/")
                                else:
                                    used_path += part
                                hist = used_path
                        tab.empty()
            pygame.display.flip()
            self.clock.tick(60)

    def run(self):
        running = True
        sIdCounter = 0
        cur = pygame.Surface(self.tilesize)
        while running:
            self.dt = self.clock.tick(60) / 1000
            if self.loaded:
                self.type = self.types[self.type_index]
                self.current = self.assets[self.type] 
                self.types = list(self.assets)
            self.display.fill((0, 10, 30))
            key = pygame.key.get_pressed()
            if key[pygame.K_l]:
                self.get_asset()
            if key[pygame.K_UP]:
                self.scroll[1] -= 4
            if key[pygame.K_DOWN]:
                self.scroll[1] += 4
            if key[pygame.K_LEFT]:
                self.scroll[0] -= 4
            if key[pygame.K_RIGHT]:
                self.scroll[0] += 4
            if self.loaded:
                mclick = pygame.mouse.get_pressed()
                if mclick[0]:
                    mpos = pygame.mouse.get_pos()
                    tile_pos = [mpos[0] // self.render_scale, mpos[1] // self.render_scale]
                    tile_pos = [int((tile_pos[0] + self.scroll[0]) // self.tilesize[0]), int((tile_pos[1] + self.scroll[1]) // self.tilesize[1])]
                    if self.type in self.level.physics:
                        self.level.tilemap[str(tile_pos[0]) + ";" + str(tile_pos[1])] = {"type": self.type, "variant": self.current_index, "pos":tile_pos, "layer": self.current_layer}
                        self.level.layering()
                    if self.type in self.level.blocks:
                        self.level.phys_blocks[str(tile_pos[0]) + ";" + str(tile_pos[1])] = {"type": self.type, "variant": self.current_index, "pos":tile_pos, "layer": self.current_layer}
                        self.level.layering()
                    if self.type in self.level.spawners:
                        self.level.spawn_blocks[str(tile_pos[0]) + ";" + str(tile_pos[1])] = {"type": self.type, "variant": self.current_index, "pos":tile_pos, "team": "", "id": sIdCounter, "limit": 4, "limited": True, "layer": self.current_layer}
                        sIdCounter += 1
                elif mclick[2]:
                    mpos = pygame.mouse.get_pos()
                    tile_pos = [mpos[0] // self.render_scale, mpos[1] // self.render_scale]
                    tile_pos = [int((tile_pos[0] + self.scroll[0]) // self.tilesize[0]), int((tile_pos[1] + self.scroll[1]) // self.tilesize[1])]
                    check = str(tile_pos[0]) + ";" + str(tile_pos[1])
                    if check in self.level.tilemap:
                        del self.level.tilemap[check]
                        self.level.layering()
                    if check in self.level.phys_blocks:
                        del self.level.phys_blocks[check]
                        self.level.layering()
                    if check in self.level.spawn_blocks:
                        del self.level.spawn_blocks[check]
            
            self.level.draw(self.display, self.scroll)
            if self.current:
                if not self.current[self.current_index] in self.level.blocks:
                    img = self.current[self.current_index]
                    cur.blit(img,[0, 0])
                else:
                    pygame.draw.rect(cur, self.current[self.current_index], [0, 0, self.tilesize[0], self.tilesize[1]])
                cur.set_alpha(50)
                self.display.blit(cur, [0, 0])
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), [0, 0])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.save_asset_path()
                    if event.key == pygame.K_COMMA:
                        if self.loaded:
                            if self.current:
                                self.current_index = (self.current_index + 1) % len(self.current)
                    if event.key == pygame.K_PERIOD:
                        if self.loaded:
                            if self.current:
                                self.current_index = (self.current_index - 1) % len(self.current)    
                    if event.key == pygame.K_LEFTBRACKET:
                        self.current_layer = (self.current_layer + 1) % 3   
                        self.level.current_layer = self.current_layer
                    if event.key == pygame.K_RIGHTBRACKET:
                        self.current_layer = (self.current_layer - 1) % 3   
                        self.level.current_layer = self.current_layer
                    if event.key == pygame.K_SEMICOLON:
                        if self.loaded:
                            if self.types:
                                self.current_index = 0
                                self.type_index = (self.type_index + 1) % len(self.types)
                    if event.key == pygame.K_QUOTE:
                        if self.loaded:
                            if self.types:
                                self.current_index = 0
                                self.type_index = (self.type_index - 1) % len(self.types)

                    if event.key == pygame.K_KP_1:
                        self.settings()
                    if event.key == pygame.K_KP_ENTER:
                        self.load_assets()
                    if event.key == pygame.K_KP_MINUS:
                        self.help_menu()
                    if event.key == pygame.K_KP_PLUS:
                        self.save_map()
                    if event.key == pygame.K_KP_MULTIPLY:
                        self.add_block()
                    if event.key == pygame.K_KP_0:
                        self.select_assets()
                    if event.key == pygame.K_KP_DIVIDE:
                        self.get_other_assets()
                    if event.key == pygame.K_PAGEDOWN:
                        self.categorise_assets()
                    if event.key == pygame.K_PAGEUP:
                        self.get_saved_assets()
                    
                    
            pygame.display.update()
        pygame.quit()

LevelEditor().run()
