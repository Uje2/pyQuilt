import pygame
from scripts.particle import Shockwave, RingWave
from scripts.utils import dists


class ShinraTensei:
    def __init__(self, max=[60, 60]):
        self.max = list(max)
        self.color = "aqua"
        self.pos = []
        self.rect = []
        self.img = pygame.Surface(self.max)
        self.pushed = False
        self.dead = False
        self.params = {"max": max}

    def serialize(self):
        return {
            "name": "ShinraTensei",
            "params": self.params
        }

    def copy(self):
        return ShinraTensei(max=self.max)

    def push(self, pos):
        self.pos = list(pos)
        #self.rect = pygame.Rect(self.pos[0], self.pos[1], self.max[0], self.max[1])
        self.rect = self.img.get_rect(center=self.pos)
        #self.wave = Shockwave(self.pos, color=self.color, width=8, size=16, speed=0.5)
        self.wave = RingWave(self.pos, square_size=60, lifetime=16, outer_thickness=8, inner_thickness=5)
        self.pushed = True

    def update(self, players):
        pushes = {"left": False, "right": False, "up": False, "down": False}
        if self.pushed:
            #self.wave.update(surf, offset=offset)
            #pygame.draw.rect(surf, self.color, [self.rect.x - offset[0], self.rect.y - offset[1], self.rect.w, self.rect.h], 2)
            if self.wave.dead:
                self.pushed = False
                self.dead = True
            else:
                for player in players:
                    p_rect = player.get_collider()
                    rect = self.rect
                    if rect.colliderect(p_rect):
                        if rect.centerx  > p_rect.centerx:
                            pushes["left"] = True
                        if rect.centerx <= p_rect.centerx:
                            pushes["right"] = True
                        if rect.centery > p_rect.centery:
                            pushes["up"] = True
                        if rect.centery <= p_rect.centery:
                            pushes["down"] = True

                        hor = False
                        vert = False
                        if pushes["left"] or pushes["right"]:
                            hor = True
                        if pushes["down"] or pushes["up"]:
                            vert = True

                        if hor and vert:
                            dist = dists(rect.center, p_rect.center)
                            if dist[0] >= dist[1]:
                                '''if pushes["left"]:
                                    #p_rect.right = rect.left 
                                    #player.pos[0] = p_rect.x
                                    player.velocity[0] = -3
                                else:
                                    #p_rect.left = rect.right
                                    #player.pos[0] = p_rect.x
                                    player.velocity[0] = 3'''
                                player.get_pushed(["hor", -3 if pushes["left"] else 3])
                            else:
                                '''if pushes["up"]:
                                    #p_rect.bottom = rect.top
                                    #player.pos[1] = p_rect.y
                                    player.velocity[1] = -3
                                else:
                                    #p_rect.top = rect.bottom
                                    #player.pos[1] = p_rect.y
                                    #player.velocity[1] = 3'''
                                player.get_pushed(["vert", -3 if pushes["up"] else 3])

    def draw(self, surf, offset=[0, 0]):
        self.wave.update(surf, offset=offset)
        #pygame.draw.rect(surf, self.color, [self.rect.x - offset[0], self.rect.y - offset[1], self.rect.w, self.rect.h], 2)


class Turrent:
    def __init__(self):
        self.pos = [0, 0]
        self.placed = False
        self.color = "red"
        self.rect = []
        self.image = []
        self.dead = False