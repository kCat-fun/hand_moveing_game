import pygame

class Bullet:
    class Vec:
        def __init__(self, x, y):
            self.x = x
            self.y = y

        def add(self, vec):
            self.x += vec.x
            self.y += vec.y

    def __init__(self, x, y, vx, vy):
        self.pos = self.Vec(x, y)
        self.vec = self.Vec(vx, vy)
        self.radius = 10
        self.remove_flag = False

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (
                (self.pos.x),
                (self.pos.y),
            ),
            self.radius,
        )

    def update(self):
        self.pos.add(self.vec)
        if self.pos.y + self.radius/2.0 < 0:
            self.remove_flag = True

