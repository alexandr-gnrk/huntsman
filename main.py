import pygame
from game import Model


class Camera(object):
    """Class that converts cartesian pos to pixel pos on the screen."""

    def __init__(self, x, y, width, height, scale=1):
        # top left point of camera box
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.scale = 1

    def set_center(self, pos):
        """Change camera postion according to passed center."""
        self.x = pos.x - self.width/2
        self.y = pos.y + self.height/2

    def adjust(self, pos):
        """Convert cartesian pos to pos relative to the camera."""
        return pygame.Vector2(
            pos.x*self.scale - self.x,
            self.y - pos.y*self.scale)

        # pos = pygame.Vector2(
        #     pos.x*self.scale - self.x,
        #     self.y - pos.y*self.scale)

        # return pygame.Vector2(pos.x % 900, pos.y % 600)

    def to_pos(self, pixel_pos):
        return pygame.Vector2(
            (pixel_pos.x + self.x) / self.scale,
            (self.y - pixel_pos.y) / self.scale)

class View():
    """"Class that displays model state and shows HUD"""

    # BACKGROUND_COLOR = (242, 251, 255)
    # BACKGROUND_COLOR = (0, 0, 0)
    BACKGROUND_COLOR = (0, 138, 0)
    # GRID_COLOR = (226, 234, 238)
    GRID_COLOR = (0, 120, 0)
    DEBUG_COLOR = (255, 0, 0)

    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = self.screen.get_size()
        self.camera = Camera(0, 0, self.width, self.height)
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.model = Model()
        self.moving_direction = pygame.Vector2(0, 0)


    def redraw(self):
        """Redraw screen according to model of game."""
        if self.model.hunter.is_alive:
            self.camera.set_center(self.model.hunter.pos)

        self.screen.fill(View.BACKGROUND_COLOR)

        self.draw_grid()
        self.model.draw(self.camera, self.screen)

        pygame.display.flip()

  
    def start(self):
        """Start game loop."""
        vector_map = {
            pygame.K_w: pygame.Vector2(0, 1),
            pygame.K_s: pygame.Vector2(0, -1),
            pygame.K_a: pygame.Vector2(-1, 0),
            pygame.K_d: pygame.Vector2(1, 0),
        }

        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key in vector_map:
                        self.moving_direction += vector_map[event.key]
                elif event.type == pygame.KEYUP:
                    if event.key in vector_map:
                        self.moving_direction -= vector_map[event.key]

            self.redraw()
            self.update()

    def update(self):
        target = self.camera.to_pos(
            pygame.Vector2(
                pygame.mouse.get_pos()))
        self.model.update(self.delta_time(), target)
        self.model.move(self.moving_direction)
        # for obj in self.objs:
        #     obj.update(self.delta_time())

    def draw_grid(self, step=35):
        """Draw grid on screen with passed step."""
        top_left = self.model.bounds[0]
        bottom_right = self.model.bounds[1]
        for i in range(int(top_left.x), int(bottom_right.x)+step, step):
            start_coord = pygame.Vector2(top_left.x, i)
            end_coord = pygame.Vector2(bottom_right.x, i)
            pygame.draw.line(
                self.screen, 
                View.GRID_COLOR, 
                self.camera.adjust(start_coord), 
                self.camera.adjust(end_coord), 
                2)
            start_coord = pygame.Vector2(i, top_left.y)
            end_coord = pygame.Vector2(i, bottom_right.y)
            pygame.draw.line(
                self.screen, 
                View.GRID_COLOR, 
                self.camera.adjust(-start_coord), 
                self.camera.adjust(-end_coord), 
                2)

    def draw_vector(self, x, y, dx, dy, color):
        """Draw passed vector on the screen."""
        pygame.draw.line(
            self.screen,
            color,
            self.camera.adjust([x, y]),
            self.camera.adjust([x+dx, y+dy]))
        pygame.draw.circle(
            self.screen,
            color,
            self.camera.adjust([x+dx, y+dy]),
            3)

    def mouse_pos_to_polar(self):
        """Convert mouse position to polar vector."""
        x, y = pygame.mouse.get_pos()
        # center offset 
        x -= self.width/2
        y = self.height/2 - y
        # get angle and length(speed) of vector
        angle = math.atan2(y, x)
        speed = math.sqrt(x**2 + y**2)
        # setting radius of speed change zone
        speed_bound = 0.8*min(self.width/2, self.height/2)
        # normalize speed
        speed = 1 if speed >= speed_bound else speed/speed_bound
        return angle, speed

    def delta_time(self):
        return self.clock.tick(self.fps) / 1000
    

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((900, 600))

    v = View(screen)
    v.start()

