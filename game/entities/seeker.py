from .gameobject import GameObject

import pygame


class Seeker(GameObject):

    def seek(self, target):
        desired = target - self.pos
        desired.scale_to_length(self.maxspeed)

        steer = desired - self.vel
        steer = self.vec_limit(steer, self.maxforce)
        self.apply_force(steer)