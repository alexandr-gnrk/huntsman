import pygame

from .interfaces import Animal, Wanderer, FlockMember, WallCoward


class Hare(Animal, Wanderer, FlockMember, WallCoward):

    VIEW_RADIUS = 100

    def __init__(self, pos):
        super().__init__(
            pos=pos,
            vel=pygame.Vector2(0, 0),
            acc=pygame.Vector2(0, 0),
            radius=3,
            color=(255, 0, 0))

    def update(self, objs, dt):
        wander = self.wander(dt)
        separate = self.separate(objs, self.VIEW_RADIUS)
        walls = self.wach_out_wall()        
        
        self.apply_force(wander*0.4)
        self.apply_force(separate)
        self.apply_force(walls)

        super().update(dt)