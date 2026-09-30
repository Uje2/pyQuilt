import pygame
import math, random
import sys
from scripts.particle import Particles, Demo, Spark, Trail, Shockwave, Trails, Sparks
from scripts.tilemap import Anchors
from scripts.widgets import Label, Slider, Button, RectedButton,TitleBar, Table, text_input, text_input2, Custom_Table, TextBox, VerticalSlider, Button2
from scripts.utils import Timer, button_control2, mouse_scroll_silders, slider_handle, button_handle, label_handle, timer_handle, get_game_assets, give_ids
from scripts.tilemap import Tilemp
from scripts.entities import PhysicsEntity

class Simulator:
    def __init__(self):
        pygame.init()
        self.renderscale = 2
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((int(self.screen.get_width() // self.renderscale), int(self.screen.get_height() // self.renderscale)))
        self.clock = pygame.time.Clock()
        self.assets = {}
        self.particles = []
        self.font = pygame.font.Font("data/fonts/at01.ttf")
        self.anchors = Anchors([50, 50], [15, 15, 15, 20, 20, 20, 20, 10, 10, 8, 5, 5, 5])
        self.anchor = self.anchors.head
        self.active = "None"
        self.level = Tilemp(self, [16, 16])
        self.id = 0
        self.player = PhysicsEntity([50, 50])
        self.player2 = PhysicsEntity([100, 50])
        self.players = [self.player, self.player2]
        self.id = give_ids(self.players, self.id)
        get_game_assets("data/allied/test_map.json", self.assets)
        self.level.assets = self.assets
    def anchor_tweaks(self):
        ...

    def anchor_manage(self):
        mclick = pygame.mouse.get_pressed()
        self.anchors.update(self.display)
        keys = pygame.key.get_pressed()
        s = 2
        if keys[pygame.K_UP]:
            self.anchor.pos[1] -= s
        if keys[pygame.K_DOWN]:
            self.anchor.pos[1] += s
        if keys[pygame.K_LEFT]:
            self.anchor.pos[0] -= s
        if keys[pygame.K_RIGHT]:
            self.anchor.pos[0] += s
        if keys[pygame.K_s]:
            self.anchors.draw(self.display)

    def selector(self):
        rrun = True
        title = TitleBar(self.font, self.display, "Selector")
        
        if self.active == "anchor":
            self.anchor_manage()
        while rrun:
            self.display.fill((20, 50, 90))
            title.update()
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        rrun = False

            pygame.display.update()
            self.clock.tick(60)

    
    def run(self):
        run = True
        count = 0
        title = TitleBar(self.font, self.display, "Simulator: Widget Testing")
        text = ""
        self.level.load_custom_map("data/allied/test_map.json")
        self.level.layering()
        #self.level.physics = {"steel_mid_two", "steel_upper_two", "steel_back", "steel_upper_one"}
        scroll = [0, 0]
        while run:
            scroll[0] += (self.player.get_collider().centerx - self.display.get_width() / 2) - scroll[0]
            scroll[1] += (self.player.get_collider().centery- self.display.get_height() / 2) - scroll[1]
            r_scroll = [int(scroll[0]), int(scroll[1])]
            self.display.fill((20, 50, 90))
            self.player.update(self.level.phys_blocks_around(self.player.pos), self.display, r_scroll)
            self.player2.update2(self.level.phys_blocks_around(self.player2.pos), self.display, r_scroll)
            self.level.draw(self.display, r_scroll)
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), [0, 0])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_KP_ENTER:
                        self.selector()
                    if event.key == pygame.K_KP_PLUS:
                        txt = text_input2([self.display, self.screen], self.font, text, "TEXT INPUT")
                    if event.key == pygame.K_KP0:
                        self.player.change_gravity_status()
                    if event.key == pygame.K_KP0:
                        self.player2.change_gravity_status()

            pygame.display.update()
            self.clock.tick(60)
        pygame.quit()

'''def mouse_scroll(slider):
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
            slider.set_value(int((int(mpos[0] - slider.pos[0]) / 64) * 255))
            
    if mp[2]:
        #slider.reset_range()
        slider.active = False'''
        
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
timer = Timer(30, 1)
timer.done = True

def btn_control(btn: Button, offset=[0, 0]):
    mp = pygame.mouse.get_pressed()
    timer.update()
    if mp[0]:
        mpos = pygame.mouse.get_pos()
        mpos = [int((mpos[0] // 2)+ offset[0]), int((mpos[1]  //2)+ offset[1])]
        btn_rect = btn.get_rect()
        if btn_rect.collidepoint(mpos):
            if timer.done:
                btn.set_state()
                timer.start()
    
Simulator().run()