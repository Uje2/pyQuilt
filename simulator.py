import pygame
import math, random
import sys
from scripts.particle import Particles, Demo, Spark, Trail, Shockwave
from scripts.tilemap import Anchors
from scripts.widgets import Label, Slider, Button, TitleBar, Table, text_input, text_input2
from scripts.utils import Timer


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
        # Widget tests
        label1 = Label("Kelvin da Great", [50, 50], self.font, ["red", "green"])
        slider1 = Slider([0, 255], [150, 50], 100, [64, 20])
        btn1 = Button([200, 100], "red", [48, 16])
        btn1.set_text(self.font, "play", "aqua", [4, 20])
        label2 = Label("Button Tests", [100, 100], self.font, ["red", "green"])
        n = 5
        table1 = Table(self.font, [50, 50], 2, 4, "aquamarine")
        table1.add_item("kelvin", [0, 0])
        table1.add_item("Mujeni", [1, 0])
        table1.add_item("Tadiwanashe", [2, 0])
        table1.add_item("Patsanza", [3, 0])
        table1.add_item("kingsley", [0, 1])
        table1.add_item("Mutondoro", [1, 1])
        table1.get_table_color("crimson")
        table1.set_table_opacity(100)
        label3 = Label("Timer Test", [100, 200], self.font, ["red", "crimson"])
        label4 = Label("Timer Test", [200, 200], self.font, ["red", "crimson"])
        timer1 = Timer(60, 2)
        timer1.start()
        text = ""
        while run:
            self.display.fill((20, 50, 90))
            #slider1.set_value(n)
            #n = (n+1) % 255
            mouse_scroll(slider1)
            btn_control(btn1)
            slider1.update(self.display)
            label1.set_text(f"value: {slider1.value}")
            label1.update(self.display)
            btn1.update(self.display)
            label2.set_text(f"btn1 is: {btn1.active}")
            label2.update(self.display)
            timer1.update()
            label3.set_text(f"Timer Test: {timer1.now}")
            label3.update(self.display)
            label4.set_text(f"Timer Test: {timer1.done}")
            label4.update(self.display)
            if timer1.done:
                timer1.start()
            title.update()
            table1.draw(self.display)
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), [0, 0])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_KP_ENTER:
                        self.selector()
                    if event.key == pygame.K_KP_PLUS:
                        text_input2([self.display, self.screen], self.font, text, "TEXT INPUT")

            pygame.display.update()
            self.clock.tick(60)
        pygame.quit()

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
            slider.set_value(int((int(mpos[0] - slider.pos[0]) / 64) * 255))
        '''else:
            mpos = pygame.mouse.get_pos()
            mpos = [int(mpos[0] // 2), int(mpos[1] //2)]
            slider.incriment_value(mpos[0])
            #slider.set_value(mpos[0] // int(640 // slider.size[0]))'''
            
    if mp[2]:
        #slider.reset_range()
        slider.active = False

timer = Timer(60, 1)
timer.done = True

def btn_control(btn: Button):
    mp = pygame.mouse.get_pressed()
    if mp[0]:
        mpos = pygame.mouse.get_pos()
        mpos = [int(mpos[0] // 2), int(mpos[1] //2)]
        btn_rect = btn.get_rect()
        if btn_rect.collidepoint(mpos):
            if timer.done:
                btn.set_state()
                timer.start()
    
Simulator().run()