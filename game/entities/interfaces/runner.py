from .gameobject import GameObject

import pygame


class Runner(GameObject):

    def run_away(self, target):
        desired = target - self.pos
        desired.scale_to_length(self.maxspeed)

        steer = desired - self.vel
        steer = self.vec_limit(steer, self.maxforce)
        steer = -steer
        self.apply_force(steer)