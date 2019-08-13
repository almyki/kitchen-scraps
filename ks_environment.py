
#### Holds classes to set up Kitchen Scraps' Background, Grids.

class Background():
    """Create the background and screen."""
    def __init__(self, bg_filename):
        self.bg_srf = pygame.image.load(bg_filename)
        self.rect = self.bg_srf.get_rect()
        self.screen = pygame.display.set_mode((self.rect[2], self.rect[3]))

    def double_screen_size(self):
        """Double the background image and screen size."""
        self.bg_srf = pygame.transform.scale2x(self.bg_srf)
        self.rect = self.bg_srf.get_rect()
        self.screen = pygame.display.set_mode((self.rect[2], self.rect[3]))

    def refresh_screen(self):
        """Refresh the screen with fill, blit, flip."""
        self.fill_color = (255, 255, 255)
        self.screen.fill(self.fill_color)
        self.screen.blit(self.bg_srf, self.rect)


class Grid():
    """Create grid coordinates in which to place objects."""
    def __init__(self, rows, columns, cell_size=(40,40), origin=(0,0), grid_name='no_name',):
        """Construct a grid's name, rows, columns, origin point, and cell size."""
        self.grid_name = grid_name
        self.rows = rows
        self.columns = columns
        self.cell_size = cell_size
        self.origin = origin
        self.grid = self.make_grid()
        self.empty_cells = self.grid[:]
        self.rect = pygame.Rect(self.origin, (self.grid[-1][0] - self.origin[0], self.grid[-1][1] - self.origin[1]))

    def check_object_data(self):
        print(f'Name: {self.grid_name}')

    def make_grid(self):
        grid = []
        xy = [self.origin[0], self.origin[1]]
        for row in range(0, self.rows):
            for column in range(0, self.columns):
                this_xy = xy[:]
                grid.append(this_xy)
                # Move coordinates to right by one cell width.
                xy[0] += self.cell_size[0]
                print(f"Test: {this_xy}")
            # Star new row. Move down by one cell height, reset x to origin.
            xy[0] = self.origin[0]
            xy[1] += self.cell_size[1]
        return grid

    def double_size(self, img_srf):
        """Double the background image and screen size."""
        img_srf = pygame.transform.scale2x(img_srf)
        img_srf.rect = img_srf.get_rect()

    def fill_grid(self, screen, filler_items=[]):
        """Fill the grid with image surfaces from a list of items."""
        # Must test double-sizing
        self.empty_cells = []
        for xy in self.grid:
            if z < len(filler_items):
                filler_items[z].img_srf.set_colorkey((255,255,255))
                filler_items[z].rect.move_ip(pygame.Rect(xy[0], xy[1]))
                self.double_size(filler_items[z].img_srf)
            else:
                self.empty_cells.append(xy)

        # This draws circles to fill the grid.
        circle = False
        if circle == True:
            for xy in self.grid:
                cell_center = (int(xy[0] + (self.cell_size[0] / 2)), int(xy[1] + (self.cell_size[1] / 2)))
                circle_radius = int(self.cell_size[0] / 2)
                pygame.draw.circle(screen, (200,0,0), cell_center, circle_radius)