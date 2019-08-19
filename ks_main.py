
# HIGHLIGHT + CTRL + ALT + C = Show dropdown of wrapping options like 'if', 'while'.

import sys
import pygame

from ks_buttons import Food
from ks_settings import Settings





####    ####    ####    ####




settings = Settings('images/ks_bg.png')

pantry_grid.fill_grid(settings.bg.screen, current_foods)

pygame.init()

def check_mix_success():
    """
    If it's a successful recipe, combine into new food. If not, return items to shelf.
    Create a list of the active foods, then make a copy of the food name strings,
    then sort the copy to compare with the recipes.
    """
    active_foods = []
    for food in current_foods:
        if food.grid == mixing_grid:
            active_foods.append(food)
    active_foods_names = [active_foods[0].name, active_foods[1].name, active_foods[2].name]
    print(f'Active food names: {active_foods_names}')
    active_foods_names = sorted(active_foods_names)
    for recipe_result, recipe_ingredients in current_recipes.items():
        if active_foods_names == recipe_ingredients:
            current_foods.append(Food(recipe_result, pantry_grid))
            current_foods[-1].double_size()
            current_foods[-1].fill_empty_cell(pantry_grid.empty_cells)
            while active_foods:
                current_foods.remove(active_foods[0])
                active_foods.remove(active_foods[0])
            mixing_grid.empty_cells = mixing_grid.grid[:]
    while active_foods:
        active_foods[0].switch_grid(pantry_grid, mixing_grid)
        active_foods.remove(active_foods[0])

def detect_events(icons):
    """Detect mouse and button clicks, then have the game respond."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            for icon in icons:
                clicked = icon.check_click()
                if clicked == True:
                    icon.switch_grid(pantry_grid, mixing_grid)
            if len(mixing_grid.empty_cells) == 0:
                clicked = mix_button.check_click()
                if clicked:
                    check_mix_success()




def run_kitchen_scraps():
    """Run the main loop for the game Kitchen Scraps."""
    while True:

        detect_events(current_foods)
        settings.bg.refresh_screen()
        for food in current_foods:
            food.refresh_img(settings.bg)
        if len(mixing_grid.empty_cells) == 0:
            mix_button.refresh_img(settings.bg)
        else:
            settings.bg.screen.blit(mix_button.img_srf, mix_button.rect)
        pygame.display.flip()

print(pantry_grid.empty_cells)
print(mixing_grid.empty_cells)
run_kitchen_scraps()