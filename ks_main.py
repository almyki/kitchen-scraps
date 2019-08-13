
import sys
import pygame
from ks_environment import Background, Grid


class Foods():
    """Make a food icon for the game.
    Make it have a hover image state.
    Make it have a click SFX.
    Make it have a hover image label."""
    def __init__(self, img_filename, hvr_filename):
        """Initialize the images, hover images, and names of each food item."""
        self.img_srf = pygame.image.load(img_filename)
        self.hvr_srf = pygame.image.load(hvr_filename)
        self.rect = self.img_srf.get_rect()

    def draw_food(self, screen, xy):
        """Draw the food item onto the screen."""
        self.rect.move_ip(xy[0], xy[1])
        mouse_xy = pygame.mouse.get_pos()
        # If mouse coordinates collide with food's rect, blit the hover image. Else, blit the default image.
        if self.rect.collidepoint(mouse_xy):
            screen.blit(self.hvr_srf, self.rect)
        else:
            screen.blit(self.img_srf, self.rect)

image_filenames = ['bread.png', 'dough.png', 'egg.png', 'salt.png', 'water.png', 'wheat.png', 'yeast.png',
                   'hvr_bread.png', 'hvr_dough.png', 'hvr_egg.png', 'hvr_salt.png', 'hvr_water.png', 'hvr_wheat.png', 'hvr_yeast.png', ]


class Settings():
    """Maintain all setting variables for the game."""
    def __init__(self, bg_filename):
        """Construct/initialize variables for Settings."""
        self.bg = Background(bg_filename)
        self.caption = pygame.display.set_caption('Kitchen Scraps - Cleanup Attempt 2, now with PyCharm!')




# Set up all the variables before the game initiates.
set = Settings('images/ks_bg.png')
set.bg.double_screen_size()
pantry_grid = Grid(5, 5, origin=(102,82), cell_size=(76,76), grid_name='pantry grid')
pantry_grid.fill_grid(set.bg.screen, )
pygame.init()

def detect_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()


def run_kitchen_scraps():
    """Run the main loop for the game Kitchen Scraps."""
    while True:

        detect_events()
        set.bg.refresh_screen()
        pantry_grid.fill_grid(set.bg.screen)
        pygame.display.flip()

run_kitchen_scraps()