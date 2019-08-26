
# Contains basic Utilities class functions and the elements for the Kitchen Scraps game. Aka the Formulas.

class Utilities():
    """Stick any undecided, general-use functions in here. Things that don't require any particular 'object'."""

    def __init__(self):
        """This should stay as empty as possible."""

    def convert_to_codehappy_string(self, string):
        codehappy_string = ''
        for character in string:
            if character == ' ':
                codehappy_string += '_'
            else:
                codehappy_string += character
        return codehappy_string

    def double_size_screen(self):
        """Double the size of all elements of the screen."""
        pass

    def original_size_screen(self):
        """Revert back to the original size of all elements."""
        pass

ks_ingredients = {
    'water': ['liquid'],
    'wheat': ['grain'],
    'eggs': ['animal produce'],
    'dough': ['grain produce'],
    'salt': ['seasoning'],
    'yeast': ['other'],
    'bread': ['grain produce'],
    'vinegar': ['seasoning'],
    'oil': ['seasoning'],
    'herbs': ['seasoning'],
    'dressing': ['seasoning'],
    'lettuce': ['vegetable'],
    'tomato': ['vegetable'],
    'salad': ['dish'],
    'meat': ['meat'],
    'eggs and bacon': ['dish', 'meat'],
    'apple': ['fruit'],
    'orange': ['fruit'],
    'orange juice': ['drink'],
    'classic breakfast': ['meal', 'meat'],
    'soybeans': ['nuts'],
    'nuts': ['nuts'],
    'carrot': ['vegetable'],
    'fruit juice': ['drink'],
    'vegetable juice': ['drink'],
    'soymilk': ['drink'],
    'three course drink': ['drink', 'meal'],
    'mayonnaise': ['animal produce'],
    'egg sandwich': ['animal produce', 'dish'],
    'cream': ['dairy'],
    'sugar': ['seasoning'],
    'ice': ['other'],
    'ice cream': ['dairy', ],
    'full course meal': ['dairy', 'meal'],
    }


# Sort ingredients into food groups.
food_groups = {
    'fruits': [],
    'vegetables': [],
    }
for ingredient, traits in ks_ingredients.items():
    for food_group, group_items in food_groups.items():
        for trait in traits:
            if trait == food_group:
                group_items.append(ingredient)




ks_recipe_book = {
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

