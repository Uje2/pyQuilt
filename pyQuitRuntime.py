import pygame
import sys

from scripts.utils import Timer, button_control2, mouse_scroll_silders, slider_handle, button_handle, label_handle, timer_handle, get_game_assets, give_ids
from scripts.tilemap import Tilemp
from scripts.entities import PhysicsEntity
import json

class Scene:
    def __init__(self, game_config):
        self.game_config = game_config
        pygame.init()
        self.deserialize()
        

    def serialize(self):
        return {
            "name": self.name,
            "resolution": self.resolution,
            "renderscale": self.renderscale,
            "assets": self.path_to_assets,
            "font": self.path_to_font,
            "level": self.path_to_tilemap,
            "players": [player.serialize() for player in self.players],
            "split": self.split_screen,
            "entities": self.entities
        }

    def deserialize(self):
        data = self.game_config
        self.name = data["name"]
        self.screen = pygame.display.set_mode(data["resolution"])
        self.renderscale = data["renderscale"]
        self.display = pygame.Surface([int(self.screen.get_width()// self.renderscale), int(self.screen.get_height() // self.renderscale)])
        self.font = pygame.font.Font(data["font"])
        self.clock = pygame.time.Clock()
        self.assets = {}
        get_game_assets(data["assets"], self.assets)
        self.entities = data["entities"]
        self.split = data["split"]
        self.id = 0
        self.level = Tilemp(self, [16, 16])
        self.players = []
        for player in data["players"]:
            p = PhysicsEntity(self, [0, 0])
            p.deserialize(player)
            self.players.append(p)
        self.id = give_ids(self.players, self.id)
        self.levels = data["level"]
        self.abilities = []


    
    def split_screen_run(self):
        run = True
        displays = []
        scrolls = []
        int_scrolls = []
        count = 0
        renderscale = 2
        main_dimensions = [int(self.screen.get_width() // 2), self.screen.get_height()]
        for player in self.players:
            displays.append(pygame.Surface((int(self.screen.get_width() // int(renderscale)), int(self.screen.get_height()))))
            scrolls.append([0, 0])
            int_scrolls.append([0, 0])
        if len(self.levels) > 0:
            self.level.load_custom_map(self.levels[0])
        disp_conf = [[0, 0], [int(self.screen.get_width() // 2), 0]]
        while run:
            for display in displays:
                display.fill((20, 50, 90))
            for i, player in enumerate(self.players):
                scrolls[i][0] += (player.get_collider().centerx - displays[i].get_width() / 2) - scrolls[i][0]
                scrolls[i][1] += (player.get_collider().centery- displays[i].get_height() / 2) - scrolls[i][1]
                int_scrolls[i] = [int(scrolls[i][0]), int(scrolls[i][1])]
            
            for i, player in enumerate(self.players):
                id = player.id
                player.no_display_update(self.level.physics_around(player.pos))
                for ability in self.abilities[:]:
                    if ability[0] == id:
                        temp = self.players.copy()
                        temp.remove(player)
                        ability[1].update(temp)
                    if ability[1].dead:
                        self.abilities.remove(ability)
                    for x, display in enumerate(displays):
                        ability[1].draw(display, int_scrolls[x])
                for y, display in enumerate(displays):
                    player.draw_collider(display, int_scrolls[y])
                    self.level.draw(display, int_scrolls[y])
                    self.screen.blit(pygame.transform.scale(display, main_dimensions), disp_conf[y])
            #self.screen.blit(pygame.transform.scale(displays[1], main_dimensions), [int(self.screen.get_width() // 2), 0])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_KP0:
                        self.players[0].change_gravity_status()
                    if event.key == pygame.K_KP0:
                        self.players[1].change_gravity_status()
                        print(f"kp0: {pygame.K_KP0}")
                    if event.key == pygame.K_TAB:
                        self.save_serial_config()

            pygame.display.update()
            self.clock.tick(60)
        pygame.quit()

def load_serial_config():
    path = "data/game-configs/"
    name = "Test1"
    f = open(path + name + ".json", "r")
    data = json.load(f)
    f.close()
    return data

    '''def run(self):
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
                        self.player2.change_gravity_status()
                    if event.key == pygame.K_TAB:
                        self.save_serial_config()

            pygame.display.update()
            self.clock.tick(60)
        pygame.quit()'''


Scene(load_serial_config()).split_screen_run()