
import pygame
import sys
from ks_environment import Background, Grid, ActiveImage, Button, ResultBox, DetectEvents
from craft_compendium import CraftCompendium


class Settings():
    """Set the values for all the settings of the game."""
    def __init__(self, bg):
        """Initiate attributes for Settings."""
        # Background images and grid attributes.
        self.level = 0
        self.bg = Background(bg)
        self.pantry = ActiveImage('pantry', self.bg, [60, 60])
        self.pantry_grid = Grid('pantry grid', 5, 5, origin=(self.pantry.origin[0] + 4, self.pantry.origin[1] + 6))
        self.mixing_grid = Grid('mixing boxes', 1, 3, origin=(276, 65))

        # Sound and Music
        pygame.mixer.init()
        self.music = 'music_lobby-time-by-kevin-macleod'
        self.sfx_click = pygame.mixer.Sound('sounds/sfx_coin_collect.wav')
        self.sfx_denied = pygame.mixer.Sound('sounds/sfx_denied.wav')
        self.sfx_failure = pygame.mixer.Sound('sounds/sfx_failure.wav')
        self.sfx_success = pygame.mixer.Sound('sounds/sfx_success.wav')
        self.sfx_win = pygame.mixer.Sound('sounds/sfx_win.wav')

        # Recipes attributes.
        self.recipe_book = {
                        'dough': ['wheat', 'egg', 'water'],
                        'bread': [ 'dough', 'salt', 'yeast' ],
                        'dressing': ['vinegar', 'oil', 'herbs'],
                        'salad': [ 'lettuce', 'carrot', 'dressing' ],
                        'eggs and bacon': ['egg', 'red meat', 'oil'],
                        'orange juice': ['orange', 'orange', 'orange'],
                        'classic breakfast': [ 'orange juice', 'eggs and bacon', 'apple' ],
                        'fruit juice': ['apple', 'orange', 'water'],
                        'vegetable juice': ['carrot', 'lettuce', 'water'],
                        'soymilk': ['soybean', 'nuts', 'water'],
                        'three-course drinks': [ 'fruit juice', 'vegetable juice', 'soymilk' ],
                        'mayonnaise': ['egg', 'vinegar', 'oil'],
                        'egg sandwich': ['bread', 'egg', 'mayonnaise'],
                        'ice cream': ['cream', 'sugar', 'ice'],
                        'full-course meal': [ 'salad', 'egg sandwich', 'ice cream' ],
                        }
        self.recipe_compendium = CraftCompendium(self.recipe_book)
        self.goals = ('bread', 'salad', 'classic breakfast', 'three-course drinks', 'full-course meal')
        # Mixing Boxes and Result Box.
        self.box_1, self.box_2, self.box_3 = '', '', ''
        self.boxes = [self.box_1, self.box_2, self.box_3]
        z = 0
        for xy in self.mixing_grid.grid.keys():
            self.boxes[z] = (ActiveImage('box_mix_' + str((z+1)), self.bg, xy))
            z += 1
        big_box_pos = (self.boxes[1].rect.centerx, self.boxes[1].rect.centery + 130)
        self.big_box = ResultBox('box_correct', self.bg, big_box_pos)

        # Mix Button
        self.mix_button = Button('mix', self.bg)
        self.mix_button.rect[3] -= 15
        mix_button_pos = (self.boxes[1].rect.centerx, self.boxes[1].rect.centery + 50)
        self.mix_button.place_image(mix_button_pos, 'center')


    def set_level(self):
        """Reset the button list with the mix button plus all food buttons.
        Set the goal food for the level, then derive the full formula from it.
        Set the raw ingredients into the pantry.
        Rebuild the images list to be blit to the screen, including the level's food buttons."""
        self.sfx_win.play()
        self.big_box.active = False
        self.big_box.success = False
        self.big_box.result = ''
        self.buttons = [self.mix_button, self.big_box]
        self.current_goal = self.goals[self.level]
        self.current_full_formula = self.recipe_compendium.get_product_full_formula(self.current_goal)
        self.current_foods = self.recipe_compendium.get_raw_materials(self.current_full_formula, dupes=True)
        for food in self.current_foods:
            self.buttons.append(Button(food, self.bg))
            self.pantry_grid.fill_empty_cell(self.buttons[-1])
        self.events = DetectEvents(self.buttons)
        self.refresh_screen()
        pygame.display.flip()

    def refresh_screen(self):
        """Refresh all elements onto the screen."""
        self.check_active_states()
        self.bg.refresh_screen()
        self.pantry.refresh_img()
        for box in self.boxes:
            box.refresh_img()
        for button in self.buttons:
            button.refresh_img()
        self.big_box.refresh_img()

    def check_active_states(self):
        """Change the mix button and mix boxes to gray or white depending on if they are active."""
        z = 0
        for coord, cell in self.mixing_grid.grid.items():
            if cell and self.big_box.active == False and self.big_box.result == '':
                self.boxes[z].active = True
            else:
                self.boxes[z].active = False
            z += 1
        if '' in self.mixing_grid.grid.values() or self.big_box.active or self.big_box.success:
            self.mix_button.active = False
        else:
            self.mix_button.active = True

    def check_buttons(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_xy = pygame.mouse.get_pos()
                for button in self.buttons:
                    collide = button.check_collide(mouse_xy)
                    if collide:
                        return button

    def switch_grid(self, filler):
        """Move an object from within this grid into another. Remove from this grid."""
        switched = False
        if filler in self.pantry_grid.grid.values():
            current_grid = self.pantry_grid.grid
            dest_grid = self.mixing_grid.grid
        elif filler in self.mixing_grid.grid.values():
            current_grid = self.mixing_grid.grid
            dest_grid = self.pantry_grid.grid
        elif filler.name == self.big_box.result.name:
            for coord, cell in self.pantry_grid.grid.items():
                if cell == '':
                    filler.rect.topleft = coord
                    self.pantry_grid.grid[coord] = filler
                    return
        else:
            print('error: it\'s not in either grid.')
            print(filler)
            return
        for coord, cell in dest_grid.items():
            if cell == '':
                filler.rect.topleft = coord
                dest_grid[coord] = filler
                switched = True
                break
        if switched:
            if self.big_box.active == False:
                self.sfx_click.play()
            for coord, cell in current_grid.items():
                if filler == cell:
                    current_grid[coord] = ''
                    break
        else:
            self.sfx_denied.play()
            print('failure to switch.')

    def confirm_result_and_cont(self):
        """Send the result product to the pantry, remove the mixed food, and reactivate screen elements."""
        result_product = Button(self.big_box.result.name, self.bg)
        self.switch_grid(result_product)
        self.current_foods.append(result_product.name)
        self.buttons.remove(self.big_box.result)
        self.buttons.append(result_product)
        for button in self.buttons:
            button.active = True
        self.big_box.success = False
        self.big_box.active = False
        self.big_box.result = ''

    def mix_ingredients(self):
        """Compare the ingredients in the mix boxes with the full formula. Return the mixed product if successful."""
        mixing_foods = []
        for food in self.mixing_grid.grid.values():
            mixing_foods.append(food.name)
        mixing_foods.sort()
        # Check lvl full formula for matching recipe.
        for product, materials in self.current_full_formula.items():
            if mixing_foods == materials:
                ## Add resulting product to current foods, but not buttons (yet). Turn on Result Box. Return product.
                self.sfx_success.play()
                self.big_box.success = True
                result = Button(product, self.bg)
                return result
        self.sfx_failure.play()
        self.big_box.success = False

    def erase_mix_materials(self):
        """Remove the food in the mixing grid from current foods, buttons, and grid."""
        for coord, button in self.mixing_grid.grid.items():
            self.buttons.remove(button)
            self.current_foods.remove(button.name)
            self.mixing_grid.grid[coord] = ''
