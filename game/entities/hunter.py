import pygame

from .interfaces import GameObject

class Hunter(GameObject):

    def __init__(self, pos):
        super().__init__(
            pos=pos,
            radius=5,
            color=(255, 0, 0),
            )

    def update(self, objs, dt):
        super().update(dt)

    def update_helth(self, dt):
        self.helth -= self.STARVATION_SPEED*dt


    def draw(self, camera, surface):
        # length of equilateral triangle
        side_len = (3*self.radius)/math.sqrt(3)

        point1 = self.direction()
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