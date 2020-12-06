from .interfaces import GameObject

import pygame


class Seeker(GameObject):

    def seek(self, target):
        desired = target - self.pos
        desired.scale_to_length(self.maxspeed)

        steer = desired - self.vel
        steer = self.vec_limit(steer, self.maxforce)
        self.apply_force(steer)

    def arrive(self, target, arrive_radius=500):
        desired = target - self.pos
        dist = desired.length()

        if dist < arrive_radius:
            print('Less', dist/arrive_radius)
            speed = (dist/arrive_radius)*self.maxspeed
            desired.scale_to_length(speed)
        else:
            print('More')
            desired.scale_to_length(self.maxspeed)

        steer = desired - self.vel
        steer = self.vec_limit(steer, self.maxforce)
        self.apply_force(steer)
