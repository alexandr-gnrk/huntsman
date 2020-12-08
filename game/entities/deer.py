import pygame

from .interfaces import Wanderer, FlockMember, WallCoward
from .wolf import Wolf

class Deer(Wanderer, FlockMember, WallCoward):

    VIEW_RADIUS = 100
    DESIRED_SEPARATION = 20
    ALIGN_RADIUS = 50
    COHESION_RADIUS = 1000

    def __init__(self, pos, family_id=0, **kwargs):
        super().__init__(
            pos=pos,
            radius=5,
            color=(102, 51, 0),
            **kwargs)
        self.family_id = family_id

    def update(self, objs, dt):
        family = list()
        predators = list()
        for obj in objs:
            if isinstance(obj, Deer) and obj.family_id == self.family_id:
                family.append(obj)
            elif isinstance(obj, Wolf):
                predators.append(obj)

        wander = self.wander(dt)
        separate_predators = self.separate(predators, self.VIEW_RADIUS)
        separate = self.separate(family, self.DESIRED_SEPARATION)
        align = self.align(family, self.ALIGN_RADIUS)
        cohase = self.cohase(family, self.COHESION_RADIUS)
        walls = self.wach_out_wall()

        self.apply_force(wander*0.2)
        if separate_predators.length() > 0:
            self.apply_force(separate_predators*2)
        else:
            self.apply_force(separate*3)
            self.apply_force(align)
            self.apply_force(cohase)
    
        self.apply_force(walls*2)

        super().update(dt)