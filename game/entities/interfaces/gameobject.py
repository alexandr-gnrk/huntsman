from abc import ABC, abstractmethod

import pygame


class GameObject(ABC):
    """Interface of objects that could kill."""

    @abstractmethod
    def __init__(self, 
            pos=None, vel=None, acc=None,
            mass=1, 
            maxspeed=500, maxforce=1000):
        # positon, velocity and acceleration
        self.pos = pygame.Vector2(pos) if pos else pygame.Vector2(0, 0)
        self.vel = pygame.Vector2(vel) if vel else pygame.Vector2(0, 0)
        self.acc = pygame.Vector2(acc) if acc else pygame.Vector2(0, 0)
        self.maxspeed = maxspeed
        self.maxforce = maxforce
        self.mass = mass
        self.friction_magn = 100

    @abstractmethod
    def draw(self, camera, surface):
        """Draw cuurrent object on passed surface."""
        pass
    
    def apply_force(self, force):
        force_cp = self.safe_normalize(force)
        force_cp.scale_to_length(force.length() / self.mass)
        self.acc += force_cp

    def apply_friction(self, dt):
        friction = self.direction()
        friction.scale_to_length(self.friction_magn * dt)
        self.vel = pygame.Vector2(0, 0) if friction.length() >= self.vel.length() else self.vel - friction

    def update(self, dt):
        self.apply_friction(dt)

        self.vel += self.acc * dt
        self.vel = self.vec_limit(self.vel, self.maxspeed)

        self.pos += self.vel * dt
        self.acc = pygame.Vector2(0, 0)

        # self.pos = pygame.Vector2(self.pos.x % 900, self.pos.y % 600)

    def direction(self):
        return self.safe_normalize(self.vel)

    def safe_normalize(self, vec):
        try:
            return vec.normalize()
        except ValueError:
            return pygame.Vector2(0, 1)

    @classmethod
    def vec_limit(cls, vec, limit):
        vec = pygame.Vector2(vec)
        if vec.length() >= limit:
            vec.scale_to_length(limit)
        return vec
