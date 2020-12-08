import pygame
import random

from .entities import Hare, Deer, Wolf


class Model():
    """Class that represents game state."""

    def __init__(self, bounds=(
                pygame.Vector2(-450, 300),
                pygame.Vector2(450, -300))):
        # means that size of world is [-world_size, world_size] 
        self.bounds = bounds
        
        self.animals = list()

        self.animals.extend([Hare((0, i), ) for i in range(1)])

        self.animals.extend([Deer((0, i)) for i in range(10)])
        self.animals.extend([Deer((0, i), family_id=1) for i in range(20)])

        self.animals.extend([Wolf((200, 200)) for i in range(1)])



    def update(self, dt, target):
        """Updates game state."""
        for obj in self.animals:
            # obj.run_away(
            #     self.camera.to_pos(
            #         pygame.Vector2(
            #             pygame.mouse.get_pos())))

            # obj.wander(self.delta_time(), self.screen, self.camera)
     
            # obj.apply_force(obj.wander(dt))
            # obj.apply_force(obj.seek(target))
            # obj.apply_force(obj.wach_out_wall())
            # obj.apply_force(obj.separate(self.objs) * 3)
            # obj.apply_force(obj.align(self.objs))
            # obj.apply_force(obj.cohase(self.objs))
            # obj.update(dt)
            obj.update(self.animals, dt)

    def draw(self, camera, surface):
        """Spawn passed amount of cells on the field."""
        for obj in self.animals:
            obj.draw(camera, surface)
    