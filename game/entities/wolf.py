import pygame

from .interfaces import Wanderer, WallCoward, Seeker

class Wolf(Seeker, Wanderer, WallCoward):

    VIEW_RADIUS = 100
    KILL_DISTANCE = 8
    STARVATION_SPEED = 3

    def __init__(self, pos, **kwargs):
        super().__init__(
            pos=pos,
            radius=4,
            color=(0, 0, 0),
            **kwargs)
        self.helth = 100

    def update(self, objs, dt):
        self.update_helth(dt)
        if self.helth <= 0:
            objs.remove(self)
            return

        min_dist = float('inf')
        prey = None
        for obj in objs:
            if not isinstance(obj, Wolf):
                dist = self.pos.distance_to(obj.pos)
                if dist < self.KILL_DISTANCE:
                    obj.kill()
                    objs.remove(obj)
                    self.helth = 100
                elif dist < self.VIEW_RADIUS and dist < min_dist:
                    min_dist = dist
                    prey = obj

        wander = self.wander(dt)
        walls = self.wach_out_wall()

        if prey:
            seek = self.seek(prey.pos)
            self.apply_force(seek*2)
        else:
            self.apply_force(wander*0.3)
    
        self.apply_force(walls*2)

        super().update(dt)

    def update_helth(self, dt):
        self.helth -= self.STARVATION_SPEED*dt