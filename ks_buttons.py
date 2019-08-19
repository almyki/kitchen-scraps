
#### Have classes relating to clickable buttons in the game 'Kitchen Scraps'.
# Includes classes: Food, Mix
# Play, Pause, Credits, Quit, Options

import pygame


class Button():
    """Make a clickable surface-rect object."""
    def __init__(self, name):
        """Initialize Button attributes."""
        self.name = name
        self.img_srf = pygame.image.load('images/' + name + '.png')
        self.hvr_srf = pygame.image.load('images/hvr_' + name + '.png')
        self.rect = self.img_srf.get_rect()

    def double_size(self):
        """Double the size of the icons."""
        self.img_srf = pygame.transform.scale2x(self.img_srf)
        self.hvr_srf = pygame.transform.scale2x(self.hvr_srf)
        self.rect = self.img_srf.get_rect()

    def place_button(self, origin):
        """Move the location of the button surface and rect."""
        self.rect.topleft = (origin)

    def refresh_img(self, bg):
        """Draw the food item onto the screen."""
        mouse_xy = pygame.mouse.get_pos()
        # If mouse coordinates collide with food's rect, blit the hover image. Else, blit the default image.
        if self.rect.collidepoint(mouse_xy):
            bg.screen.blit(self.hvr_srf, self.rect)
        else:
            bg.screen.blit(self.img_srf, self.rect)

    def check_click(self):
        """Check if mouse click collides with self."""
        mouse_xy = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_xy):
            return True
        else:
            return False


class Food(Button):
    """Make a food icon for the game. Allow it to switch grid location when clicked."""
    def __init__(self, name, grid):
        """Initialize the images, hover images, and names of each food item."""
        super().__init__(name)
        self.grid = grid
        self.active = False

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
            self.grid.empty_cells.append((self.rect[0], self.rect[1]))
            self.fill_empty_cell(dest_grid.empty_cells)
            self.grid = dest_grid
        else:
            pass
