
import pygame
import sys
import os
from ks_environment import Background, Grid, ActiveImage, Button, ResultBox, DetectEvents
from craft_compendium import CraftCompendium

root = RootPaths()
level - goal, full formula, materials, music, theme


class Settings():
    """Set the values for all the settings of the game."""
    def __init__(self, ):
        """Initiate attributes for Settings."""
        # Background images and grid attributes.
        self.level = 0
        self.bg = 'ks_bg.png'
        self.pantry = 'pantry.png'
        self.pantry = ActiveImage('pantry', self.bg, [60, 60])
        # Sound and Music
        pygame.mixer.init()
        self.volume = 0.3
        self.music = 'music_lobby-time-by-kevin-macleod'
        self.sfx_click = pygame.mixer.Sound(root.sounds + 'sfx_coin_collect.wav')
        self.sfx_denied = pygame.mixer.Sound(root.sounds + 'sfx_denied.wav')
        self.sfx_failure = pygame.mixer.Sound(root.sounds + 'sfx_failure.wav')
        self.sfx_success = pygame.mixer.Sound(root.sounds + 'sfx_success.wav')
        self.sfx_win = pygame.mixer.Sound(root.sounds + 'sfx_win.wav')
        # Mixing Boxes and Result Box.
        self.box_1 = ActiveImage('box_mix_1', self.bg, list(self.mixing_grid.grid)[0])
        self.box_2 = ActiveImage('box_mix_2', self.bg, list(self.mixing_grid.grid)[1])
        self.box_3 = ActiveImage('box_mix_3', self.bg, list(self.mixing_grid.grid)[2])
        self.boxes = [self.box_1, self.box_2, self.box_3]
        z = 0
        for xy in self.mixing_grid.grid.keys():
            self.boxes[z] = (ActiveImage('box_mix_' + str((z+1)), self.bg, xy))
            z += 1
        big_box_pos = (self.boxes[1].rect.centerx, self.boxes[1].rect.centery + 130)
        self.big_box = ResultBox('box_correct', self.bg, big_box_pos)

        # Mix Button

        # Grids
        self.pantry_grid = Grid('pantry grid', 5, 5, origin=(self.pantry.origin[0] + 4, self.pantry.origin[1] + 6))
        self.mixing_grid = Grid('mixing boxes', 1, 3, origin=(276, 65))
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


    def set_music(self):
        if not os.path.exists('./sounds'):
            root_sounds = './../sounds/'
        else:
            root_sounds = 'sounds/'
        pygame.mixer.music.load(root_sounds + self.music + '.mp3')
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play(-1)

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


