import pygame
from .model import Model


class Camera(object):
    """Class that converts cartesian pos to pixel pos on the screen."""

    def __init__(self, x, y, width, height, scale=1):
        # top left point of camera box
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.scale = scale

    def set_center(self, pos):
        """Change camera postion according to passed center."""
        self.x = pos.x - self.width*self.scale/2
        self.y = pos.y + self.height*self.scale/2

    def adjust(self, pos):
        """Convert cartesian pos to pos relative to the camera."""
        return pygame.Vector2(
            (pos.x - self.x)/self.scale,
            (self.y - pos.y)/self.scale)

    def to_pos(self, pixel_pos):
        return pygame.Vector2(
            (pixel_pos.x * self.scale + self.x),
            (self.y - pixel_pos.y * self.scale))

class View():
    """"Class that displays model state and shows HUD"""

    # BACKGROUND_COLOR = (242, 251, 255)
    TEXT_COLOR = (50, 50, 50)
    TEXT_COLOR = (204, 204, 153)
    HUD_BACGROUND_COLOR = (50,50,50,80)
    BACKGROUND_COLOR = (0, 100, 0)

    FOREST_COLOR = (0, 138, 0)
    GRID_COLOR = (0, 120, 0)
    DEBUG_COLOR = (255, 0, 0)

    def __init__(self, screen, model, scale):
        self.screen = screen
        self.width, self.height = self.screen.get_size()
        self.camera = Camera(0, 0, self.width, self.height, scale)
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.hud_surface = pygame.Surface((1, 1), pygame.SRCALPHA)
        self.hud_surface.fill(View.HUD_BACGROUND_COLOR)
        self.font = pygame.font.Font(pygame.font.get_default_font(), 18)

        self.model = model
        self.moving_direction = pygame.Vector2(0, 0)

    def redraw(self):
        """Redraw screen according to model of game."""
        if self.model.hunter.is_alive:
            self.camera.set_center(self.model.hunter.pos)

        self.screen.fill(View.BACKGROUND_COLOR)
        self.draw_forest()
        self.draw_grid()
        self.model.draw(self.camera, self.screen)
        if self.model.hunter.is_alive:
            self.draw_hud()

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
                if event.type == pygame.KEYDOWN:
                    if event.key in vector_map:
                        self.moving_direction += vector_map[event.key]
                if event.type == pygame.KEYUP:
                    if event.key in vector_map:
                        self.moving_direction -= vector_map[event.key]
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.model.shoot(self.camera)

            self.redraw()
            self.update()

    def update(self):
        target = self.camera.to_pos(
            pygame.Vector2(
                pygame.mouse.get_pos()))
        self.model.update(self.delta_time(), target)
        self.model.move(self.moving_direction)

    def draw_forest(self):
        top_left = self.camera.adjust(self.model.bounds[0])
        top_right = self.camera.adjust(
            pygame.Vector2(
                self.model.bounds[1].x,
                self.model.bounds[0].y))

        bottom_right = self.camera.adjust(self.model.bounds[1])
        bottom_left = self.camera.adjust(
            pygame.Vector2(
                self.model.bounds[0].x,
                self.model.bounds[1].y))

        pygame.draw.polygon(
            self.screen,
            self.FOREST_COLOR,
            (top_left, top_right, bottom_right, bottom_left))

    def draw_grid(self, step=50):
        """Draw grid on screen with passed step."""
        top_left = self.model.bounds[0]
        bottom_right = self.model.bounds[1]

        x = top_left.x
        while x <= bottom_right.x:
            start = pygame.Vector2(x, top_left.y)
            end = pygame.Vector2(x, bottom_right.y)
            pygame.draw.line(
                self.screen,
                self.GRID_COLOR,
                self.camera.adjust(start),
                self.camera.adjust(end))
            x += step

        y = bottom_right.y
        while y <= top_left.y:
            start = pygame.Vector2(bottom_right.x, y)
            end = pygame.Vector2(top_left.x, y)
            pygame.draw.line(
                self.screen,
                self.GRID_COLOR,
                self.camera.adjust(start),
                self.camera.adjust(end))
            y += step

    def draw_text(self, surface, text, pos, color=TEXT_COLOR, align_center=False):
        text_surface = self.font.render(text, True, color)
        pos = list(pos)
        if align_center:
            # offset pos if was passed center
            pos[0] -= text_surface.get_width() // 2
            pos[1] -= text_surface.get_height() // 2
        surface.blit(text_surface, pos)

    def draw_hud(self, padding=(8, 5)):
        bullets_text = 'Bullets: {:6}'.format(self.model.hunter.bullets_left)
        self.draw_hud_item(
             (15, self.height - 30 - 2*padding[1]),
             (bullets_text,),
             10,
             padding)

        killed_text = 'Killed: {:6}'.format(self.model.hunter.killed)
        self.draw_hud_item(
             (self.width - 150, 15),
             (killed_text,),
             10,
             padding)

    def draw_hud_item(self, pos, lines, maxchars, padding):
        # seacrh max line width
        max_width = max(map(lambda line: self.font.size(line)[0], lines))
        font_height = self.font.get_height()
        # size of HUD item background
        item_size = (
            max_width + 2*padding[0], 
            font_height*len(lines) + 2*padding[1])
        # scaling transparent HUD background
        item_surface = pygame.transform.scale(self.hud_surface, item_size)
        # draw each line
        for i, line in enumerate(lines):
            self.draw_text(
                item_surface,
                line,
                (padding[0], padding[1] + font_height*i))
        # bilt on main surface
        self.screen.blit(item_surface, pos)

    def delta_time(self):
        return self.clock.tick(self.fps) / 1000
    
