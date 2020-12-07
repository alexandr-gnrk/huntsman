import random

import pygame

from .interfaces import GameObject


class Wanderer(GameObject):

    # degrees per second
    ANGLE_CHANGE_SPEED = 45*12
    WANDER_DISTANCE_RANGE = (65, 100)
    WANDER_RADIUS_RANGE = (50, 60)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.wander_angle = 0
        self.wander_distance = random.randint(*self.WANDER_DISTANCE_RANGE)
        self.wander_radius = random.randint(*self.WANDER_RADIUS_RANGE)
        # self.wander_distance = 70
        # self.wander_radius = 50

    def wander(self, dt):
        delta_angle = self.ANGLE_CHANGE_SPEED*dt
        is_add_angle = random.choice([True, False])

        if is_add_angle:
            self.wander_angle += delta_angle
        else:
            self.wander_angle -= delta_angle

        delta_pos = self.direction()
        delta_pos.scale_to_length(self.wander_distance)
        future_pos = self.pos + delta_pos

        wander_radius_vec = self.direction().rotate(self.wander_angle)
        wander_radius_vec.scale_to_length(self.wander_radius)
        target = future_pos + wander_radius_vec

        desired = target - self.pos
        desired.scale_to_length(self.maxspeed)

        steer = desired - self.vel
        steer = self.vec_limit(steer, self.maxforce)
        self.apply_force(steer)

        # pygame.draw.line(
        #     screen, 
        #     (255, 0, 0),
        #     camera.adjust(self.pos),
        #     camera.adjust(future_pos),
        #     )
        # pygame.draw.circle(
        #     screen, 
        #     (255, 0, 0),
        #     camera.adjust(future_pos),
        #     self.wander_radius,
        #     width=1)
        # pygame.draw.line(
        #     screen, 
        #     (255, 0, 0),
        #     camera.adjust(future_pos),
        #     camera.adjust(future_pos + wander_radius_vec),
        #     )