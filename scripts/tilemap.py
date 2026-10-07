import pygame
import json
import math

from scripts.utils import join

NEIGHBOR_OFFSETS = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 0], [0, 1], [1, -1], [1, 0], [1, 1]]

class Tilemp:
    def __init__(self, game, tilesize, layered=True):
        self.game = game
        self.tilesize = tilesize
        self.layered = layered
        if self.layered:
            self.tilemap = {"layer0": {}, "layer1": {}, "layer2": {}}
            self.spawn_blocks = {"layer0": {}, "layer1": {}, "layer2": {}}
            self.phys_blocks = {"layer0": {}, "layer1": {}, "layer2": {}}
            self.fluid_blocks = {"layer0": {}, "layer1": {}, "layer2": {}}
        else:
            self.tilemap = {}
            self.phys_blocks = {}
            self.spawn_blocks = {}
            self.fluid_blocks = {}
        self.offgrid = []
        self.ongrid = {}
        self.ongrid_decor = set()
        self.physics = {}
        self.offgrid_decor = set()
        self.spawners = set()
        self.decor = set()
        self.fluid = set()
        self.animated = set()
        self.current_layer = 1
        self.blocks = set()
        
    
    def tiles_around(self, pos):
        tiles = []
        tile_pos = [int(pos[0] // self.tilesize[0]), int(pos[1] // self.tilesize[1])]
        for offset in NEIGHBOR_OFFSETS:
            check_pos = str(tile_pos[0] + offset[0]) + ";" + str(tile_pos[1] + offset[1])
            if check_pos in self.tilemap:
                tile = self.tilemap[check_pos]
                if tile["type"] in self.physics and not tile["type"] in self.spawners and not tile["type"] in self.fluid:
                    tiles.append(tile)
        return tiles

    def pblocks_around(self, pos):
            tiles = []
            tile_pos = [int(pos[0] // self.tilesize[0]), int(pos[1] // self.tilesize[1])]
            for offset in NEIGHBOR_OFFSETS:
                check_pos = str(tile_pos[0] + offset[0]) + ";" + str(tile_pos[1] + offset[1])
                if check_pos in self.phys_blocks:
                    tile = self.phys_blocks[check_pos]
                    if tile["type"] in self.blocks and not tile["type"] in self.spawners and not tile["type"] in self.fluid:
                        tiles.append(tile)
            return tiles

    def phys_blocks_around(self, pos):
        rects = []
        for tile in self.pblocks_around(pos):
            rects.append(pygame.Rect(tile["pos"][0] * self.tilesize[0], tile["pos"][1] * self.tilesize[1], self.tilesize[0], self.tilesize[1]))
        return rects
    
    def physics_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            rects.append(pygame.Rect(tile["pos"][0] * self.tilesize[0], tile["pos"][1] * self.tilesize[1], self.tilesize[0], self.tilesize[1]))
        return rects
    
    def tile_at(self, pos):
        tile_pos = [int(pos[0] // self.tilesize[0]), int(pos[1] // self.tilesize[1])]
        check_pos = str(tile_pos[0]) + ";" + str(tile_pos[1])
        if check_pos in self.tilemap:
            return True
        else:
            return False
    
    def ongrid_at(self, pos):
        tile_pos = [int(pos[0] // self.tilesize[0]), int(pos[1] // self.tilesize[1])]
        check_pos = str(tile_pos[0]) + ";" + str(tile_pos[1])
        if check_pos in self.ongrid:
            return True
        else:
            return False
        
    def offgrid_at(self, pos, offset=[0, 0]):
        ...
    
    def save_map(self, path):
        f = open(f"data/maps/{path}.json", "w")
        data = {"tilesize": self.tilesize, "tilemap": self.tilemap, "ongrid": self.ongrid, "offgrid": self.offgrid, "physics": self.physics}
        json.dump(data, f)
        f.close()

    def load_map(self, path):
        f = open(f"data/maps/{path}.json", "r")
        data = json.load(f)
        self.tilemap = data["tilemap"]
        self.tilesize = data["tilesize"]
        if "physics" in data:
            self.physics = set(data["physics"])
        if "ongrid" in data:
            self.ongrid = data["ongrid"]
        if "offgrid" in data:
            self.offgrid = data["offgrid"]
        if "blocks" in data:
            self.blocks = set(data["blocks"])
        if "phys_blocks" in data:
            self.phys_blocks = data["phys_blocks"]
        if "spawners" in data:
            self.spawners = set(data["spawners"])
        f.close()

    def load_custom_map(self, path):
            f = open(f"{path}", "r")
            data = json.load(f)
            self.tilemap = data["tilemap"]
            self.tilesize = data["tilesize"]
            if "physics" in data:
                self.physics = set(data["physics"])
            if "ongrid" in data:
                self.ongrid = data["ongrid"]
            if "offgrid" in data:
                self.offgrid = data["offgrid"]
            if "blocks" in data:
                self.blocks = set(data["blocks"])
            if "phys_blocks" in data:
                self.phys_blocks = data["phys_blocks"]
            if "spawners" in data:
                self.spawners = set(data["spawners"])
            f.close()

    def draw(self, surf, offset=[0, 0]):
        for x in range(int(offset[0] // self.tilesize[0]), int((offset[0]+surf.get_width()+self.tilesize[0]) // self.tilesize[0])):
            for y in range(int(offset[1] // self.tilesize[1]), int((offset[1]+surf.get_height()+self.tilesize[1]) // self.tilesize[1])):
                loc = str(x) + ";" + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    img = self.game.assets[tile["type"]][tile["variant"]].copy()
                    img.set_alpha(50 if self.current_layer != 0 else 255)
                    surf.blit(img, [tile["pos"][0] * self.tilesize[0] - offset[0], tile["pos"][1] * self.tilesize[1] - offset[1]])
                if loc in self.phys_blocks:
                    tile = self.phys_blocks[loc]
                    img = pygame.Surface(self.tilesize)
                    #img = pygame.Surface(tile["size"])
                    pygame.draw.rect(img, tile["type"], [0, 0, self.tilesize[0], self.tilesize[1]], 0 if tile["variant"] == 0 else 2)
                    #pygame.draw.rect(img, tile["type"], [0, 0, tile["size"][0], tile["size"][1]], 0 if tile["variant"] == 0 else 2)
                    img.set_alpha(50 if self.current_layer != 0 else 255)
                    surf.blit(img, [tile["pos"][0] * self.tilesize[0] - offset[0], tile["pos"][1] * self.tilesize[1] - offset[1]])
                    #surf.blit(img, [tile["pos"][0] * tile["size"][0] - offset[0], tile["pos"][1] * tile["size"][1] - offset[1]])
        
                '''
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    surf.blit(self.game.assets[tile["type"]][tile["variant"]], [tile["pos"][0] * self.tilesize[0] - offset[0], tile["pos"][1] * self.tilesize[1] - offset[1]])
                if loc in self.ongrid:
                    tile = self.ongrid[loc]
                    surf.blit(self.game.assets[tile["type"]][tile["variant"]], [tile["pos"][0] * self.tilesize[0] - offset[0], tile["pos"][1] * self.tilesize[1] - offset[1]])
                '''

    def draw_layers(self, surf,offset=[0, 0]):
        for i in range(3):
            self.draw_layer(surf=surf,layer=i, offset=offset)


    def draw_layer(self, surf, layer, offset=[0, 0]):
        is_color = False
        for x in range(int(offset[0] // self.tilesize[0]), int((offset[0]+surf.get_width() + self.tilesize[0]) // self.tilesize[0])):
            for y in range(int(offset[1] // self.tilesize[1]), int((offset[1]+surf.get_height() + self.tilesize[1]) // self.tilesize[1])):
                loc = str(x) + ";" + str(y)
                tmap = "layer"+str(layer)
                tem = 200
                if loc in self.tilemap[tmap]:
                    tile = self.tilemap[tmap][loc]
                    if "layer" in tile:
                        if tile["layer"] == 0:
                            tem = 50
                        elif tile["layer"] == 1:
                            tem = 200
                        elif tile["layer"] == 2:
                            tem = 255
                    img = self.game.assets[tile["type"]][tile["variant"]].copy()
                    try:
                        pygame.Color(img)
                        is_color = True
                    except ValueError:
                        is_color = False
                    if is_color:
                        img = pygame.Surface(self.tilesize)
                        pygame.draw.rect(img, tile["type"], [0, 0, self.tilesize[0], self.tilesize[1]], 0 if tile["variant"] == 0 else 2)
                    else:
                        img = self.game.assets[tile["type"]][tile["variant"]].copy()
                    img.set_alpha(tem)
                    surf.blit(img, [tile["pos"][0] * self.tilesize[0] - offset[0], tile["pos"][1] * self.tilesize[1] - offset[1]])
                if loc in self.phys_blocks[tmap]:
                    tile = self.phys_blocks[tmap][loc]
                    if "layer" in tile:
                        if tile["layer"] == 0:
                            tem = 50
                        elif tile["layer"] == 1:
                            tem = 200
                        elif tile["layer"] == 2:
                            tem = 255
                    img = pygame.Surface(self.tilesize)
                    pygame.draw.rect(img, tile["type"], [0, 0, self.tilesize[0], self.tilesize[1]], 0 if tile["variant"] == 0 else 2)
                    img.set_alpha(tem)
                    surf.blit(img, [tile["pos"][0] * self.tilesize[0] - offset[0], tile["pos"][1] * self.tilesize[1] - offset[1]])
                if loc in self.spawn_blocks[tmap]:
                    tile = self.spawn_blocks[tmap][loc]
                    if "layer" in tile:
                        if tile["layer"] == 0:
                            tem = 50
                        elif tile["layer"] == 1:
                            tem = 200
                        elif tile["layer"] == 2:
                            tem = 255
                    try:
                        pygame.Color(tile["type"])
                        is_color = True
                    except ValueError:
                        is_color = False
                    if is_color:
                        img = pygame.Surface(self.tilesize)
                        pygame.draw.rect(img, tile["type"], [0, 0, self.tilesize[0], self.tilesize[1]], 0 if tile["variant"] == 0 else 2)
                    else:
                        img = self.game.assets[tile["type"]][tile["variant"]].copy()
                    img.set_alpha(tem)
                    surf.blit(img, [tile["pos"][0] * self.tilesize[0] - offset[0], tile["pos"][1] * self.tilesize[1] - offset[1]])
                if loc in self.fluid_blocks[tmap]:
                    tile = self.fluid_blocks[tmap][loc]
                    if "layer" in tile:
                        if tile["layer"] == 0:
                            tem = 50
                        elif tile["layer"] == 1:
                            tem = 200
                        elif tile["layer"] == 2:
                            tem = 255
                    try:
                        pygame.Color(tile["type"])
                        is_color = True
                    except ValueError:
                        is_color = False
                    if is_color:
                        img = pygame.Surface(self.tilesize)
                        pygame.draw.rect(img, tile["type"], [0, 0, self.tilesize[0], self.tilesize[1]], 0 if tile["variant"] == 0 else 2)
                    else:
                        img = self.game.assets[tile["type"]][tile["variant"]].copy()
                    img.set_alpha(tem)
                    surf.blit(img, [tile["pos"][0] * self.tilesize[0] - offset[0], tile["pos"][1] * self.tilesize[1] - offset[1]])



class Anchor:
    def __init__(self, pos, radius):
        self.pos = list(pos)
        self.radius = radius
        self.anchored = False
        self.left = []
        self.right = []

    def get_anchor(self, anchor):
        self.anchor = anchor
        self.anchored = True

    def update(self, surf, offset=[0, 0]):
        if self.anchored:
            pos = self.pos
            anchor_pos = self.anchor.pos
            x = int(anchor_pos[0] - pos[0])
            y = int(anchor_pos[1] - pos[1])
            print(f"x: {x}, y: {y}")
            angle = math.atan2(y, x)
            #angle *= 10
            print(f"angle: {angle}")
            self.anchor.pos = list([self.pos[0] + math.cos(angle) * self.radius, self.pos[1] + math.sin(angle) * self.radius])
            left = [self.pos[0] + math.cos(angle + math.pi / 2) * self.radius, self.pos[1] + math.sin(angle + math.pi / 2) * self.radius]
            right = [self.pos[0] + math.cos(angle - math.pi / 2) * self.radius, self.pos[1] + math.sin(angle - math.pi / 2) * self.radius]
            pygame.draw.line(surf, "aqua", left, right)
            pygame.draw.aaline(surf, "white", self.pos, self.anchor.pos, 5)
            self.left = left
            self.right = right
        pygame.draw.circle(surf, "white", [self.pos[0] - offset[0], self.pos[1] - offset[1]], 3, 2)
        pygame.draw.circle(surf, "yellow", [self.pos[0] - offset[0], self.pos[1] - offset[1]], self.radius, 2)


class Anchors:
    def __init__(self, pos, radi):
        self.pos = list(pos)
        #self.head = Anchor(self.pos, radi[0])
        self.body = []
        for i in range(len(radi)):
            self.body.append(Anchor([self.pos[0] + i, self.pos[1]], radi[i]))
        if self.body:
            if len(self.body) > 1:
                for i in range(len(self.body)):
                    if i < len(self.body) - 1:
                        self.body[i].get_anchor(self.body[i + 1])
        self.head = self.body[0]
        self.points = []

    def add_anchor(self, radius):
        an = Anchor(self.pos, radius)
        self.body[-1].get_anchor(an)
        self.body.append(an)

    def draw(self, surf):
        self.points = []
        right = []
        for anchor in self.body:
            if anchor.left and anchor.right:
                self.points.append(anchor.left)
                #self.points.append(anchor.right)
        for anchor in self.body:
            if anchor.left and anchor.right:
                right.append(anchor.right)
        self.points = join(self.points, reversed(right))
        pygame.draw.polygon(surf, "green", self.points, 3)
        pygame.draw.circle(surf, "green", self.head.pos, self.head.radius)
        pygame.draw.circle(surf, "green", self.body[-2].pos, self.body[-2].radius)
        pygame.draw.circle(surf, "green", self.body[-1].pos, self.body[-1].radius)
        pygame.draw.circle(surf, "aqua", [self.head.left[0], self.head.left[1]], 3)
        pygame.draw.circle(surf, "aqua", [self.head.right[0], self.head.right[1]], 3)

    
    def update(self, surf):
        self.head.update(surf)
        for anchor in self.body:
            anchor.update(surf)
        #self.draw(surf)
