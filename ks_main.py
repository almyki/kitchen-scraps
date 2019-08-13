
# HIGHLIGHT + CTRL + ALT + C = Show dropdown of wrapping options like 'if', 'while'.

import sys
import pygame
from ks_library import *
from ks_environment import Background, Grid





class Settings():
    """Maintain all setting variables for the game."""
    def __init__(self, bg_filename):
        """Construct/initialize variables for Settings."""
        self.bg = Background(bg_filename)
        self.caption = pygame.display.set_caption('Kitchen Scraps - Cleanup Attempt 2, now with PyCharm!')
        self.levels = ('bread', 'salad', 'classic_breakfast', 'three_course_drinks', 'full_course_meal')
        self.current_level = 0

def remove_dupes(a_list):
    """Remove duplicate items from a list."""
    a_list = list(dict.fromkeys(a_list))
    return a_list

####    ####    ####    ####



# Set up all the variables before the game initiates.
settings = Settings('images/ks_bg.png')
settings.bg.double_screen_size()
pantry_grid = Grid(5, 5, origin=(102, 90), cell_size=(74, 74), grid_name='pantry grid')
mixing_grid = Grid(1, 3, origin=(520, 240), cell_size=(76, 76), grid_name='mixing grid')


#settings.current_level += 1
the_one_meal = settings.levels[settings.current_level]
current_foods = [the_one_meal]
current_recipes = {}
for food in current_foods:
    for recipe_result, recipe_ingredients in recipe_book.items():
        if recipe_result == food:
            for recipe_ingredient in recipe_ingredients:
                current_foods.append(recipe_ingredient)
                current_recipes[recipe_result] = recipe_ingredients
current_foods = remove_dupes(current_foods)
print(f'Current foods: {current_foods}')

food_names = current_foods[:]
for food_name in current_foods:
    if type(food_name) == str:
        current_foods.append((Food(food_name, pantry_grid, mixing_grid)))
        current_foods[-1].double_size()

for food_name in food_names:
    current_foods.remove(food_name)


# Separate the level's 'starting food'.
starting_foods = []
for food in current_foods:
    if food.name not in current_recipes.keys():
        starting_foods.append(food)
    else:
        pass


pantry_grid.fill_grid(settings.bg.screen, starting_foods)
pygame.init()


def detect_events(buttons):
    """Detect mouse and button clicks, then have the game respond."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_xy = pygame.mouse.get_pos()
            print(mouse_xy)
            for button in buttons:
                button.check_click(mouse_xy, pantry_grid, mixing_grid)
                button.refresh_food(settings.bg)



def run_kitchen_scraps():
    """Run the main loop for the game Kitchen Scraps."""
    while True:

        detect_events(starting_foods)
        settings.bg.refresh_screen()
        for food in starting_foods:
            food.refresh_food(settings.bg)
        pygame.display.flip()

print(pantry_grid.empty_cells)
print(mixing_grid.empty_cells)
run_kitchen_scraps()