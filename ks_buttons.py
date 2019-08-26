
#### Have classes relating to clickable buttons in the game 'Kitchen Scraps'.
# Includes classes: Food, Mix
# Play, Pause, Credits, Quit, Options

import pygame
from PIL import Image
from ks_library import *
utilities = Utilities()

#self.topleft_pos = self.rect.topleft[:]
#self.rect.topleft = (self.topleft_pos[0] * 2, self.topleft_pos[1] * 2)
#self.topleft_pos = self.rect.topleft[:]
#self.rect.topleft = (self.topleft_pos[0] * 2, self.topleft_pos[1] * 2)


class GameImage():
    """Create image surfaces of frames, boxes, display surfaces, et cetera without interaction options."""

    def __init__(self, name, bg):
        """Initialize Frames attributes."""
        self.name = name
        self.filename = utilities.convert_to_codehappy_string(name)
        self.img_srf = pygame.image.load('images/' + self.filename + '.png')
        self.act_srf = pygame.image.load('images/' + self.filename + '.png')
        gry_srf = Image.open('images/'+ self.filename + '.png').convert('LA')
        gry_srf.save('images/gry_' + self.filename + '.png')
        self.gry_srf = pygame.image.load('images/gry_' + self.filename + '.png')
        self.img_srfs = [self.act_srf, self.gry_srf]
        self.rect = self.img_srf.get_rect()
        self.bg = bg

    # def double_size(self):
    #     """Double the size of the icons."""
    #     self.double_srfs = []
    #         pygame.transform.scale2x(the_img_srf)
    #     print(self.img_srfs)
    #         #self.double_srfs.append(pygame.transform.scale2x(img_srf))
    #     #self.img_srf = self.double_srfs[0]
    #     self.rect = self.img_srf.get_rect()

    def place_image(self, xy, xy_placement='topleft'):
        """Move the location of the button surface and rect."""
        if xy_placement == 'topleft':
            self.rect.topleft = xy
        elif xy_placement == 'center':
            self.rect.center = xy

    def refresh_img(self):
        """Draw the food item onto the screen."""
        self.bg.screen.blit(self.img_srf, self.rect)

class Frame(GameImage):
    """Create an image surface that works as a background frame for another image/text to be positioned on top of."""

    def __init__(self, name, bg, xy_topleft=(0,0)):
        """Initialize GameImage and Frame attributes."""
        super().__init__(name, bg)
        self.rect.topleft = xy_topleft

    def refresh_framed_img(self, framed_image):
        self.bg.screen.blit(self.img_srf, self.rect)
        if framed_image == type(list) or framed_image == type(tuple):
            for image in framed_image:
                self.img_srf.blit(image, image.rect)
        else:
            self.img_srf.blit(framed_image, framged_image.rect)

class Button(GameImage):
    """Make a clickable surface-rect object."""
    def __init__(self, name, bg):
        """Initialize Button attributes."""
        super().__init__(name, bg)
        self.def_srf = pygame.image.load('images/' + self.filename + '.png')
        self.hvr_srf = pygame.image.load('images/hvr_' + self.filename + '.png')
        self.img_srfs.append(self.hvr_srf)

    def double_size(self, img_srf=''):
        """Double the size of the icons."""
        self.double_srfs = []
        if not img_srf:
            img_srf = self.img_srf

        for img_srf in self.img_srfs:
            self.double_srfs.append(pygame.transform.scale2x(img_srf))
        self.img_srf = self.double_srfs[0]
        self.hvr_srf = self.double_srfs[1]
        self.rect = self.img_srf.get_rect()

    def refresh_img(self):
        """Draw the food item onto the screen."""
        mouse_xy = pygame.mouse.get_pos()
        # If mouse coordinates collide with food's rect, blit the hover image. Else, blit the default image.
        if self.rect.collidepoint(mouse_xy):
            self.bg.screen.blit(self.hvr_srf, self.rect)
        else:
            self.bg.screen.blit(self.img_srf, self.rect)

    def check_click(self):
        """Check if mouse click collides with self."""
        mouse_xy = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_xy):
            return True
        else:
            return False

    def deactivate_button(self):
        self.gry_srf = pygame.image.load('images/gry_' + self.filename + '.png')



class Food(Button):
    """Make a food icon for the game. Allow it to switch grid location when clicked."""
    def __init__(self, name, bg, grid):
        """Initialize the images, hover images, and names of each food item."""
        super().__init__(name, bg)
        self.grid = grid
        self.active = False
        self.bg = bg

    def fill_empty_cell(self, empty_cells):
        """Fill an empty cell in a grid."""
        # TODO OPT: Sort empty cells coordinates from topleft to bottomright.
        self.rect.topleft = empty_cells[0]
        del empty_cells[0]

    def switch_grid(self, grid_a, grid_b):
        """Move icon from self.grid into an empty cell in another grid."""
        if self.grid == grid_a:
            dest_grid = grid_b
        elif self.grid == grid_b:
            dest_grid = grid_a
        if dest_grid.empty_cells:
            self.grid.empty_cells.insert(0, (self.rect[0], self.rect[1]))
            self.fill_empty_cell(dest_grid.empty_cells)
            self.grid = dest_grid
        else:
            pass
