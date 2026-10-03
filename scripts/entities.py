import pygame
from scripts.utils import load_image
from scripts.ability import ShinraTensei

GRAVITY = 0.2
jump_height = -3
image_path = "data/images/other/mine/01.png"

class PhysicsEntity:
    def __init__(self, game, origin, size=[8, 15], offset=[0, 0], pid=3):
        self.pos = list(origin)
        self.size = list(size)
        self.direction = [0, 0]
        self.velocity = [0, 0]
        self.offset = list(offset)
        self.image = pygame.Surface(self.size)
        self.gravity = GRAVITY
        self.collisions = {"top": False, "bottom": False, "left": False, "right": False}
        self.jumper = True
        self.has_gravity = False
        self.rotated = False
        self.rotate_request = "vert"
        self.current_rot = "vert"
        self.crouch = False
        #self.image = load_image(image_path)
        self.type = "force"
        self.id = 0
        self.health = 100
        self.pid = pid
        self.game = game
        self.ability = self.get_ability()
        self.count = 0
        self.count2 = 0
        self.pushed = True

    def get_collider(self):
        if not self.rotated:
            return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        else:
            return pygame.Rect(self.pos[0], self.pos[1], self.size[1], self.size[0])

    def get_ability(self):
        if self.type == "force":
            return ShinraTensei().copy()

    def activate_ability(self):
        if self.type == "force":
            ab = self.ability.copy()
            ab.push(self.get_collider().center)
            return [self.id, ab]
    
    def draw_collider(self, surf, offset=[0, 0], color="green"):
        temp = self.get_collider()
        rect = pygame.Rect(temp.x - self.offset[0] - offset[0], temp.y - self.offset[1] - offset[1], temp.w, temp.h)
        #pygame.draw.rect(self.image, color, rect)
        pygame.draw.rect(surf, color, rect)
        #pygame.draw.rect(self.image, color, temp)
        #surf.blit(self.image, rect)

    def rotate_rect(self, colliders):
        if self.rotate_request == "vert":
            self.rotated = False
        elif self.rotate_request == "hor":
            self.rotated = True
        rect = self.get_collider()
        for collider in colliders:
            if rect.colliderect(collider):
                if self.rotate_request == "vert":
                    self.rotated = True
                elif self.rotate_request == "hor":
                    self.rotated = False

    def move(self, movement, colliders):
        self.collisions = {"top": False, "bottom": False, "left": False, "right": False}
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])
        self.pos[1] += frame_movement[1]
        entity_rect = self.get_collider()
        for collider in colliders:
            if entity_rect.colliderect(collider):
                if frame_movement[1] > 0:
                    entity_rect.bottom = collider.top
                    self.collisions["bottom"] = True
                if frame_movement[1] < 0:
                    entity_rect.top = collider.bottom
                    self.collisions["top"] = True
                self.pos[1] = entity_rect.y
        
        self.pos[0] += frame_movement[0]
        entity_rect = self.get_collider()
        for collider in colliders:
            if entity_rect.colliderect(collider):
                if frame_movement[0] > 0:
                    entity_rect.right = collider.left
                    self.collisions["right"] = True
                if frame_movement[0] < 0:
                    entity_rect.left = collider.right
                    self.collisions["left"] = True
                self.pos[0] = entity_rect.x

        self.rotate_rect(colliders)
        if self.count > 5 and self.pushed:
            hor_push = True
        if self.count2 > 5 and self.pushed:
            vert_push = True
        if self.velocity[0] != 0:
            self.count += 1
        if self.count >= 25:
            self.velocity[0] = 0
            self.count = 0
        if self.velocity[1] == -3 or self.velocity[1] == 3:
            self.count2 += 1
        if self.count2 >= 25:
            self.velocity[1] = 0
            self.count2 = 0

        
        if self.has_gravity:
            if not self.collisions["bottom"]:
                self.velocity[1] = min(5, self.velocity[1] + self.gravity)
            if self.collisions["bottom"] or self.collisions["top"]:
                self.velocity[1] = 0

    def get_wasd_input(self):
        self.crouch = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.direction[0] = -1
        elif keys[pygame.K_d]:
            self.direction[0] = 1
        else:
            self.direction[0] = 0

        if self.jumper and self.has_gravity:
            if keys[pygame.K_w]:
                self.velocity[1] = jump_height  
            elif keys[pygame.K_s]:
                self.crouch = True
        else: 
            if keys[pygame.K_a] or keys[pygame.K_d]:
                self.rotate_request = "hor"
            elif keys[pygame.K_w] or keys[pygame.K_s]:
                self.rotate_request = "vert"
            else:
                self.rotate_request = "vert"
            if keys[pygame.K_w]:
                self.direction[1] = -1
            elif keys[pygame.K_s]:
                self.direction[1] = 1
            else:
                self.direction[1] = 0
        if keys[pygame.K_g]:
            self.game.abilities.append(self.activate_ability())
            
    def get_arrow_input(self):
        self.crouch = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.direction[0] = -1
        elif keys[pygame.K_RIGHT]:
            self.direction[0] = 1
        else:
            self.direction[0] = 0

        if self.jumper and self.has_gravity:
            if keys[pygame.K_UP]:
                self.velocity[1] = jump_height  
            elif keys[pygame.K_DOWN]:
                self.crouch = True
        else: 
            if keys[pygame.K_UP] or keys[pygame.K_DOWN]:
                self.rotate_request = "vert"
            elif keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
                self.rotate_request = "hor"
            else:
                self.rotate_request = "vert"
            if keys[pygame.K_UP]:
                self.direction[1] = -1
            elif keys[pygame.K_DOWN]:
                self.direction[1] = 1
            else:
                self.direction[1] = 0
        if keys[pygame.K_k]:
            self.game.abilities.append(self.activate_ability())

    def update(self, colliders, surf, offset=[0, 0]):
        if self.pid == 1:
            self.update1(colliders, surf, offset)
        elif self.pid == 2:
            self.update2(colliders, surf, offset)

    def update1(self, colliders, surf, offset=[0, 0]):
        self.get_wasd_input()
        self.move(movement=self.direction, colliders=colliders)
        self.draw_collider(surf, offset=offset)

    def update2(self, colliders, surf, offset=[0, 0]):
        self.get_arrow_input()
        self.move(movement=self.direction, colliders=colliders)
        self.draw_collider(surf, offset=offset)

    def change_gravity_status(self):
        self.has_gravity = not self.has_gravity
        self.rotate_request = "vert"
        self.velocity[1] = 0

    def get_damage(self, damage):
        self.health -= damage