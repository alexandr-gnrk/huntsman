import pygame
import random

from .entities import Hare, Deer, Wolf, Hunter


class Model():
    """Class that represents game state."""

    def __init__(self, bounds=(
                pygame.Vector2(-450, 300),
                pygame.Vector2(450, -300))):
        # means that size of world is [-world_size, world_size] 
        self.bounds = bounds

        self.hunter = Hunter((0, 0))
        
        self.objects = [self.hunter]

        # self.objects = list()
        for i in range(1):
            self.objects.append(
                Hare((0, i), walls_rect=self.bounds))

        for i in range(10):
            self.objects.append(
                Deer((0, i), walls_rect=self.bounds))
            self.objects.append(
                Deer((0, i), family_id=1, walls_rect=self.bounds))

        for i in range(1):
            self.objects.append(
                Wolf((200, 200), walls_rect=self.bounds))         


    def update(self, dt, target):
        """Updates game state."""
        for obj in self.objects:
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
            obj.update(self.objects, dt)

        if self.hunter.is_alive:
            self.hunter.update(self.objects, dt)

    def move(self, direction):
        if self.hunter.is_alive:
            self.hunter.move(direction)


    def draw(self, camera, surface):
        """Spawn passed amount of cells on the field."""
        for obj in self.objects:
            if isinstance(obj, Hunter):
                target = camera.to_pos(
                    pygame.Vector2(
                        pygame.mouse.get_pos()))
                obj.draw(camera, surface, target - obj.pos)
                continue

            obj.draw(camera, surface)    