import pygame
import json
import os

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
            slider.set_value(int((int(mpos[0] - slider.pos[0]) / 64) * 255))
        '''else:
            mpos = pygame.mouse.get_pos()
            mpos = [int(mpos[0] // 2), int(mpos[1] //2)]
            slider.incriment_value(mpos[0])
            #slider.set_value(mpos[0] // int(640 // slider.size[0]))'''
            
    if mp[2]:
        #slider.reset_range()
        slider.active = False

def btn_control(btn):
    mp = pygame.mouse.get_pressed()
    if mp[0]:
        mpos = pygame.mouse.get_pos()
        mpos = [int(mpos[0] // 2), int(mpos[1] //2)]
        btn_rect = btn.get_rect()
        if btn_rect.collidepoint(mpos):
            btn.set_state()
    
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
        rect = pygame.Rect(pos[0]* 16 - offset[0], pos[1]*16- offset[1], dists[0], dists[1])
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
            temp.append(extract_image(image["path"], image["size"], images["pos"]))
        dicty[asset] = temp
    return dicty

def multiply_lists(list1, list2):
    return [list1[0] * list2[0], list1[1] * list2[1]]

def add_lists(list1, list2):
    return [list1[0] + list2[0], list1[1] + list2[1]]

def load_image(path, setcolorkey= True,color="black"):
    image = pygame.image.load(path)
    image.convert_alpha()
    if setcolorkey:
        image.set_colorkey(color)
    return image

def load_images(path, setcolorkey= True,color="black"):
    images = []
    for image in os.listdir(path):
        images.append(load_image(path + "/" + image, setcolorkey,color))
    return images