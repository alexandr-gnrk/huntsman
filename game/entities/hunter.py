import pygame

from .interfaces import GameObject

class Hunter(GameObject):

    MOVING_FORCE = 300

    def __init__(self, pos):
        super().__init__(
            pos=pos,
            radius=5,
            color=(255, 0, 0),
            )

    def update(self, objs, dt):
        super().update(dt)

    def move(self, direction):
        if direction.length() > 0:
            direction = pygame.Vector2(direction)
            direction.scale_to_length(self.MOVING_FORCE)
            print(direction)
            self.apply_force(direction)
