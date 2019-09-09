
import os
import sys
import pygame
from ks_environment import Button

class RootPaths():
    """Create root paths for finding file locations."""
    def __init__(self, images_folder='images/', sounds_folder='sounds/', fonts_folder='fonts/'):
        """Initiate RootPath attributes."""
        self.paths = [images_folder, sounds_folder, fonts_folder]
        self.paths = ['./../'+path if not os.path.exists('./'+path) else path for path in self.paths]
        self.images = self.paths[0]
        self.sounds = self.paths[1]
        self.fonts = self.paths[2]




class GameMechanics():
    """Contain functions related to the actual changing and working mechanics of the game."""
    def __init__(self, settings):
        self.bg = Background(settings.bg)
        self.buttons = [self.mix_button, self.result_box]

        self.mix_button = Button('mix', self.bg)
        self.mix_button.rect[3] -= 15
        mix_button_pos = (self.boxes[1].rect.centerx, self.boxes[1].rect.centery + 50)
        self.mix_button.place_image(mix_button_pos, 'center')

        self.mix_box1 = mix_box1
        self.mix_box2 = mix_box2
        self.mix_box3 = mix_box3
        self.mix_boxes = [self.mix_box1, self.mix_box2, self.mix_box3]
        self.result_box = result_box

    def check_buttons(self):
        """Check user events. On mouse-click, check if a button was clicked. If so, return the button."""
        for event in pygame.event.get():
            # Close game if user exits.
            if event.type == pygame.QUIT:
                sys.exit()
            # Check if player clicked a button.
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_xy = pygame.mouse.get_pos()
                for button in self.buttons:
                    collide = button.check_collide(mouse_xy)
                    if collide:
                        # Return Button object.
                        return button

    def switch_grid(self, filler, grid_a, grid_b):
        """Move an object from within this grid into another. Remove from this grid."""
        # 'filler' is a Button object. 'grid_a' and 'grid_b' are Grid objects.
        # Check which grid 'filler' is in.
        if filler in grid_a.grid.values():
            current_grid = grid_a.grid
            dest_grid = grid_b.grid
        elif filler in grid_b.grid.values():
            current_grid = grid_b.grid
            dest_grid = grid_a.grid
        else:
            # If not in either grid, return 'filler' unchanged.
            print('error: it\'s not in either grid.')
            print(filler)
            return filler
        switched = False
        # Find first empty cell in dest_grid, then switch filler to it.
        for coord, cell in dest_grid.items():
            if cell == '':
                filler.rect.topleft = coord
                dest_grid[coord] = filler
                switched = True
                break
        # If switch was successful, clear current grid's cell.
        if switched:
            #if self.result_box.active == False: # TODO I don't recall the purpose of this.
            #    self.sfx_click.play()
            for coord, cell in current_grid.items():
                if filler == cell:
                    current_grid[coord] = ''
                    break
        else:
            # If switch failed, play denial click sound.
            self.sfx_denied.play()
            print('failure to switch.')

        # elif filler.name == self.big_box.result.name: # TODO I don't remember what this is for either.
        #     for coord, cell in self.grid_a.grid.items():
        #         if cell == '':
        #             filler.rect.topleft = coord
        #             self.grid_a.grid[coord] = filler
        #             return

    def confirm_result_and_cont(self):
        """Send result product to pantry, delete display-size result, activate buttons, reset result box."""
        result_product = Button(self.big_box.result.name, self.bg)
        self.switch_grid(result_product)
        self.buttons.remove(self.result_box.result)
        self.buttons.append(result_product)
        for button in self.buttons:
            button.active = True
        self.result_box.success = False
        self.result_box.active = False
        self.result_box.result = ''
        # TODO Add the result name to current foods list.

    def mix_ingredients(self, mixing_grid, formulas):
        """Compare the ingredients in the mix boxes with the full formula. Return the mixed product if successful."""
        # 'mixing_grid' is a Grid object.
        # Make a list of the mixing food names to use for comparison.
        mixing_foods = []
        for food in mixing_grid.grid.values():
            mixing_foods.append(food.name)
        mixing_foods.sort()
        # Check the library's formulas for a matching recipe.
        for product, materials in formulas.items():
            if mixing_foods == materials:
                ## On success, play success SFX, turn on O Result Box, return product.
                self.sfx_success.play()
                self.result_box.active = True
                self.result_box.success = True
                result = Button(product, self.bg)
                return result
        # If no match is found, play failure SFX and turn on X Result Box.
        self.sfx_failure.play()
        self.result_box.active = True
        self.result_box.success = False

    def erase_mix_materials(self, mixing_grid, current_foods):
        """Remove the food in the mixing grid from current foods, buttons, and grid."""
        # TODO Should I include mixing grid and current  foods as attributes?
        for coord, button in mixing_grid.grid.items():
            self.buttons.remove(button)
            current_foods.remove(button.name)
            mixing_grid.grid[coord] = ''