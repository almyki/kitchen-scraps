
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

        pygame.display.flip()
        if len(ks.current_foods) == 1:
            current_level += 1
            ks.setup_new_level(current_level)



run_kitchen_scraps()