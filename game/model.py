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
        for i in range(5):
            self.objects.append(
                Hare((0, i), walls_rect=self.bounds))

        for i in range(10):
            self.objects.append(
                Deer((0, i), walls_rect=self.bounds))
            self.objects.append(
                Deer((0, i), family_id=1, walls_rect=self.bounds))
            self.objects.append(
                Deer((0, i), family_id=2, walls_rect=self.bounds))

        for i in range(2):
            self.objects.append(
                Wolf((200, 200), walls_rect=self.bounds))         

    def update(self, dt, target):
        """Updates game state."""
        for obj in self.objects:
            obj.update(self.objects, dt)

            if self.is_outside_bounds(obj):
                self.objects.remove(obj)

    def move(self, direction):
        if self.hunter.is_alive:
            self.hunter.move(direction)

    def is_outside_bounds(self, obj):
        if obj.pos.x < self.bounds[0].x or \
                obj.pos.x > self.bounds[1].x or \
                obj.pos.y > self.bounds[0].y or \
                obj.pos.y < self.bounds[1].y:
            return True
        return False

    def shoot(self, camera):
        if self.hunter.is_alive:
            mouse_pos = camera.to_pos(
                    pygame.Vector2(
                        pygame.mouse.get_pos()))
            direction =  mouse_pos - self.hunter.pos
            self.hunter.shoot(direction)

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