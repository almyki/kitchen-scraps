
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
        self.mix_button.def_srf = self.mix_button.img_srf
        self.mix_button_pos = self.mix_button.place_image((270, 50))

        self.pantry = Frame('pantry', self.bg, (58, 60))
        self.pantry_spot = (self.pantry.rect[0] + 6, self.pantry.rect[1] + 6)
        self.pantry_grid = Grid(5, 5, cell_size=(38, 38), origin=(self.pantry_spot), grid_name='pantry grid')

        self.mixing_grid = Grid(1, 3, origin=(270, 130), grid_name='mixing grid')
        self.mixboxes = []
        for index in range(0, len(self.mixing_grid.grid)):
            self.mixboxes.append(Frame('box_mix', self.bg, self.mixing_grid.grid[index]))

        self.result_box = Frame('box_questionmark', self.bg)
        result_box_center = (self.mixboxes[1].rect.centerx, self.mixboxes[1].rect.centery + self.result_box.rect[2]*0.8)
        self.result_box.place_image(result_box_center, 'center')
        self.result_box.q_srf = pygame.image.load('images/box_questionmark.png')
        self.result_box.x_srf = pygame.image.load('images/box_wrong.png')
        self.result_box.c_srf = pygame.image.load('images/box_correct.png')
        self.result_box.b_srf = pygame.image.load('images/box_blank.png')
        self.result_boxes = (self.result_box.q_srf, self.result_box.x_srf, self.result_box.c_srf)

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
        z = 0
        for xy in self.mixing_grid.grid:
        #    if xy not in self.mixing_grid.empty_cells:
        #       self.mixboxes[z].img_srf = self.mixboxes[z].def_srf
        #    else:
        #       self.mixboxes[z].img_srf = self.mixboxes[z].gry_srf
            self.mixboxes[z].refresh_img()
            z += 1
        mixed = True
        #if len(self.mixing_grid.empty_cells) > 0:
        #self.bg.screen.blit(self.mix_button.img_srf, self.mix_button.rect)

        if self.mixing_grid.empty_cells:
            self.mix_button.img_srf = self.mix_button.gry_srf
            self.bg.screen.blit(self.mix_button.img_srf, self.mix_button.rect)
        else:
            self.mix_button.img_srf = self.mix_button.def_srf
            self.mix_button.refresh_img()
        for food in self.current_foods:
            food.refresh_img()


    def
        successful_mix = False
        if successful_mix:
            self.bg.darken_screen()
            self.result_box.refresh_img()
            self.apple_win.refresh_img()
        else:
            self.result_box.refresh_img()
            self.apple_win = self.display_item('apple')

    def check_mix_success(self):
        """If it's a successful recipe, combine into new food. If not, return items to shelf.
        Create a list of the active foods, then make a copy of the food name strings,
        then sort the copy to compare with the recipes.
        """
        mixed = self.mix_button.check_click()
        if mixed:
            active_foods = []
            for food in self.current_foods:
                if food.grid == self.mixing_grid:
                    active_foods.append(food.name)
            active_foods = sorted(active_foods)
            for product, materials in self.current_full_formula.items():
                if active_foods == materials:
                    return product

    def display_results(self):
        """Show the successful mix if successful. Otherwise, return items to pantry."""
        successful_mix = self.check_mix_success()
        if successful_mix:
            result = self.display_item(successful_mix)


                self.current_foods.append(Food(product, self.bg, self.pantry_grid))


                self.current_foods[-1].fill_empty_cell(self.pantry_grid.empty_cells)
                while active_foods:
                    self.current_foods.remove(active_foods[0])
                    active_foods.remove(active_foods[0])
                self.mixing_grid.empty_cells = self.mixing_grid.grid[:]
        while active_foods:
            active_foods[0].switch_grid(self.pantry_grid, self.mixing_grid)
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

    def display_item(self, item):
        """Show the item in the center of the results box, double-sized."""
        display_item = Button(item, self.bg)
        display_item.img_srf = pygame.transform.scale2x(display_item.img_srf)
        display_item.hvr_srf = pygame.transform.scale2x(display_item.hvr_srf)
        display_item.rect = display_item.img_srf.get_rect()
        display_item.rect.center = self.result_box.rect.center
        self.bg.screen.blit(display_item, display_item.rect)
        return display_item

    def wait_for_result_click(self):
        """Wait for the click on the result item, then transfer the result to the pantry and reenable the screen."""
        clicked = display_item.check_click()
        if clicked:
            self.current_foods.append(Food(display_item.name, self.bg, self.pantry_grid))
            # Wipe the display item.


    def set_state(self):
        """Decide the state of various frames and such."""
        z = 0
        for xy in self.mixing_grid.grid:
            if xy not in self.mixing_grid.empty_cells:
                self.mixboxes[z].img_srf = self.mixboxes[z].def_srf
            else:
                self.mixboxes[z].img_srf = self.mixboxes[z].gry_srf
            z += 1
        # for box in self.mixboxes:
        #     if box.rect.topleft in self.mixing_grid.empty_cells:
        #         box.img_srf = box.gry_srf
        #     else:
        #         box.img_srf = box.gry_srf













