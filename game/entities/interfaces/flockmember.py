from .seeker import Seeker

import pygame


class FlockMember(Seeker):

    DESIRED_SEPARATION = 20
    ALIGN_RADIUS = 50
    COHESION_RADIUS = 50

    def separate(self, objects, desired_separation=DESIRED_SEPARATION):
        sum_vec = pygame.Vector2(0, 0)
        amount = 0

        for obj in objects:
            dist = self.pos.distance_to(obj.pos)

            if dist > 0 and dist < desired_separation:
                diff_vec = self.pos - obj.pos
                diff_vec.normalize_ip()
                diff_vec /= dist

                sum_vec += diff_vec
                amount += 1

        # if amount > 0:
        if sum_vec.length() > 0:
            sum_vec /= amount
            sum_vec.normalize_ip()
            sum_vec *= self.maxspeed

            steer = sum_vec - self.vel
            steer = self.vec_limit(steer, self.maxforce)
            return steer
        else:
            return pygame.Vector2(0, 0)


        # desired = target - self.pos
        # desired.scale_to_length(self.maxspeed)

        # steer = desired - self.vel
        # steer = self.vec_limit(steer, self.maxforce)
        # steer = -steer
        # self.apply_force(steer)

    def align(self, objects, align_radius=ALIGN_RADIUS):
        amount = 0
        sum_vec = pygame.Vector2(0, 0)
        for obj in objects:
            dist = self.pos.distance_to(obj.pos)

            if dist > 0 and dist < align_radius:
                sum_vec += obj.vel
                amount += 1

        # if amount > 0:
        if sum_vec.length() > 0:
            sum_vec /= amount

            sum_vec.scale_to_length(self.maxspeed)

            steer = sum_vec - self.vel
            steer = self.vec_limit(steer, self.maxforce)
            return steer
        else:
            return pygame.Vector2(0, 0)

    def cohase(self, objects, cohesion_radius=COHESION_RADIUS):
        sum_vec = pygame.Vector2(0, 0)
        amount = 0

        for obj in objects:
            dist = self.pos.distance_to(obj.pos)

            if dist > 0 and dist < cohesion_radius:
                sum_vec += obj.pos
                amount += 1

        # if amount > 0:
        if sum_vec.length() > 0:
            sum_vec /= amount
            return self.seek(sum_vec)
        else:
            return pygame.Vector2(0, 0)