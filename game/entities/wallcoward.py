from .interfaces import GameObject

import pygame


class WallCoward(GameObject):

    WALL_AFRAID_RADIUS = 100

    def __init__(self, 
            walls_rect=(
                pygame.Vector2(-450, 300),
                pygame.Vector2(450, -300)),
            **kwargs):
        super().__init__(**kwargs)
        self.walls_rect = walls_rect

    def wach_out_wall(self):
        top_left = self.walls_rect[0]
        bottom_right = self.walls_rect[1]

        desired = pygame.Vector2(0, 0)
        # print('diff', self.pos.x - top_left.x, bottom_right.x - self.pos.x)
        if self.pos.x < top_left.x + self.WALL_AFRAID_RADIUS:     
            desired += pygame.Vector2(self.maxspeed, self.vel.y)
        elif self.pos.x > bottom_right.x - self.WALL_AFRAID_RADIUS:
            desired += pygame.Vector2(-self.maxspeed, self.vel.y)

        if self.pos.y > top_left.y - self.WALL_AFRAID_RADIUS:     
            desired += pygame.Vector2(self.vel.x, -self.maxspeed)
        elif self.pos.y < bottom_right.y + self.WALL_AFRAID_RADIUS:
            desired += pygame.Vector2(self.vel.x, self.maxspeed)

        print(self.pos, desired)
        if desired.length() > 0:
            steer = desired - self.vel
            steer = self.vec_limit(steer, self.maxforce)
            steer.scale_to_length(self.maxforce)
            print(steer)
            self.apply_force(steer)