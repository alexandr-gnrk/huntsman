import math

import pygame

from .seeker import Seeker


class Circle(Seeker):

    def __init__(self, pos, vel, acc, radius, color):
        # radius and color
        super().__init__(pos, vel, acc)
        self.radius = radius
        self.color = color

    def draw(self, camera, surface):
        # length of equilateral triangle
        side_len = (3*self.radius)/math.sqrt(3)

        point1 = pygame.Vector2(self.vel)
        point1.scale_to_length(self.radius)

        point2 = pygame.Vector2(point1).rotate(150)
        point2.scale_to_length(side_len)

        point3 = pygame.Vector2(point2).rotate(60)
        point3.scale_to_length(side_len)

        point1 += self.pos
        point2 += self.pos
        point3 += self.pos

        pygame.draw.polygon(
            surface, 
            self.color, 
            (
                camera.adjust(point1), 
                camera.adjust(point2), 
                camera.adjust(point3)))

