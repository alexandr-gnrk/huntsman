from abc import ABC, abstractmethod

import pygame


class GameObject(ABC):
    """Interface of objects that could kill."""

    @abstractmethod
    def __init__(self, 
            pos=None, vel=None, acc=None,
            mass=1, 
            maxspeed=500, maxforce=500):
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
        force = pygame.Vector2(force)
        force.scale_to_length(force.length() / self.mass)
        self.acc += force

    def apply_friction(self, dt):
        friction = pygame.Vector2(self.vel)
        friction.scale_to_length(self.friction_magn * dt)
        self.vel -= pygame.Vector2(0, 0) if friction.length() >= self.vel.length() else friction


    def update(self, dt):
        # apply friction
        # print(self.friction * dt)
        # self.vel = self.vel.normalize() * self.friction * dt
        # print((self.vel.normalize() * self.friction_magn * dt).length())

        self.apply_friction(dt)

        print(self.vel.length())
        self.vel += self.acc * dt
        self.vel = self.vec_limit(self.vel, self.maxspeed)

        self.pos += self.vel * dt
        self.acc = pygame.Vector2(0, 0)
        print('pos:', self.pos, ', vel:', self.vel.length())

    @classmethod
    def vec_limit(cls, vec, limit):
        vec = pygame.Vector2(vec)
        if vec.length() >= limit:
            vec.scale_to_length(limit)
        return vec
