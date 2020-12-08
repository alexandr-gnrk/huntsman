import pygame

from .interfaces import Wanderer, FlockMember, WallCoward


class Hare(Wanderer, FlockMember, WallCoward):

    VIEW_RADIUS = 100

    def __init__(self, pos, **kwargs):
        super().__init__(
            pos=pos,
            radius=4,
            color=(153, 153, 102),
            **kwargs)

    def update(self, objs, dt):
        wander = self.wander(dt)
        separate = self.separate(objs, self.VIEW_RADIUS)
        walls = self.wach_out_wall()        
        
        self.apply_force(wander*0.4)
        self.apply_force(separate)
        self.apply_force(walls*2)

        super().update(dt)