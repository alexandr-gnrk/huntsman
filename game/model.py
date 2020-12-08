import pygame
import random

from .entities import Hare, Deer, Wolf, Hunter


class Model():
    """Class that represents game state."""

    def __init__(self, world_size, hares, wolves, deer_families):
        # means that size of world is [-world_size, world_size] 
        self.bounds = (
            pygame.Vector2(-world_size[0]/2, world_size[1]/2),
            pygame.Vector2(world_size[0]/2, -world_size[1]/2))

        self.hunter = Hunter((0, 0))
        
        self.objects = [self.hunter]

        self.spawn_hares(hares)
        self.spawn_deer_families(deer_families, (3, 10))
        self.spawn_wolves(wolves)

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

    def spawn_hares(self, amount):
        for i in range(amount):
            pos = self.get_random_pos()
            self.objects.append(
                Hare(pos, walls_rect=self.bounds))

    def spawn_deer_families(self, families_amount, flock_size_range):
        for family_id in range(families_amount):
            pos = self.get_random_pos()
            flock_size = random.randint(*flock_size_range)
            for j in range(flock_size):
                self.objects.append(
                    Deer(pos, family_id=family_id, walls_rect=self.bounds))

    def spawn_wolves(self, amount):
        for i in range(amount):
            pos = self.get_random_pos()
            self.objects.append(
                Wolf(pos, walls_rect=self.bounds))

    def get_random_pos(self):
        x = random.randint(
            self.bounds[0].x,
            self.bounds[1].x)
        y = random.randint(
            self.bounds[1].y,
            self.bounds[0].y)
        return pygame.Vector2(x, y)