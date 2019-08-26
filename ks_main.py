
# HIGHLIGHT + CTRL + ALT + C = Show dropdown of wrapping options like 'if', 'while'.

import sys
import pygame
from ks_library import *
from ks_settings import Settings
from ks_buttons import GameImage, Frame, Button, Food

# TODO Put 'check mix success' and 'detect events' into a class.
#  Detect win condition, show win screen, then wait for input to go to next level.
# Test all 5 levels. Solve the category type problem.
# Create robust messages system, and utility buttons, to cover for multiple situations as placeholders until replaced.






def check_mix_success():
    """
    If it's a successful recipe, combine into new food. If not, return items to shelf.
    Create a list of the active foods, then make a copy of the food name strings,
    then sort the copy to compare with the recipes.
    """
    active_foods = []
    for food in ks.current_foods:
        if food.grid == ks.mixing_grid:
            active_foods.append(food)

    active_foods_names = [active_foods[0].name, active_foods[1].name, active_foods[2].name]
    print(f'Active food names: {active_foods_names}')
    active_foods_names = sorted(active_foods_names)
    for recipe_result, recipe_ingredients in ks.current_full_formula.items():
        if active_foods_names == recipe_ingredients:
            ks.current_foods.append(Food(recipe_result, ks.bg, ks.pantry_grid))

            # C_box and SFX. Animate ingredients disappearing, then show new ingredient appearing at box.
            # Show new food name
            #ks.current_foods[-1].double_size()
            #clicked = False
            #while clicked == False:
            #    ks.current_foods[-1].refresh_img()
            #    clicked = ks.current_foods[-1].check_click()
            ks.current_foods[-1].fill_empty_cell(ks.pantry_grid.empty_cells)
            while active_foods:
                ks.current_foods.remove(active_foods[0])
                active_foods.remove(active_foods[0])
            ks.mixing_grid.empty_cells = ks.mixing_grid.grid[:]
    while active_foods:
        active_foods[0].switch_grid(ks.pantry_grid, ks.mixing_grid)
        active_foods.remove(active_foods[0])

def detect_events(icons):
    """Detect mouse and button clicks, then have the game respond."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            print(mouse_pos)
            for icon in icons:
                clicked = icon.check_click()
                if clicked == True:
                    icon.switch_grid(ks.pantry_grid, ks.mixing_grid)
            if len(ks.mixing_grid.empty_cells) == 0:
                ks.mix_button.refresh_img()
                clicked = ks.mix_button.check_click()
                if clicked:
                    check_mix_success()


# def win():
#     """When 1 food is left, show the win screen, then wait for input before changing to next level."""
#     if len(self.current_foods) == 1:
#
#         self.win_frame.screen.blit(self.bg.screen.center)
#         self.current_foods[0].double_size()
#         self.current_foods[0].place_button(self.bg.screen.center)
#         win_msg = Message('You made ' + self.current_foods[0].name.title() + '!')
#         win_msg.place((self.bg.screen.centerx, self.bg.screen.centery-20)
#
# def award_recipe():
#     """Give the player a new recipe to add to their collection."""
#     self.player_collection.append(new_product)
#
#     for recipe in self.player_collection:
#         recipe_button = Message(new_product)
#         recipe_menu.append(recipe_msg_object)
#     for recipe in recipe_menu:
#         recipe_frame.place(x, y)
#         recipe.place_button(x, y)
#         y += recipe.height
#     if recipe_menu.clicked:
#         recipe_frame = recipe_frame_image
#         recipe_title = Message(recipe_menu.name.title())
#         recipe_title.place(top center)
#         draw.rectangle? # TODO check if rounded rectangles are possible
#         product_obj.img_srf.double_size()
#         place product.centertop_belowtitle
#         for ingredient in ingredients:
#             ingredient_obj = Msg(ingredient.title())
#             ingredient_obj.img_surface.rect.topleft = (ingredient_msg_obj+20, ingredient_msg_obj[1]+5)
#             ingredient_obj.place(x, y)
#             y += 20
#
#     BUTTONS TO HAVE:
#         play
#         credits
#         quit
#         recipe collection
#     menu
#         current goal
#         main menu
#         recipe collection
#         quit

# Classes - music, sfx on click, sfx, mute
# front screen - play, recipe list, options,
# Music
# Recipe sheets / archives
# level query card
# branching - ethnicity-based cuisine, advanced levels.
# badges - american/fast food, korean, chinese, japanese, italian, french, german, uk/irish/scottish, russian, thai, vietnamese, cuban, puerto rican,
# 10 levels. 1-3 teaching levels. 4-7 regular levels. 8-9 challenging. 10 ultimate challenge.
# randomized level creator. based on - locale, dietary restrictions, tastes/preferences.





####    ####    ####    ####

pygame.init()



ks = Settings('ks_bg', ks_recipe_book)



def run_kitchen_scraps():
    """Run the main loop for the game Kitchen Scraps."""
    current_level = 0
    win = False
    ks.setup_new_level(current_level)
    while win == False:
        detect_events(ks.current_foods)
        ks.refresh_screen()
        if len(ks.mixing_grid.empty_cells) == 0:
            ks.mix_button.refresh_img()
        else:
            ks.bg.screen.blit(ks.mix_button.img_srf, ks.mix_button.rect)
        pygame.display.flip()
        if len(ks.current_foods) == 1:
            current_level += 1
            ks.setup_new_level(current_level)



run_kitchen_scraps()