
import pygame
from ks_library import *
from ks_environment import Background, Grid
from ks_buttons import Button, Food
from craft_compendium import CraftCompendium

class Settings():
    """Define all the settings for the game Kitchen Scraps."""
    def __init__(self, bg_filename, recipe_book):
        """Initialize attributes for Settings."""
        self.bg = Background(bg_filename)
        self.caption = pygame.display.set_caption('Kitchen Scraps - Cleanup Attempt 2, now with PyCharm!')
        self.level_goals = ('bread', 'salad', 'classic_breakfast', 'three_course_drinks', 'full_course_meal')
        self.recipe_book = CraftCompendium(recipe_book)
        self.pantry_grid = Grid(5, 5, origin=(48, 48), grid_name='pantry grid')
        self.mixing_grid = Grid(1, 3, origin=(260, 120), grid_name='mixing grid')
        self.mix_button = Button('mix')
        self.mix_button_pos = self.mix_button.place_button((250, 40))

    def double_screen(self, double=True):
        if double == True:
            print(self.bg.name)
            self.bg.double_screen_size()
            print(self.bg.name)
            self.pantry_grid.double_size()
            self.mixing_grid.double_size()
            for food in self.current_foods:
                food.double_size()
            self.pantry_grid.fill_grid(self.bg.screen, self.current_foods)
            self.mix_button.double_size()


    def setup_new_level(self, level_num):
        """Set the new level's items and images."""
        # Current Level
        self.current_goal = 'salad' #self.level_goals[level_num - 1]
        self.current_full_formula = self.recipe_book.get_product_full_formula(self.current_goal)
        print(self.current_full_formula)
        self.current_all_materials = self.recipe_book.get_all_materials(self.current_full_formula, dupes=True)
        self.current_raw_ingredients = self.recipe_book.get_raw_materials(self.current_full_formula, dupes=True)

        self.current_foods = []
        for food in self.current_raw_ingredients:
            self.current_foods.append(Food(food, self.pantry_grid))
        self.pantry_grid.fill_grid(self.bg.screen, self.current_foods)
