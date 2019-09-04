
# Background, Grid, ActiveImage, Button

import pygame
import sys
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
        # Dark Mode settings
        self.dark_screen = pygame.Surface(self.dim)
        self.dark_screen.set_alpha(100)
        self.dark_screen.fill((0, 0, 0))

    def refresh_screen(self):
        """Refresh the screen with fill, blit, flip."""
        self.fill_color = (255, 0, 0)
        self.screen.fill(self.fill_color)
        self.screen.blit(self.img_srf, self.rect)

    def darken_screen(self):
        self.screen.blit(self.dark_screen, (0, 0))


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


class ActiveImage():
    """Creates an image Surface with some form of active feedback, like changing position, color, or state."""
    def __init__(self, name, bg, origin=(0, 0)):
        self.name = name
        self.bg = bg
        self.filename = self.convert_to_codehappy_string(name)
        self.img_srf = pygame.image.load('images/' + self.filename + '.png')
        self.def_srf = pygame.image.load('images/' + self.filename + '.png')
        gry_srf = Image.open('images/' + self.filename + '.png').convert('LA')
        gry_srf.save('images/' + self.filename + '_gry.png')
        self.gry_srf = pygame.image.load('images/' + self.filename + '_gry.png')
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
        """Draw the item onto the screen."""
        if self.active:
            self.bg.screen.blit(self.img_srf, self.rect)
        else:
            self.bg.screen.blit(self.gry_srf, self.rect)


class Button(ActiveImage):
    """"""
    def __init__(self, name, bg, origin=(0, 0)):
        """Initialize the parent attributes and Button-specific attributes."""
        super().__init__(name, bg, origin)
        self.hvr_srf = pygame.image.load('images/' + self.filename + '_hvr.png')

    def check_collide(self, mouse_xy):
        """Check if mouse click collides with self."""
        if self.active:
            if self.rect.collidepoint(mouse_xy):
                self.img_srf = self.hvr_srf
                return True
            else:
                self.img_srf = self.def_srf
                return False
        else:
            self.img_srf = self.gry_srf

    def refresh_img(self):
        """Draw the item onto the screen."""
        if self.active:
            mouse_xy = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_xy):
                self.img_srf = self.hvr_srf
            else:
                self.img_srf = self.def_srf
            self.bg.screen.blit(self.img_srf, self.rect)
        else:
            self.bg.screen.blit(self.gry_srf, self.rect)


class ResultBox(Button):
    """The big box that displays the result of a mix."""

    def __init__(self, name, bg, origin=(0, 0)):
        """Initialize ResultBox attributes."""
        super().__init__(name, bg, origin)
        self.name = 'box_correct'
        self.wht_srf = pygame.image.load('images/box_blank.png')
        self.q_srf = pygame.image.load('images/box_questionmark.png')
        self.x_srf = pygame.image.load('images/box_wrong.png')
        self.x_hvr = pygame.image.load('images/box_wrong_hvr.png')
        self.c_srf = pygame.image.load('images/box_correct.png')
        self.c_hvr = pygame.image.load('images/box_correct_hvr.png')
        self.active = False
        self.success = False
        self.rect.center = origin
        self.result = ''

    def fill_big_box(self, product):
        self.active = False
        self.result = product
        self.result.def_srf = pygame.transform.scale2x(product.def_srf)
        self.result.hvr_srf = pygame.transform.scale2x(product.hvr_srf)
        self.result.rect = self.result.def_srf.get_rect()
        self.result.place_image(self.rect.center, 'center')

    def disable_all_except_self(self, buttons_to_disable):
        self.active = True
        for button in buttons_to_disable:
            if button is not self:
                button.active = False
        if self.result:
            self.result.active = True

    def refresh_img(self):
        """Draw the item onto the screen."""
        mouse_xy = pygame.mouse.get_pos()
        if self.active:
            if self.success:
                if self.rect.collidepoint(mouse_xy):
                    self.img_srf = self.c_srf
                else:
                    self.img_srf = self.c_hvr
            else:
                if self.rect.collidepoint(mouse_xy):
                    self.img_srf = self.x_srf
                else:
                    self.img_srf = self.x_hvr
            self.bg.darken_screen()
            self.bg.screen.blit(self.img_srf, self.rect)
        else:
            if self.success:
                self.img_srf = self.wht_srf
                self.bg.darken_screen()
                self.bg.screen.blit(self.img_srf, self.rect)
                self.result.refresh_img()
            else:
                self.img_srf = self.q_srf
                self.bg.screen.blit(self.img_srf, self.rect)


class DetectEvents():
    """Detect any inputs or interactions and respond."""
    def __init__(self, clickables=''):
        """Initialize attributes for Detect Events."""
        self.clickables = clickables

    def detect_events(self):
        """Loop through all user input events. Exit if user quits. Return any clicked button."""
        for button in self.clickables:
            button.check_collide()
        for event in pygame.event.get():
            self.detect_quit(event)
            mouse_xy = self.get_click_xy(event)
            if mouse_xy:
                button = self.detect_button_collide()
                return button

    def detect_quit(self, event):
        """Close the game if player exits out."""
        if event.type == pygame.QUIT:
            sys.exit()

    def get_click_xy(self, event):
        """Return the xy coordinates for any mouse clicks."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_xy = pygame.mouse.get_pos()
            return mouse_xy
        else:
            return

    def detect_button_collide(self):
        """Check through all clickable buttons to see if the mouse pos collides with any of them."""
        for button in self.clickables:
            clicked_button = button.check_collide()
            if clicked_button:
                print('clicked: ' + button.name)
                return button