import pygame

from .interfaces import Animal, Wanderer, WallCoward, Seeker

class Wolf(Animal, Seeker, Wanderer, WallCoward):

    VIEW_RADIUS = 100
    KILL_DISTANCE = 8
    STARVATION_SPEED = 10

    def __init__(self, pos):
        super().__init__(
            pos=pos,
            vel=pygame.Vector2(0, 0),
            acc=pygame.Vector2(0, 0),
            radius=4,
            color=(255, 0, 0),
            )
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
            self.apply_force(wander)
    
        self.apply_force(walls)

        super().update(dt)

    def update_helth(self, dt):
        self.helth -= self.STARVATION_SPEED*dt