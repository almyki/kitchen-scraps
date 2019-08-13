

ingredients = {
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
for ingredient, traits in ingredients.items():
    for food_group, group_items in food_groups.items():
        for trait in traits:
            if trait == food_group:
                group_items.append(ingredient)
# todo remove test
print(food_groups)


recipe_book = {
    'dough': ['wheat', 'egg', 'water'],
    'bread': ['dough', 'salt', 'yeast'],

    'dressing': ['vinegar', 'oil', 'herbs'],
    'salad': ['lettuce', 'vegetable', 'dressing'],

    'eggs_and_bacon': ['egg', 'meat', 'oil'],
    'orange_juice': ['orange', 'orange', 'orange'],
    'classic_breakfast': ['orange_juice', 'eggs_and_bacon', 'apple'],

    'fruit_juice': [food_groups['fruits'], food_groups['fruits'], 'water'],
    'vegetable_juice': [food_groups['vegetables'], food_groups['vegetables'], 'water'],
    'soy_milk': ['soybeans', 'nuts', 'water'],
    'three_course_drinks': ['fruit_juice', 'vegetable_juice', 'soy_milk'],

    'mayonnaise': ['egg', 'vinegar', 'oil'],
    'egg_sandwich': ['bread', 'egg', 'mayonnaise'],
    'ice_cream': ['cream', 'sugar', 'ice'],
    'full_course meal': ['salad', 'egg_sandwich', 'ice cream'],
    }
