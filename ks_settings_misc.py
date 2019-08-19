
import pygame
from ks_library import *
from ks_environment import Background, Grid
from ks_buttons import Button, Food

print('Testing the Compendium:')

def give_options_and_request_choice(input_options, prompt='Please choose an option by entering a number: '):
    """Return a string prompt requesting the user input a number to choose from a list of options."""
    z = 1
    for input_option in input_options:
        prompt += f'\n    [{z}] {input_option[0].title()}'
    prompt += '*****     *****     *****     *****\n\n\n       >>> '
    user_input = input(prompt)
    user_input = user_input.lower()
    return user_input
print('check if valid option')
def check_if_valid_option(user_input, input_options):
    """Check if an input is a valid number from a list of numbered options. Return error message and False if not."""
    # TODO Check if these try-except statements work like I think they should. Consider breaking into two functions.
    try:
        user_input = int(user_input)
        try:
            user_input = input_options[user_input - 1]
            return user_input
        except IndexError:
            print('HEY, WAIT! Sorry, that number\'s not a real option. Try again.')
            return
    except TypeError:
        # Check if input_options is a list of tuples, used to include valid variations of each option.
        # If not, assume it's a list of strings and each option has only one valid string-type input.
        if input_options[0] == type(tuple):
            for input_option in input_options:
                if user_input in input_option:
                    return input_option[0]
        elif user_input in input_options:
            return user_input
        else:
            print('HEY, WAIT! Sorry, please give me an option or the option\'s number.')
            return
print('give numbered list')
def give_numbered_list(listothings):
    """Print a list of things and have each item numbered with Title Caps."""
    z = 1
    for thing in listothings:
        print(f'    {z}. {thing.title()}')
        z += 1




print('the craft compendium class')
class CraftCompendium():
    """Contain all materials and formulas within a crafting system."""
    # Make an object. Create a Materials class. Include: name, image(s), description, category, tags, sources, stats,
    # quality, traits, invention ideas, effects, variants, recipe.

    def __init__(self, total_formulas):
        self.total_formulas = total_formulas
        self.total_materials = self.get_total_materials(self.total_formulas)
        self.total_raw_materials = self.get_raw_materials(self.total_formulas)
        self.total_products = self.total_formulas.keys()
        self.total_first_tier_products = self.get_tier_one_products()
        self.total_crafting_products = self.separate_crafting_and_final_products('crafting products')
        self.total_final_products = self.separate_crafting_and_final_products('final products')
        self.total_full_formulas = self.get_full_formulas()
        self.total_tiers = self.get_all_tiers()

    def get_total_materials(self, formulas):
        """Get a list of all materials from a dictionary of formulas. Strip all dupes."""
        total_materials = set()
        for product, materials in formulas.items():
            total_materials.update(product)
            total_materials.update(materials)

    def get_raw_materials(self, formulas=''):
        """Return a list of only the raw materials from a collection of formulas."""
        if not formulas:
            formulas = self.total_formulas
        raw_materials = []
        for materials in formulas.values():
            for material in materials:
                if material not in formulas.keys():
                    raw_materials.append(material)
        return raw_materials

    def get_product_full_formula_and_materials(self, product, get_this='both'):
        """Search through all formulas to return a dictionary of all formulas needed for a product."""
        # The formula dictionary goes in order from top-level product down to the root-level product(s).
        product_full_materials = [product]
        product_full_formula = {}
        for gathered_material in product_full_materials:
            for formula_product, formula_materials in self.total_formulas.items():
                if formula_product == gathered_material:
                    for formula_material in formula_materials:
                        product_full_materials.append(formula_material)
                    product_full_formula[formula_product] = formula_materials
        if get_this == 'formula':
            return product_full_formula
        elif get_this == 'materials':
            return product_full_materials
        else:
            return product_full_formula, product_full_materials

    def get_full_formulas(self, formulas=''):
        """Return a list of dictionaries including all the full formulas of a formulas collection."""
        if not formulas:
            formulas = self.total_formulas
        full_formulas = []
        for product in formulas.keys():
            product_full_formula = self.get_product_full_formula_and_materials(product, get_this='full formula')
            full_formulas.append(product_full_formula)
        return full_formulas

    def get_tier_one_products(self, formulas=''):
        """Return a list of products that only require raw materials."""
        if not formulas:
            formulas = self.total_formulas
        upper_tier_products = []
        tier_one_products = []
        for product, materials in formulas.items():
            for material in materials:
                if material in formulas.keys():
                    upper_tier_products.append(product)
        for product in formulas.keys():
            if product not in upper_tier_products:
                tier_one_products.append(product)
        return tier_one_products

    def get_next_tier_products(self, prev_tier_products, formulas=''):
        """Return a list of products that require a material of the previous tier"""
        if not formulas:
            formulas = self.total_formulas
        tier_products = []
        for product, materials in formulas.items():
            for material in materials:
                if material in prev_tier_products:
                    tier_products.append(product)
        return tier_products

    def get_all_tiers(self, formulas=''):
        """Return a list containing lists of products for each tier from a formulas collection, following the index."""
        if not formulas:
            formulas = self.total_formulas
        tier_one_products = self.get_tier_one_products(formulas)
        tiers = [tier_one_products]
        # Check if this truly captures all the tier products
        for tier in tiers:
            next_tier = self.get_next_tier_products(tier)
            tiers.append(next_tier)
        return tiers


    def give_results(self):
        """Prompt the user for what information they'd like from the compendium."""
        req_total_materials = ('total materials list',)
        req_total_products = ('total products list',)
        req_total_formulas = ('total formulas list',)
        req_total_tiers = ('total tiers list',)
        req_product_raw_materials = ('request raw materials needed for...',)
        req_product_materials = ('request all materials from...',)
        req_full_formula = ('request the full formula for...',)
        req_tier_x_products = ('request products of tier...',)
        req_product_formula = ('request the formula for...',)
        req_formulas_with_x = ('request formulas that use...',)
        
        cc_input_options_all_variants = [req_total_materials, req_total_products, req_total_formulas, req_total_tiers,
            req_product_raw_materials, req_product_materials, req_full_formula, req_tier_x_products,
            req_product_formula, req_formulas_with_x,
            ]
        cc_input_options = []
        for option in cc_input_options_all_variants:
            cc_input_options.append(option[0])
        print('Start up the questionnaire:')
        while True:
            user_input = give_options_and_request_choice(cc_input_options)
            valid_opt = check_if_valid_option(user_input, cc_input_options_all_variants)
            if not valid_opt:
                break
            else:
                if user_input in req_total_materials:
                    give_numbered_list(self.total_materials)
                elif user_input in req_total_products:
                    give_numbered_list(self.total_products)
                elif user_input in req_total_formulas:
                    give_numbered_list(self.total_formulas)
                elif user_input in req_total_tiers:
                    give_numbered_list(self.total_tiers)

                elif user_input in req_product_raw_materials:
                    product_choice = self.request_product_choice('For what end-product do you want to know the raw materials?')
                    product_raw_materials = self.get_raw_materials(product_choice)
                    give_numbered_list(product_raw_materials)
                elif user_input in req_product_materials:
                    product_choice = self.request_product_choice('For what end-product do you want to know all related materials?')
                    product_materials = self.get_product_full_formula_and_materials(product_choice, get_this='materials')
                    give_numbered_list(product_materials)
                elif user_input in req_product_formula:
                    product_choice = self.request_product_choice('For what end-product do you want to know the formula?')
                    self.give_formula(product_choice, self.total_formulas)
                elif user_input in req_full_formula:
                    product_choice = self.request_product_choice('For what end-product do you want to know the FULL formula?')
                    full_formula = get_product_full_formula_and_materials(get_this='formula')
                    for product in full_formula.keys():
                        self.give_formula(product, full_formula)

                elif user_input in req_tier_x_products:
                    # TODO Test out tier product list building.
                    # msg = 'For what tier would you like to know all the products included?'
                    # tier_choice = give_options_and_request_choice(self.total_tiers, msg)
                    # tier_choice = check_if_valid_option(tier_choice, self.total_products)
                    print('Let\'s test this functionality later, Mira!')
                elif user_input in req_formulas_with_x:
                    msg = 'For what material would you like to know all the products that they\'re included in?'
                    material_choice = give_options_and_request_choice(self.total_materials, msg)
                    material_choice = check_if_valid_option(tier_choice, self.total_materials)
                    formulas_with_x = {}
                    for product, materials in self.total_formulas.items():
                        if material_choice in materials:
                            formulas_with_x['product'] = materials
                    for product in formulas_with_x.keys():
                        self.give_formula(product, formulas_with_x)
                else:
                    print('Hey, Mira! Something went wrong >:[ !! FIX IT!')

    def request_product_choice(self, msg='Please choose a product to analyze:'):
        """Request a choice from the list of all products given and return the product choice."""
        product_choice = give_options_and_request_choice(self.total_products, msg)
        product_choice = check_if_valid_option(product_choice, self.total_products)
        return product_choice

    def give_formula(req_product, formulas):
        """Print the inputted formula like so: Product = Material 1, Material 2, Material 3[...]"""
        if not formulas:
            formulas = self.total_formulas
        for product, materials in formulas.items():
            if product == req_product:
                formula_string = product.title() + ' = '
                for material in materials:
                    formula_string += material.title() + ', '
        print(formula_string)



print('before making the craft compendium')
# It works up to here. The craft compendium has a problem.
ks_compendium = CraftCompendium(ks_ingredients, ks_recipe_book)

print('Is this working?!!?!')
ks_compendium.give_results()
print(ks_compendium.total_materials)
