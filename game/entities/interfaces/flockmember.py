from .seeker import Seeker

import pygame


class FlockMember(Seeker):

    DESIRED_SEPARATION = 20
    COHASION_RADIUS = 150
    ALIGN_RADIUS = 50
    COHESION_RADIUS = 50

    def separate(self, objects):
        sum_vec = pygame.Vector2(0, 0)
        amount = 0

        for obj in objects:
            dist = self.pos.distance_to(obj.pos)

            if dist > 0 and dist < self.DESIRED_SEPARATION:
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
            self.apply_force(steer)


        # desired = target - self.pos
        # desired.scale_to_length(self.maxspeed)

        # steer = desired - self.vel
        # steer = self.vec_limit(steer, self.maxforce)
        # steer = -steer
        # self.apply_force(steer)

    def align(self, objects):
        amount = 0
        sum_vec = pygame.Vector2(0, 0)
        for obj in objects:
            dist = self.pos.distance_to(obj.pos)

            if dist > 0 and dist < self.ALIGN_RADIUS:
                sum_vec += obj.vel
                amount += 1

        if amount > 0:
            sum_vec /= amount

            sum_vec.scale_to_length(self.maxspeed)

            steer = sum_vec - self.vel
            steer = self.vec_limit(steer, self.maxforce)
            self.apply_force(steer)

    def cohase(self, objects):
        sum_vec = pygame.Vector2(0, 0)
        amount = 0

        for obj in objects:
            dist = self.pos.distance_to(obj.pos)

            if dist > 0 and dist < self.COHASION_RADIUS:
                sum_vec += obj.pos
                amount += 1

        if amount > 0:
            sum_vec /= amount
            self.seek(sum_vec)