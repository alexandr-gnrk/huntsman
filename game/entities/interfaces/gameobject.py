import math

from abc import ABC, abstractmethod

import pygame


class GameObject(ABC):
    """Interface of objects that could kill."""

    @abstractmethod
    def __init__(self, 
            pos, radius, color,
            mass=1, 
            maxspeed=500, maxforce=1000):
        # positon, velocity and acceleration
        self.pos = pygame.Vector2(pos) if pos else pygame.Vector2(0, 0)
        self.vel = pygame.Vector2(0, 0)
        self.acc =  pygame.Vector2(0, 0)
        self.maxspeed = maxspeed
        self.maxforce = maxforce
        self.mass = mass
        self.friction_magn = 100
        self.is_alive = True
        self.radius = radius
        self.color = color


    def draw(self, camera, surface, direction=None, triangle=True):
        if not triangle:
            pygame.draw.circle(
                surface,
                self.color,
                camera.adjust(self.pos),
                self.radius)
            return

        # length of equilateral triangle
        side_len = (3*self.radius)/math.sqrt(3)

        point1 = direction if direction else self.direction()
        point1.scale_to_length(self.radius)

        point2 = pygame.Vector2(point1).rotate(150)
        point2.scale_to_length(side_len)

        point3 = pygame.Vector2(point2).rotate(60)
        point3.scale_to_length(side_len)

        point1 += self.pos
        point2 += self.pos
        point3 += self.pos

        points = (
                camera.adjust(point1), 
                camera.adjust(point2), 
                camera.adjust(point3))
        pygame.draw.polygon(
            surface, 
            self.color, 
            points,
            width=0)
        pygame.draw.polygon(
            surface, 
            self.to_border_color(self.color), 
            points,
            width=1)
    
    def apply_force(self, force):
        force_cp = self.safe_normalize(force)
        force_cp.scale_to_length(force.length() / self.mass)
        self.acc += force_cp

    def apply_friction(self, dt):
        friction = self.direction()
        friction.scale_to_length(self.friction_magn * dt)
        self.vel = pygame.Vector2(0, 0) if friction.length() >= self.vel.length() else self.vel - friction

    def kill(self):
        self.is_alive = False

    def update(self, dt):
        self.apply_friction(dt)

        self.vel += self.acc * dt
        self.vel = self.vec_limit(self.vel, self.maxspeed)

        self.pos += self.vel * dt
        self.acc = pygame.Vector2(0, 0)

    def is_collide(self, obj):
        if self.pos.distance_to(obj.pos) < self.radius + obj.radius:
            return True
        return False

    def direction(self):
        return self.safe_normalize(self.vel)

    def safe_normalize(self, vec):
        try:
            return vec.normalize()
        except ValueError:
            return pygame.Vector2(0, 1)

    @classmethod
    def to_border_color(cls, color):
        mult = 0.8
        return [part*mult for part in color]

    @classmethod
    def vec_limit(cls, vec, limit):
        vec = pygame.Vector2(vec)
        if vec.length() >= limit:
            vec.scale_to_length(limit)
        return vec
