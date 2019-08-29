
# Background, Grid, ActiveImage, Button

import pygame
from PIL import Image

class Background():
    """Create all the background"""
    def __init__(self, name):
        self.name = name
        self.filename = 'images/' + name + '.png'
        self.img_srf = pygame.image.load(self.filename)
        self.rect = self.img_srf.get_rect()
        self.dim = (self.rect[2], self.rect[3])
        self.screen = pygame.display.set_mode(self.dim)

    def darken_screen(self):
        """Fill the screen with a transparent dark color."""
        dark_screen = pygame.Surface(self.dim)
        dark_screen.set_alpha(150)
        dark_screen.fill((0, 0, 0))
        self.screen.blit(dark_screen, (0, 0))

    def refresh_screen(self):
        """Refresh the screen with fill, blit, flip."""
        self.fill_color = (255, 0, 0)
        self.screen.fill(self.fill_color)
        self.screen.blit(self.img_srf, self.rect)

class Grid():
    """Create grid coordinates in which to place objects."""
    def __init__(self, grid_name, rows, columns, cell_size=(40, 40), origin=(0, 0)):
        """Construct a grid's name, rows, columns, origin point, and cell size."""
        self.grid_name = grid_name
        self.rows = rows
        self.columns = columns
        self.cell_size = cell_size
        self.origin = origin
        self.grid = self.make_grid()

    def make_grid(self):
        """Make a list of xy coordinates based on the rows, columns, cell size, and origin point of the class."""
        grid = {}
        xy = [self.origin[0], self.origin[1]]
        for row in range(0, self.rows):
            for column in range(0, self.columns):
                xy_key = (xy[0], xy[1])
                grid[xy_key] = ''
                xy[0] += self.cell_size[0]
            xy[0] = self.origin[0]
            xy[1] += self.cell_size[1]
        return grid

    def fill_empty_cell(self, filler):
        """Modify the location of an object's rectangle and add its name to the grid's dict data."""
        for coord, cell in self.grid.items():
            if cell == '':
                filler.rect.topleft = coord
                self.grid[coord] = filler
                break

    def switch_grid(self, filler, grid_b):
        """Move an object from within this grid into another. Remove from this grid."""
        switched = False
        for coord, cell in grid_b.grid.items():
            if cell == '':
                filler.rect.topleft = coord
                grid_b.grid[coord] = filler
                switched = True
                break
        if switched == True:
            for coord, cell in self.grid.items():
                if filler == cell:
                    self.grid[coord] = ''
                    break

class ActiveImage():
    """Creates an image Surface with some form of active feedback, like changing position, color, or state."""
    def __init__(self, name, bg, origin=(0, 0)):
        self.name = name
        self.bg = bg
        self.filename = self.convert_to_codehappy_string(name)
        self.img_srf = pygame.image.load('images/' + self.filename + '.png')
        self.def_srf = pygame.image.load('images/' + self.filename + '.png')
        self.gry_srf = pygame.image.load('images/gry_' + self.filename + '.png')
        self.rect = self.img_srf.get_rect()
        self.origin = origin
        self.rect.move_ip(origin)
        self.active = True

    def convert_to_codehappy_string(self, string):
        codehappy_string = ''
        for character in string:
            if character == ' ':
                codehappy_string += '_'
            else:
                codehappy_string += character
        return codehappy_string

    def place_image(self, xy, origin_pos='topleft'):
        """Move the location of the button surface and rect."""
        if origin_pos == 'topleft':
            self.rect.topleft = xy
        elif origin_pos == 'center':
            self.rect.center = xy
        self.origin = xy

    def refresh_img(self):
        """Draw the food item onto the screen."""
        if self.active:
            self.bg.screen.blit(self.img_srf, self.rect)
        else:
            self.bg.screen.blit(self.gry_srf, self.rect)


class Button(ActiveImage):
    """"""
    def __init__(self, name, bg, origin=(0, 0)):
        """Initialize the parent attributes and Button-specific attributes."""
        super().__init__(name, bg, origin)
        self.hvr_srf = pygame.image.load('images/hvr_' + name + '.png')

    def check_collide(self):
        """Check if mouse click collides with self."""
        if self.active:
            mouse_xy = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_xy):
                self.img_srf = self.hvr_srf
                return True
            else:
                self.img_srf = self.def_srf
                return False
        else:
            self.img_srf = self.gry_srf