import pygame
import random

from .entities import Circle


class Model():
    """Class that represents game state."""

    def __init__(self, bounds=(
                pygame.Vector2(-450, 300),
                pygame.Vector2(450, -300))):
        # means that size of world is [-world_size, world_size] 
        self.bounds = bounds
        self.objs = list()
        for i in range(100):
            self.objs.append(
                Circle((0, i), (1, 0), (0, 0), 5, (255, 0, 0))
                )

    def update(self, dt, target):
        """Updates game state."""
        for obj in self.objs:
            # obj.run_away(
            #     self.camera.to_pos(
            #         pygame.Vector2(
            #             pygame.mouse.get_pos())))

            # obj.wander(self.delta_time(), self.screen, self.camera)
     
            # obj.wander(dt)
            obj.seek(target)
            obj.wach_out_wall()
            obj.separate(self.objs)
            obj.align(self.objs)
            obj.cohase(self.objs)
            obj.update(dt)

    def draw(self, camera, surface):
        """Spawn passed amount of cells on the field."""
        for obj in self.objs:
            obj.draw(camera, surface)
    