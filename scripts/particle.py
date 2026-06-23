import pygame
import random, math

class Particle:
    def __init__(self, pos, dir=[random.uniform(-1, 1), random.uniform(-1, 1)], speed=random.randint(1, 5), size=random.randint(10, 15)):
        self.dir = dir
        self.speed = speed
        self.size = size
        self.pos = list(pos)
        self.dead = False
        self.color = "white"

    def move(self):
        self.pos[0] += self.speed * self.dir[0]
        self.pos[1] += self.speed * self.dir[1]
        self.size = max(self.size - 0.1, 0)
        if self.size <= 0:
            self.dead = True
    
    def draw_circle(self, surf, offset=[0, 0]):
        pygame.draw.circle(surf, self.color, [int(self.pos[0] - offset[0]), int(self.pos[1] - offset[1])], self.size, 2)

    def update(self, surf, offset=[0, 0]):
        self.move()
        self.draw_circle(surf, offset=offset)
    
class Particles:
    def __init__(self, number, pos):
        self.particles = []
        for i in range(number):
            self.particles.append(Particle(pos, dir=[random.uniform(-1, 1), random.uniform(-1, 1)], speed=random.randint(1, 5), size=random.randint(10, 15)))
    
    def update(self, surf, offset=[0, 0]):
        for particle in self.particles:
            particle.update(surf, offset)
    

class Spark:
    def __init__(self, pos, dir, speed):        
            self.speed = speed
            self.dir = dir
            self.pos = list(pos)
            self.timer = random.randint(5, 10)
            self.angle = math.atan2(dir[1], dir[0])
            self.dead = False
            self.scale = 2
            self.color = random.choice(["aqua", "yellow"])

    def move(self):
        self.pos[0] += self.speed * self.dir[0]
        self.pos[1] += self.speed * self.dir[1]
        self.timer = max(self.timer - 0.1, 0)
        if self.timer <= 0:
            self.dead = True

    def draw(self, surf, offset=[0, 0]):
        points = [
            [self.pos[0] + math.cos(self.angle) * self.scale * 1.5 - offset[0], self.pos[1] + math.sin(self.angle) * self.scale * 1.5- offset[1]],
            [self.pos[0] + math.cos(self.angle + math.pi / 4) * self.scale - offset[0], self.pos[1] + math.sin(self.angle + math.pi / 4) * self.scale - offset[1]],
            [self.pos[0] - math.cos(self.angle) *  self.scale * self.speed * 3 - offset[0], self.pos[1] - math.sin(self.angle) *  self.scale * self.speed  * 3 - offset[1]],
            [self.pos[0] + math.cos(self.angle - math.pi / 4) * self.scale - offset[0],self.pos[1] + math.sin(self.angle - math.pi / 4) * self.scale - offset[1]]
        ]
        pygame.draw.polygon(surf, self.color, points)
    
    def update(self, surf, offset=[0, 0]):
        self.move()
        self.draw(surf, offset=offset)

class Demo:
    def __init__(self, pos, angle, speed):
        self.pos = list(pos)
        self.angle = angle
        self.speed = speed
        self.timer = 10
        self.dead = False

    def move(self):
        self.pos[0] += math.cos(self.angle) * self.speed
        self.pos[1] += math.sin(self.angle) * self.speed
        self.timer = max(self.timer-0.1, 0)
        if self.timer <= 0:
            self.dead = True

    def draw(self, surf):
        pygame.draw.circle(surf, "red", [int(self.pos[0]), int(self.pos[1])], self.timer)

    def update(self, surf):
        self.move()
        self.draw(surf)

class Trail:
    def __init__(self, pos, size, fade=0.1, color="lime"):
        self.color = color
        self.pos = list(pos)
        self.size = size
        self.fade = fade
        self.dead = False

    def trail(self):
        self.size = max(self.size - self.fade, 0)
        if self.size <= 0: 
            self.dead = True

    def draw(self, surf, offset=[0, 0]):
        pygame.draw.circle(surf, self.color, [int(self.pos[0] - offset[0]), int(self.pos[1] - offset[1])], int(self.size))
    
    def update(self, surf, offset=[0, 0]):
        self.trail()
        self.draw(surf=surf, offset=offset)


class Shockwave:
    def __init__(self, pos, size=2, width=5, color="magenta"):
        self.pos = list(pos)
        self.size = size
        self.width = width
        self.color = color
        self.dead = False

    def wave(self):
        self.size += 1
        self.width = max(self.width - 0.1, 1)
        if self.width <= 1:
            self.dead = True

    def draw(self, surf, offset=[0, 0]):
        pygame.draw.circle(surf, self.color, [int(self.pos[0] - offset[0]), int(self.pos[1] - offset[1])], int(self.size), int(self.width))

    def update(self, surf, offset=[0, 0]):
        self.wave()
        self.draw(surf=surf, offset=offset)



class Anchor:
    def __init__(self, pos, radius, anchored=False):
        self.pos = list(pos)
        self.radius = radius
        self.anchored = anchored

    def get_anchor(self, anchor):
        self.anchor = anchor
        self.anchored = True

    def update(self, surf, offset=[0, 0]):
        if self.anchored:
            '''
            self.anchor.pos = list(self.anchor.pos)
            x = -(self.pos[0] - (self.anchor.pos[0]))
            y = -(self.pos[1] - (self.anchor.pos[1]))
            #x = max(self.pos[0] , (self.anchor.pos[0])) - min(self.pos[0] , (self.anchor.pos[0]))
            #y = max(self.pos[1] , (self.anchor.pos[1])) - min(self.pos[1] , (self.anchor.pos[1]))
            rad = math.sqrt(self.radius**2 + self.radius ** 2)
            angle = math.atan2(y, x)
            #self.pos[0] = int(math.cos(angle) * rad)
            #self.pos[1] = int(math.sin(angle) * rad)
            self.pos[0] = int(math.cos(angle) * self.radius)
            self.pos[1] = int(math.sin(angle) * self.radius)
            #self.pos[0] += int(math.cos(angle) * 2)
            #self.pos[1] += int(math.sin(angle) * 2)
            pygame.draw.line(surf, "green", self.anchor.pos, self.pos, 2)
            '''
            x = -(self.pos[0] - (self.anchor.pos[0]))
            y = -(self.pos[1] - (self.anchor.pos[1]))
            angle = math.atan2(y, x)
            s = 2
            if self.anchor.pos[0] > self.pos[0]:
                if self.pos[0] < self.anchor.pos[0] - self.anchor.radius:
                    self.pos[0] += math.cos(angle) * s
            elif self.anchor.pos[0] < self.pos[0]:
                if self.pos[0] < self.anchor.pos[0] + self.anchor.radius:
                    self.pos[0] -= math.cos(angle) * s
            if self.anchor.pos[1] > self.pos[1]:
                if self.pos[1] < self.anchor.pos[1] - self.anchor.radius:
                    self.pos[1] += math.sin(angle) * s
            elif self.anchor.pos[1] < self.pos[1]:
                if self.pos[1] > self.anchor.pos[1] + self.anchor.radius:
                    self.pos[1] -= math.sin(angle) * s
            '''
            '''
            if self.anchor.pos[1] > self.pos[1]:
                self.pos[1] = self.anchor.pos[1] - self.anchor.radius
            elif self.anchor.pos[1] < self.pos[1]:
                self.pos[1] = self.anchor.pos[1] + self.anchor.radius
        

        pygame.draw.circle(surf, "aqua", [self.pos[0] - offset[0], self.pos[1] - offset[1]], 3, 2)
        pygame.draw.circle(surf, "yellow", [self.pos[0] - offset[0], self.pos[1] - offset[1]], self.radius, 2)
        if self.anchored:
            print(f"{self.anchor.pos}, myp: {self.pos}")
            pygame.draw.line(surf, "red", self.anchor.pos, self.pos)
            #pygame.draw.line(surf, "blue", self.anchor.pos[1], self.pos[1])

