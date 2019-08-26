
import pygame
from ks_library import *
from ks_environment import Background, Grid
from ks_buttons import GameImage, Frame, Button, Food
from craft_compendium import CraftCompendium




class Settings():
    """Define all the settings for the game Kitchen Scraps."""
    def __init__(self, bg_filename, recipe_book):
        """Initialize attributes for Settings."""
        self.bg = Background(bg_filename)
        self.caption = pygame.display.set_caption('Kitchen Scraps - Cleanup Attempt 2, now with PyCharm!')
        self.level_goals = ('bread', 'salad', 'classic breakfast', 'three-course drinks', 'full-course meal')
        self.recipe_book = CraftCompendium(recipe_book)
        self.mix_button = Button('mix', self.bg)
        self.mix_button.act_srf = self.mix_button.img_srf
        self.mix_button_pos = self.mix_button.place_image((270, 50))

        self.pantry = Frame('pantry', self.bg, (58, 60))
        self.pantry_spot = (self.pantry.rect[0] + 6, self.pantry.rect[1] + 6)
        self.pantry_grid = Grid(5, 5, cell_size=(38, 38), origin=(self.pantry_spot), grid_name='pantry grid')

        self.mixing_grid = Grid(1, 3, origin=(270, 130), grid_name='mixing grid')
        self.mixbox_1 = Frame('box_mix_gry', self.bg, self.mixing_grid.grid[0])
        self.mixbox_2 = Frame('box_mix_gry', self.bg, self.mixing_grid.grid[1])
        self.mixbox_3 = Frame('box_mix_gry', self.bg, self.mixing_grid.grid[2])
        self.mixboxes = [self.mixbox_1, self.mixbox_2, self.mixbox_3]
        for mixbox in self.mixboxes:
            mixbox.wht_srf = pygame.image.load('images/box_mix_wht.png')
            mixbox.gry_srf = pygame.image.load('images/box_mix_gry.png')
            mixbox.img_srfs.extend([mixbox.wht_srf, mixbox.gry_srf])

        self.result_box = Frame('box_questionmark', self.bg)
        result_box_center = (self.mixbox_2.rect.centerx, self.mixbox_2.rect.centery + self.result_box.rect[2]*0.8)
        self.result_box.place_image(result_box_center, 'center')
        self.result_box.q_srf = pygame.image.load('images/box_questionmark.png')
        self.result_box.x_srf = pygame.image.load('images/box_wrong.png')
        self.result_box.c_srf = pygame.image.load('images/box_correct.png')
        self.result_box.b_srf = pygame.image.load('images/box_blank.png')
        self.result_boxes = (self.result_box.q_srf, self.result_box.x_srf, self.result_box.c_srf)


    # def double_screen(self, double=True):
    #     if double == True:
    #         self.bg.double_screen_size()
    #         self.pantry_grid.double_size()
    #         self.mixing_grid.double_size()
    #         for food in self.current_foods:
    #             food.double_size()
    #         self.pantry_grid.fill_grid(self.bg.screen, self.current_foods)
    #         self.pantry.double_size()
    #         self.mix_button.double_size()
    #         for mixbox in self.mixboxes:
    #             mixbox.double_size()
    #         self.result_box.double_size()
    #     return True

    def setup_new_level(self, level_num):
        """Set the new level's items and images."""
        # Current Level
        self.current_goal = self.level_goals[level_num]
        self.current_full_formula = self.recipe_book.get_product_full_formula(self.current_goal)
        print(self.current_full_formula)
        self.current_all_materials = self.recipe_book.get_all_materials(self.current_full_formula, dupes=True)
        self.current_raw_ingredients = self.recipe_book.get_raw_materials(self.current_full_formula, dupes=True)

        self.current_foods = []
        for food in self.current_raw_ingredients:
            self.current_foods.append(Food(food, self.bg, self.pantry_grid))
        self.pantry_grid.fill_grid(self.bg.screen, self.current_foods)

    def refresh_screen(self):
        """Refresh all images on screen."""
        self.set_state()
        self.bg.refresh_screen()
        self.pantry.refresh_img()


        # TODO Enable this so it works whether double-screen or normal screen.
        #z = 0
        #for xy in self.mixing_grid.grid:
            #if xy not in self.mixing_grid.empty_cells:
            #    self.mixboxes[z].img_srf = self.mixboxes[z].double_srfs[1]
            #else:
            #    self.mixboxes[z].img_srf = self.mixboxes[z].double_srfs[0]
            #self.mixboxes[z].refresh_img()
            #z += 1
        self.result_box.refresh_img()
        #if self.mixing_grid.empty_cells == []:
        #    self.mix_button.img_srf = self.mix_button.double_srfs[1]
        #    self.mix_button.refresh_img()
        #else:
        #    self.mix_button.img_srf = self.mix_button.double_srfs[2]
        for food in self.current_foods:
            food.refresh_img()

    def set_state(self):
        """Decide the state of various frames and such."""
        z = 0
        for xy in self.mixing_grid.grid:
            if xy not in self.mixing_grid.empty_cells:
                self.mixboxes[z].img_srf = self.mixboxes[z].wht_srf
            else:
                self.mixboxes[z].img_srf = self.mixboxes[z].gry_srf
            z += 1













