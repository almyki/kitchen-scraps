
#### Have classes relating to clickable buttons in the game 'Kitchen Scraps'.
# Includes classes: Food, Mix
# Play, Pause, Credits, Quit, Options


class Button():
    """Make a clickable surface-rect object."""
    def __init__(self, name):
        """Initialize Button attributes."""
        self.name = name
        self.img_srf = pygame.image.load('images/' + food_name + '.png')
        self.hvr_srf = pygame.image.load('images/hvr_' + food_name + '.png')
        self.rect = self.img_srf.get_rect()

    def double_size(self):
        """Double the size of the icons."""
        self.img_srf = pygame.transform.scale2x(self.img_srf)
        self.hvr_srf = pygame.transform.scale2x(self.hvr_srf)
        self.rect = self.img_srf.get_rect()

    def refresh_button(self, bg):
        """Draw the food item onto the screen."""
        mouse_xy = pygame.mouse.get_pos()
        # If mouse coordinates collide with food's rect, blit the hover image. Else, blit the default image.
        if self.rect.collidepoint(mouse_xy):
            bg.screen.blit(self.hvr_srf, self.rect)
        else:
            bg.screen.blit(self.img_srf, self.rect)

    def place_button(self, origin_point):
        """Fill an empty cell in a grid."""
        self.rect.topleft = origin_point
        del origin_point


class Food(Button):
    """Make a food icon for the game.
    Make it have a hover image state.
    Make it have a click SFX.
    Make it have a hover image label."""
    def __init__(self, food_name, grid, active_grid):
        """Initialize the images, hover images, and names of each food item."""
        self.grid = grid
        self.active = False



    def switch_grid(self, other_grid):
        """Move icon from self.grid into an empty cell in another grid."""
        if other_grid.empty_cells:
            self.grid.empty_cells.append((self.rect[0], self.rect[1]))
            self.fill_empty_cell(other_grid.empty_cells)
            self.grid = other_grid
        else:
            pass

    def check_click(self, mouse_xy, grid_a, grid_b):
        """Check if mouse click collides with self."""
        if self.rect.collidepoint(mouse_xy):
            # TODO How to make icons fade in and out when clicked?
            if self.grid == grid_a:
                self.switch_grid(grid_b)

            elif self.grid == grid_b:
                self.switch_grid(grid_a)
