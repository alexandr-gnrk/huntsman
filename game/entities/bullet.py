import pygame

from .interfaces import GameObject

class Bullet(GameObject):

    def __init__(self, pos):
        super().__init__(
            pos=pos,
            radius=2,
            color=(0, 0, 0),
            )
        self.friction_magn = 0

    def update(self, objs, dt):
        super().update(dt)

    def draw(self, camera, surface, direction=None, triangle=False):
        super().draw(camera, surface, direction, triangle)