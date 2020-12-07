from .gameobject import GameObject

import pygame


class Seeker(GameObject):

    def seek(self, target):
        desired = target - self.pos
        desired.scale_to_length(self.maxspeed)

        steer = desired - self.vel
        steer = self.vec_limit(steer, self.maxforce)
        return steer

    def arrive(self, target, arrive_radius=300):
        desired = target - self.pos
        dist = desired.length()
        print('Dist:', dist)

        if dist < arrive_radius:
            print('Less', dist/arrive_radius)
            speed = (dist/arrive_radius)*self.maxspeed
            desired.scale_to_length(speed)
        else:
            print('More')
            desired.scale_to_length(self.maxspeed)

        steer = desired - self.vel
        print('Force before', steer.length())
        steer = self.vec_limit(steer, self.maxforce)
        print('Force after', steer.length())
        return steer
