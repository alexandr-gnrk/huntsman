import pygame

from .interfaces import GameObject
from .bullet import Bullet

class Hunter(GameObject):

    MOVING_FORCE = 300
    BULLET_SPEED = 500
    SHOOT_DISTANCE = 400

    BULLET_SPREAD = 3 # in degrees

    def __init__(self, pos):
        super().__init__(
            pos=pos,
            radius=7,
            # color=(255, 0, 0),
            # color=(204, 51, 0),
            color=(204, 0, 0),
            # color=(255, 102, 0),
            # color=(255, 51, 0),
            )
        self.bullets_left = 100
        self.killed = 0
        self.bullets = list()

    def update(self, objs, dt):
        for bullet in self.bullets:
            bullet.update(objs, dt)

            if self.pos.distance_to(bullet.pos) > self.SHOOT_DISTANCE:
                self.bullets.remove(bullet)
                continue

            for obj in objs:
                if bullet.is_collide(obj) and not isinstance(obj, Hunter):
                    objs.remove(obj)
                    self.killed += 1
            
        super().update(dt)

    def move(self, direction):
        if direction.length() > 0:
            direction = pygame.Vector2(direction)
            direction.scale_to_length(self.MOVING_FORCE)
            self.apply_force(direction)

    def draw(self, camera, surface, direction=None, triangle=True):
        for bullet in self.bullets:
            bullet.draw(camera, surface)

        super().draw(camera, surface, direction, triangle)

    def shoot(self, direction, shootgun=True):
        if self.bullets_left > 0:
            magazine = list()
            bullet = self.make_bullet(direction)
            magazine.append(bullet)
            self.bullets_left -= 1

            if shootgun and self.bullets_left >= 2:
                bullet = self.make_bullet(direction)
                bullet.vel.rotate_ip(self.BULLET_SPREAD)
                magazine.append(bullet)

                bullet = self.make_bullet(direction)
                bullet.vel.rotate_ip(-self.BULLET_SPREAD)
                magazine.append(bullet)

                self.bullets_left -=2

            self.bullets.extend(magazine)

    def make_bullet(self, direction):
        bullet = Bullet(self.pos)
        vel = pygame.Vector2(direction)
        vel.scale_to_length(self.BULLET_SPEED)
        bullet.vel = vel
        return bullet