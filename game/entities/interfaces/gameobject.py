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

    @abstractmethod
    def draw(self, camera, surface):
        """Draw cuurrent object on passed surface."""
        pass
    
    def apply_force(self, force):
        force = pygame.Vector2(force)
        force.scale_to_length(force.length() / self.mass)
        self.acc += force

    def update(self, dt):
        self.vel += self.acc * dt
        self.vel = self.vec_limit(self.vel, self.maxspeed)
        self.pos += self.vel * dt
        self.acc = pygame.Vector2(0, 0)

    @classmethod
    def vec_limit(cls, vec, limit):
        vec = pygame.Vector2(vec)
        if vec.length() >= limit:
            vec.scale_to_length(limit)
        return vec
