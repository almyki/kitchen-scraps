
#### Main module for the game Kitchen Scraps.

import sys
import pygame
from PIL import Image
from ks_environment import Background, Grid, ActiveImage, Button, DetectEvents
from ks_settings import Settings
from craft_compendium import CraftCompendium

# TODO change box to ? after starting new combo.
#  change to check after mixing, then change to ingredient after click.
#  change so the grid fills empty spot even after new level et cetera.


ks = Settings('ks_bg')

# Set up the game and level.
pygame.init()
pygame.mixer.music.load('sounds/' + ks.music + '.mp3')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

ks.set_level()
while True:
    ks.refresh_screen()
    # TODO Show Level Prompt Card.

    # Detect user events. If mouse-click, return the clicked element and act on it.
    clicked_button = ks.check_buttons()
    # If button is food item, switch grid if possible.
    if clicked_button:
        if clicked_button.name in ks.current_foods and clicked_button.active:
            ks.switch_grid(clicked_button)
        # If button is 'Mix' and 'Mix' is active, try the mix. Activate and return O/X for Result Box.
        elif clicked_button == ks.mix_button and ks.mix_button.active:
            ks.big_box.result = ks.mix_ingredients()
            ks.big_box.disable_all_except_self(ks.buttons)
        # If Result Box is active, proceed on user input based on success or failure.
        elif clicked_button == ks.big_box and ks.big_box.active:
            # If Result is Success, show result food in Result Box and wait for another input.
            if ks.big_box.success:
                ks.sfx_click.play()
                ks.big_box.fill_big_box(ks.big_box.result)
                ks.buttons.append(ks.big_box.result)
            # If Result is Failure, return food to pantry.
            else:
                ks.sfx_denied.play()
                for material in ks.mixing_grid.grid.values():
                    ks.switch_grid(material)
                for button in ks.buttons:
                    button.active = True
                ks.big_box.result = ''
            ks.big_box.active = False
        # If Result Product is displayed, wait for user input before continuing the game.
        elif clicked_button == ks.big_box.result:
            ks.erase_mix_materials()
            if clicked_button.name != ks.current_goal:
                ks.confirm_result_and_cont()
            # TODO If player wins, show Win Card and wait for input. Level up and reset screen when user proceeds.
            elif clicked_button.name == ks.current_goal:
                ks.level += 1
                if ks.level < len(ks.goals):
                    ks.set_level()
            else:
                print('Hey, congrats, you win! I don\'t have any more levels yet. Thanks for playing =3= !')
    pygame.display.flip()




####
