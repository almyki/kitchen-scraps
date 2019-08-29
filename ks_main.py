
#### Main module for the game Kitchen Scraps.

import sys
import pygame
from PIL import Image
from ks_environment import Background, Grid, ActiveImage, Button
from craft_compendium import CraftCompendium
from ks_library import *

# TODO

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
                print(button.name)
                return button


class Settings():
    """Set the values for all the settings of the game."""
    def __init__(self, bg, recipe_book):
        """Initiate attributes for Settings."""
        # Background images and grid attributes.
        self.bg = Background(bg)
        self.pantry = ActiveImage('pantry', self.bg, [60, 60])
        self.pantry_grid = Grid('pantry grid', 5, 5, origin=(self.pantry.origin[0] + 4, self.pantry.origin[1] + 8))
        self.mixing_grid = Grid('mixing boxes', 1, 3, origin=(276, 65))

        # Recipes attributes.
        self.recipe_book = recipe_book
        self.recipe_compendium = CraftCompendium(self.recipe_book)
        self.goals = ('bread', 'salad', 'classic breakfast', 'three-course drink', 'three-course meal')

        # Screen elements attributes (boxes, buttons).
        self.mix_button = Button('mix', self.bg)
        self.big_box = ActiveImage('box_blank', self.bg)
        self.boxes = []
        for xy in self.mixing_grid.grid.keys():
            self.boxes.append(ActiveImage('box_mix', self.bg, xy))

        # Move visual elements to their locations.
        self.mix_button.rect[3] -= 15
        mix_button_pos = (self.boxes[1].rect.centerx, self.boxes[1].rect.centery + 50)
        self.mix_button.place_image(mix_button_pos, 'center')
        big_box_pos = (self.boxes[1].rect.centerx, self.boxes[1].rect.centery + 130)
        self.big_box.place_image(big_box_pos, 'center')

    def set_level(self):
        """Reset the button list with the mix button plus all food buttons.
        Set the goal food for the level, then derive the full formula from it.
        Set the raw ingredients into the pantry.
        Rebuild the images list to be blit to the screen, including the level's food buttons."""
        self.buttons = [self.mix_button]
        self.goal = self.goals[self.level]
        self.goal_full_formula = self.recipe_compendium.get_product_full_formula(self.goal)
        self.current_foods = self.recipe_compendium.get_raw_materials(self.goal_full_formula)
        for food in self.current_foods:
            self.buttons.append(Button(food, self.bg))
            self.pantry_grid.fill_empty_cell(self.buttons[-1])
        self.images = self.consolidate_images()
        self.bg.refresh_screen()
        pygame.display.flip()

    def consolidate_images(self):
        """Put image objects together into one list."""
        images = [self.pantry, self.big_box]
        for box in self.boxes:
            images.append(box)
        for button in self.buttons:
            images.append(button)
        return images

    def refresh_screen(self):
        """Refresh all elements onto the screen."""
        self.check_box_activity()
        if '' in self.mixing_grid.grid.values():
            self.mix_button.active = False
        else:
            self.mix_button.active = True
        clicked_button = self.events.detect_events()
        self.check_grid_switching(clicked_button)
        self.bg.refresh_screen()
        for image in self.images:
            image.refresh_img()
        for button in self.buttons:
            button.refresh_img()

    def check_grid_switching(self, clicked_button):
        """"(Switch the grid of the clicked button input into the function.)"""
        if clicked_button in self.pantry_grid.grid.values():
            for filler in self.pantry_grid.grid.values():
                if filler == clicked_button:
                    print('clicked:')
                    print(filler)
                    self.pantry_grid.switch_grid(filler, self.mixing_grid)
                    return
        else:
            for filler in self.mixing_grid.grid.values():
                if filler == clicked_button:
                    self.mixing_grid.switch_grid(filler, self.pantry_grid)
                    return

    def check_box_activity(self):
        """Change the mixing boxes to gray or white depending on if they are active (filled)."""
        z = 0
        for coord, cell in ks.mixing_grid.grid.items():
            if cell:
                self.boxes[z].active = True
            else:
                self.boxes[z].active = False
            z += 1


recipe_book = {
    'dough': ['wheat', 'egg', 'water'],
    'bread': ['dough', 'salt', 'yeast'],

    'dressing': ['vinegar', 'oil', 'herbs'],
    'salad': ['lettuce', 'carrot', 'dressing'],

    'eggs and bacon': ['egg', 'red meat', 'oil'],
    'orange juice': ['orange', 'orange', 'orange'],
    'classic breakfast': ['orange juice', 'eggs and bacon', 'apple'],

    'fruit juice': ['apple', 'orange' 'water'],
    'vegetable juice': ['carrot', 'lettuce', 'water'],
    'soy milk': ['soybeans', 'nuts', 'water'],
    'three-course drinks': ['fruit juice', 'vegetable juice', 'soy milk'],

    'mayonnaise': ['egg', 'vinegar', 'oil'],
    'egg sandwich': ['bread', 'egg', 'mayonnaise'],
    'ice cream': ['cream', 'sugar', 'ice'],
    'full-course meal': ['salad', 'egg sandwich', 'ice cream'],
    }


ks = Settings('ks_bg', recipe_book)


pygame.init()
ks.set_level()

while True:
    ks.refresh_screen()
    pygame.display.flip()

    if len(ks.current_foods) == 1:
        ks.level += 1
        ks.set_level()