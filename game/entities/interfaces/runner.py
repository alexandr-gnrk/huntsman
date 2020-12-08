from .gameobject import GameObject

import pygame


class Runner(GameObject):

    def run_away(self, target):
        desired = target - self.pos
        desired.scale_to_length(self.maxspeed)

        steer = desired - self.vel
        steer = self.vec_limit(steer, self.maxforce)
        steer = -steer
        return steer


    def run_away_objs(self, objs):
        sum_vec = pygame.Vector2(0, 0)
        amount = 0

        for obj in objects:
            dist = self.pos.distance_to(obj.pos)

            if dist > 0:
                diff_vec = self.pos - obj.pos
                diff_vec.normalize_ip()
                diff_vec /= dist

                sum_vec += diff_vec
                amount += 1

        if amount > 0:
            sum_vec /= amount
            sum_vec.normalize_ip()
            sum_vec *= self.maxspeed

            steer = sum_vec - self.vel
            steer = self.vec_limit(steer, self.maxforce)
            return steer
        else:
            return pygame.Vector2(0, 0)