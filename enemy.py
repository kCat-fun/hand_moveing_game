import pygame

class Enemy:
    class Vec:
        def __init__(self, x, y):
            self.x = x
            self.y = y

        def add(self, vec):
            self.x += vec.x
            self.y += vec.y

    def __init__(self, x, y, vx, vy):
        self.radius = 20
        self.pos = self.Vec(x, y-self.radius)
        self.vec = self.Vec(vx, vy)

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            (255, 50, 50),
            (
                (self.pos.x),
                (self.pos.y),
            ),
            self.radius,
        )

    def update(self):
        self.pos.add(self.vec)