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

class Sparks:
    def __init__(self, pos, ranges, speed):
        self.x_range = ranges[0]
        self.y_range = ranges[1]
        self.speed = speed
        self.pos = list(pos)
        self.sparks = []

    def add_spark(self):
        self.sparks.append(Spark(self.pos, [random.randint(1, self.speed) * self.x_range, random.randint(1, self.speed) * self.y_range], self.speed))
    
    def update(self, surf, offset=[0, 0]):
        for spark in self.sparks:
            spark.update(surf, offset)

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
    def __init__(self, pos, size: int | float, fade=0.1, color="lime"):
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

class Trails:
    def __init__(self, size: int | float = 5, fade: float=0.1, color: str | tuple="lime"):
        self.trails : list = []
        self.color = color
        self.fade = fade
        self.size = size

    def follow(self, pos):
        self.trails.append(Trail(pos, self.size, self.fade, self.color))
    
    def update(self, pos, surf, offset=[0, 0]):
        self.follow(list(pos))
        for trail in self.trails:
            trail.update(surf, offset)

class Shockwave:
    def __init__(self, pos, size=2, width=5, color="magenta", speed=0.1):
        self.pos = list(pos)
        self.size = size
        self.width = width
        self.color = color
        self.dead = False
        self.speed = speed

    def wave(self):
        self.size += 1
        self.width = max(self.width - self.speed, 1)
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

class RingWave:
    """
    Two concentric rings that grow and die together, sized so that:
      - the OUTER ring starts at the center and ends at the
        circumscribed radius of a `square_size` square  (S / sqrt(2))
      - the INNER ring starts at the inscribed radius (S / 2) and ends
        at the same circumscribed radius
    Net effect: any point inside the square is already visually inside
    the inner ring at t=0, so a rect-based hit never looks like it
    came out of nowhere, and both rings finish exactly on the corners.
    """

    _INV_SQRT2 = 0.7071067811865476

    def __init__(self, pos, square_size,
                 outer_color="aqua", inner_color="white",
                 lifetime=16, outer_thickness=8, inner_thickness=5):
        self.pos = list(pos)
        self.square_size = float(square_size)
        self.lifetime = max(1, int(lifetime))
        self.age = 0
        self.dead = False

        # --- the geometry -------------------------------------------------
        self.r_final       = self.square_size * self._INV_SQRT2   # ≈ 0.7071 * S
        self.r_start_inner = self.square_size * 0.5               # = 0.5000 * S
        self.r_start_outer = 0.0
        # ------------------------------------------------------------------

        self.outer_color     = outer_color
        self.inner_color     = inner_color
        self.outer_thickness = float(outer_thickness)
        self.inner_thickness = float(inner_thickness)

        # legacy attrs so any code reading .size / .width still works
        self.size  = 0
        self.width = int(self.outer_thickness)

    # --- shape at the current age ----------------------------------------
    def _t(self):
        return min(self.age / self.lifetime, 1.0)

    def _outer_radius(self):
        return self.r_start_outer + (self.r_final - self.r_start_outer) * self._t()

    def _inner_radius(self):
        return self.r_start_inner + (self.r_final - self.r_start_inner) * self._t()

    def _stroke(self, base):
        return max(1, int(round(base * (1.0 - self._t()))))

    # --- Shockwave-compatible API ----------------------------------------
    def draw(self, surf, offset=[0, 0]):
        cx = int(self.pos[0] - offset[0])
        cy = int(self.pos[1] - offset[1])
        # inner ring first so the brighter one sits on top
        pygame.draw.circle(surf, self.inner_color, (cx, cy),
                           int(self._inner_radius()),
                           self._stroke(self.inner_thickness))
        pygame.draw.circle(surf, self.outer_color, (cx, cy),
                           int(self._outer_radius()),
                           self._stroke(self.outer_thickness))

    def update(self, surf, offset=[0, 0]):
        self.draw(surf, offset=offset)
        self.age += 1
        self.size  = int(self._outer_radius())
        self.width = self._stroke(self.outer_thickness)
        if self.age > self.lifetime:
            self.dead = True

