
class Settings():
    """Maintain all setting variables for the game."""
    def __init__(self):
        """Construct/initialize variables for Settings."""
        # Initialize background and environmental elements.
        self.caption = pygame.display.set_caption('Kitchen Scraps - Cleanup Attempt 2, now with PyCharm!')
        self.bg = Background('ks_bg')
        self.pantry_grid = Grid(5, 5, origin=(50, 45), cell_size=(38, 38), grid_name='pantry grid')
        self.mixing_grid = Grid(1, 3, origin=(210, 120), cell_size=(38, 38), grid_name='mixing grid')
        # Initialize the Mix Button.
        self.mix_button = Button('mix')
        self.mix_button.rect.topleft = (250, 40)
        # Initialize food and recipe data.
        self.compendium = CraftCompendium(ks_ingredients, ks_recipe_book)
        self.ingredients_str = self.compendium.total_materials
        self.recipe_book = self.compendium.total_formulas
        self.ingredients_obj = self.convert_strings_to_foods(self.ingredients.str)
        #Initialize level data
        self.level_goals = ('bread', 'salad', 'classic_breakfast', 'three_course_drinks', 'full_course_meal')
        self.current_level = 0
    def convert_strings_to_foods(self, food_strings):
        """Use foods string list to make Food instances, then double Food img size."""
        foods = []
        for food_string in food_strings:
            new_food = ((Food(food_string, self.pantry_grid)))
            foods.append(new_food)
        return foods

    def double_coordinates(self, coordinates):
        """Return a double-sized coordinates tuple."""
        doubled_coordinates = (coordinates[0]*2, coordinates[1]*2)
        return doubled_coordinates

    def double_size(self, foods):
        """Double the size of everything. Screen, images, coordinates."""
        # TODO Can 'couble screen size' and 'double button size' be rolled into this too?
        self.bg.double_screen_size()
        self.mix_button.double_size()
        for food in foods:
            food.double_size()
        coordinates = [self.pantry_grid.origin, self.pantry_grid.cell_size,
                       self.mixing_grid.origin, self.mixing_grid.cell_size,
                       self.mix_button.rect.topleft]
        for coordinate in coordinates:
            coordinate = self.double_coordinates(coordinate*2)

    def halve_size(self, foods):
        """Halve the size of everything back to their original size."""
        # TODO When changing to new level and new foods, must ensure food sizes aren't thrown off-sync.
        print('Halve the sizes of: screen, images, coordinates, fonts.')










from ks_library import *
class CraftCompendium():
    """Contain all materials and formulas within a crafting system."""
    # Make an object. Create a Materials class. Include: name, image(s), description, category, tags, sources, stats,
    # quality, traits, invention ideas, effects, variants, recipe.

    def __init__(self, total_materials, total_formulas):
        self.total_formulas = total_formulas
        self.total_materials = total_materials
        self.total_products = self.total_formulas.keys()

compendium_test = CraftCompendium(ks_ingredients, ks_recipe_book)
print('Test the compendium!')
print(compendium_test.total_materials)
'''
classes: formulas/crafting. objects/sources/data. evolve/customize/grow.
tags/groups -
dictionary of tags, materials. anything material with the tag is added to the tag list.
also, dictionary of materials, tags. all materials also get a list of their related tags
if one is updated, so is the other. they stay in tandem.
connected tags - some tags are subcategories of other tags, like food > fruit. if fruit is included,
food auto-included too.
some tags are a 'type' of tag. for example, 'fashion' type tag.

locations, materials.
materials, locations.
for this, include the frequency/rarity within that location.
this can also be used for pets/creatures/wildlife.
shop - stores available, average cost,
generate object - some randomization, set the 'rarity', 'location', 'variants', etc.
class to make objects without recipe relation. just the object itself.
tags - locations - random spawning - object creation -

for recipe_results, recipe_ingredients in recipe_book.items():
    try:
        recipes[recipe_results] = sorted(recipe_ingredients)
    except TypeError:
        pass'''