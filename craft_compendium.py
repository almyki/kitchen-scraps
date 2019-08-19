from ks_library import *

class Questionnaire():
    """Give user a list of numbered options.
    Allow them to choose an option with either its number, its name, or a related keyword option.
    Return error message if an invalid option is chosen.
    """

    def __init__(self, options):
        """Initialize attributes."""
        self.options = options

    def give_numbered_options(self, upper=False, styling='brackets'):
        """Return a list of things and have each item numbered with Title Caps or UPPER CAPS."""
        # TODO Consider how to make this neater.
        z = 1
        numbered_options = ''
        options = self.options
        # Check if the options are strings or lists of variations for each option. If so, convert to first variety.
        if isinstance(self.options[0], list) or isinstance(self.options[0], tuple):
            options = []
            for option_variations in self.options:
                options.append(option_variations[0])
        for option in options:
            if upper:
                option = option.upper()
            else:
                option = option.title()
            if styling == 'brackets':
                numbered_options += f'\n\t[{str(z)}] {option} '
            elif styling == 'dotted':
                numbered_options += f'\n\t{str(z)}. {option} '
            z += 1
        return numbered_options

    def give_options_request_choice(self, prompt=''):
        """Return a string prompt requesting the user input a number to choose from a list of options."""
        if not prompt:
            prompt = 'Please choose an option. You can choose by number too! '
        prompt += self.give_numbered_options(self.options)
        prompt += '\n*****     *****     *****     *****\n       >>> '
        user_input = input(prompt)
        user_input = user_input.lower()
        return user_input

    def check_if_valid_option(self, user_input):
        """Check if an input is a valid number from a list of numbered options. Return error message and False if not."""
        # TODO Check if these try-except statements work like I think they should. Consider breaking into two functions.
        try:
            user_input = int(user_input)
            try:
                user_input = self.options[user_input - 1]
                if isinstance(user_input, list) or isinstance(user_input, tuple):
                    user_input = user_input[0]
                return user_input
            except IndexError:
                print('OBJECTION! Sorry, that number\'s not a real option. Try again.')
                user_input = ''
                return user_input
        except ValueError:
            # Check if input_options is a list of tuples, used to include valid variations of each option.
            # If not, assume it's a list of strings and each option has only one valid string-type input.
            if user_input in self.options:
                return user_input
            else:
                print('HOLD IT! Sorry, please give me an option or the option\'s number.')
                user_input = ''
                return user_input

    def wait_for_user(self):
        """Wait for a button press before returning to the start of the while loop."""
        input('\nPress enter to continue \t>>>> ')
        return




class CraftCompendium():
    """Contain all materials and formulas within a crafting system."""
    # Make an object. Create a Materials class. Include: name, image(s), description, category, tags, sources, stats,
    # quality, traits, invention ideas, effects, variants, recipe.

    def __init__(self, total_formulas):
        self.total_formulas = self.sort_formulas_materials(total_formulas)
        self.total_materials = self.get_all_materials(self.total_formulas)
        self.total_products = sorted(self.total_formulas)
        self.total_raw_materials = self.get_raw_materials(self.total_formulas, dupes=False)
        self.total_full_formulas = self.get_all_full_formulas(self.total_formulas)
        self.total_tiers = self.get_all_tiers(self.total_formulas)
        self.final_products = self.total_tiers[-1]

        # Create surveys for the data interface.
        self.action_options = self.give_action_options()
        self.total_materials_options = Questionnaire(self.total_materials)
        self.total_products_options = Questionnaire(self.total_products)
        formatted_formulas = []
        for formula in self.total_formulas:
            formatted_formula = self.give_formula(formula, self.total_formulas)
            formatted_formulas.append(formatted_formula)
        self.total_formulas_options = Questionnaire(formatted_formulas)
        written_numbers = ('zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten')
        formatted_tiers = []
        z = 0
        for tier in range(len(self.total_tiers)):
            formatted_tiers.append('Tier ' + written_numbers[z].upper())
            z += 1
        self.total_tiers_options = Questionnaire(formatted_tiers)

    def sort_formulas_materials(self, formulas):
        """Sort all the formula material lists."""
        for materials in formulas.values():
            materials.sort()
        return formulas

    def get_all_materials(self, formulas, dupes=False):
        """Get a sorted list of all materials from a dictionary of formulas, with no duplicate materials."""
        all_materials = []
        for materials in formulas.values():
            for material in materials:
                all_materials.append(material)
        if dupes == False:
            all_materials = list(set(all_materials))
        all_materials.sort()
        return all_materials

    def get_raw_materials(self, formulas, dupes=False):
        """Return a sorted list of only the raw materials from a collection of formulas.
        This doesn't remove dupes or category items, so it will include ALL materials needed for a full formula.
        """
        raw_materials = []
        for materials in formulas.values():
            for material in materials:
                if material not in formulas.keys():
                    raw_materials.append(material)
        if dupes == False:
            raw_materials = list(set(raw_materials))
        raw_materials.sort()
        return raw_materials

    def get_product_full_formula(self, req_product):
        """Search through all formulas to return a dictionary of all formulas needed for a product."""
        if req_product not in self.total_formulas.keys():
            print(f'Huh?! [ {req_product} ] is not a real product. Try again!')
            return
        product_full_formula = {}
        product_full_formula[req_product] = self.total_formulas[req_product]
        products = [req_product]
        for product in products:
            for material in product_full_formula[product]:
                if material in self.total_formulas.keys():
                    product_full_formula[material] = self.total_formulas[material]
                    products.append(material)
        return product_full_formula

    def get_all_full_formulas(self, formulas):
        """Return a dictionary of dictionaries including all the full formulas from a formulas collection."""
        # TODO Is this really needed?
        full_formulas = {}
        for product in formulas.keys():
            product_full_formula = self.get_product_full_formula(product)
            full_formulas[product] = product_full_formula
        return full_formulas

    def get_tier_one_products(self, formulas):
        """Return a sorted list of products that only require raw materials, no dupes."""
        upper_tier_products = set()
        tier_one_products = set()
        for product, materials in formulas.items():
            for material in materials:
                if material in formulas.keys():
                    upper_tier_products.add(product)
        for product in formulas.keys():
            if product not in upper_tier_products:
                tier_one_products.add(product)
        tier_one_products = sorted(tier_one_products)
        return tier_one_products

    def get_next_tier_products(self, prev_tier_products, formulas):
        """Return a list of products that require a material of the previous tier"""
        next_tier_products = []
        for product, materials in formulas.items():
            valid = True
            if product not in prev_tier_products:
                for material in materials:
                    if (material not in prev_tier_products) and (material not in self.total_raw_materials):
                        valid = False
                if valid == True:
                    next_tier_products.append(product)
        next_tier_products.sort()
        return next_tier_products

    def get_all_tiers(self, formulas):
        """Return a list containing lists of products for each tier from a formulas collection, following the index."""
        tier_one_products = self.get_tier_one_products(formulas)
        tiers = [tier_one_products]
        prev_tier_products = tier_one_products[:]
        # Check if this truly captures all the tier products
        for tier in tiers:
            next_tier = self.get_next_tier_products(prev_tier_products, formulas)
            if next_tier:
                tiers.append(next_tier)
                for product in next_tier:
                    prev_tier_products.append(product)
        tier0_raw_materials = self.get_raw_materials(self.total_formulas)
        tiers.insert(0, tier0_raw_materials)
        return tiers

    def give_formula(self, req_product, formulas, include_tier=False):
        """Return the inputted formula like so: Product = Material 1, Material 2, Material 3[...]"""
        z=0
        formula_msg = '[ ' + req_product.upper() + ' = '
        for material in formulas[req_product]:
            for tier in self.total_tiers:
                if material in tier:
                    tier_num = self.total_tiers.index(tier)
                    break
            if include_tier:
                formula_msg += material.title() + ' *' + str(tier_num)
            else:
                formula_msg += material.title()
            z += 1
            if z < len(formulas[req_product]):
                formula_msg += ', '
            else:
                formula_msg += ' ]'
        return formula_msg

    def give_action_options(self):
        """Prompt the user for what information they'd like from the compendium."""
        req_total_materials = ['total materials list',]
        req_total_products = ['total products list',]
        req_total_formulas = ['total formulas list',]
        req_total_tiers = ['total tiers list',]
        req_product_raw_materials = ['request raw materials needed for...',]
        req_product_materials = ['request all materials from...',]
        req_full_formula = ['request the full formula for...',]
        req_tier_x_products = ['request products of tier...',]
        req_product_formula = ['request the formula for...']
        req_formulas_with_x = ['request formulas that use...',]

        action_options_all = [req_total_materials, req_total_products, req_total_formulas, req_total_tiers,
                            req_product_raw_materials, req_product_materials, req_full_formula, req_tier_x_products,
                            req_product_formula, req_formulas_with_x,
                            ]
        return action_options_all



    def option_output(self, user_input):
        """Reply according to the user's input option."""
        if user_input == self.action_options[0][0]:
            print('\nThe Total Materials List: ')
            materials_info = self.total_materials_options.give_numbered_options(styling='dotted')
            print(materials_info)
            self.total_materials_options.wait_for_user()
        elif user_input == self.action_options[1][0]:
            print('\nThe Total Products List: ')
            products_info = self.total_products_options.give_numbered_options(styling='dotted')
            print(products_info)
            self.total_products_options.wait_for_user()
        elif user_input == self.action_options[2][0]:
            print('\nThe Total Formulas List: ')
            formulas_info = self.total_formulas_options.give_numbered_options(styling='dotted')
            print(formulas_info)
            self.total_formulas_options.wait_for_user()
        elif user_input == self.action_options[3][0]:
            print('\nThe Total Tier List: ')
            tiers_info = self.total_tiers_options.give_numbered_options(styling='dotted')
            print(tiers_info)
            self.total_tiers_options.wait_for_user()
        elif user_input == self.action_options[4][0]:
            print('\nRequest the Raw Materials needed for...? ')
            user_choice = self.total_products_options.give_options_request_choice()
            user_choice = self.total_products_options.check_if_valid_option(user_choice)
            if user_choice:
                print('\nThese are all the raw ingredients needed for \'' + user_choice.title() + '\'!')
                req_full_formula = self.get_product_full_formula(user_choice)
                req_product_raws = self.get_raw_materials(req_full_formula, dupes=True)
                print(req_product_raws)
            self.total_formulas_options.wait_for_user()
        elif user_input == self.action_options[5][0]:
            print('\nRequest all materials from what formula?')
            user_choice = self.total_products_options.give_options_request_choice()
            user_choice = self.total_products_options.check_if_valid_option(user_choice)
            if user_choice:
                print('\nThese are all the materials in the formula of \'' + user_choice.title() + '\'!')
                req_full_formula = self.get_product_full_formula(user_choice)
                req_product_materials = self.get_all_materials(req_full_formula, dupes=False)
                print(req_product_materials)
            self.total_formulas_options.wait_for_user()
        elif user_input == self.action_options[6][0]:
            print('\nRequest the full formula for what product?')
            user_choice = self.total_products_options.give_options_request_choice()
            user_choice = self.total_products_options.check_if_valid_option(user_choice)
            if user_choice:
                print('\nThis is the full formula on how to create \'' + user_choice.title() + '\'!')
                req_full_formula = self.get_product_full_formula(user_choice)
                for formula in req_full_formula:
                    formatted_formula = self.give_formula(formula, req_full_formula)
                    print(formatted_formula)
            self.total_formulas_options.wait_for_user()
        elif user_input == self.action_options[7][0]:
            print('\nRequest the products of what tier?')
            user_choice = self.total_tiers_options.give_options_request_choice()
            user_choice = self.total_tiers_options.check_if_valid_option(user_choice)
            if user_choice:
                if user_choice == 'tier one':
                    print(self.total_tiers[1])
                elif user_choice == 'tier two':
                    print(self.total_tiers[2])
                elif user_choice == 'tier three':
                    print(self.total_tiers[3])
                elif user_choice == 'tier four':
                    print(self.total_tiers[4])
                elif user_choice == 'tier five':
                    print(self.total_tiers[5])
                else:
                    print('aMira, you need to add more options. Also, this is really ugly code!')
            self.total_formulas_options.wait_for_user()
        elif user_input == self.action_options[8][0]:
            print('I\'m too lazy to do this one now.')
        elif user_input == self.action_options[9][0]:
            print('\nRequest formulas that use what ingredient?')
            user_choice = self.total_materials_options.give_options_request_choice()
            user_choice = self.total_materials_options.check_if_valid_option(user_choice)
            if user_choice:
                formulas_with_x = {}
                for product, materials in self.total_formulas.items():
                    if user_choice in materials:
                        formulas_with_x[product] = materials
                for formula in formulas_with_x:
                    formatted_formula = self.give_formula(formula, formulas_with_x)
                    print(formatted_formula)
            self.total_formulas_options.wait_for_user()

# TODO Add:
#  request raw materials for one product, all materials for one product,
#  product formula, product full formula,
#  tier x products, formula with x

#         elif user_input in req_product_raw_materials:
#             product_choice = self.request_product_choice('For what end-product do you want to know the raw materials?')
#             product_raw_materials = self.get_raw_materials(product_choice)
#             give_numbered_list(product_raw_materials)
#         elif user_input in req_product_materials:
#             product_choice = self.request_product_choice(
#                 'For what end-product do you want to know all related materials?')
#             product_materials = self.get_product_full_formula_and_materials(product_choice, get_this='materials')
#             give_numbered_list(product_materials)
#         elif user_input in req_product_formula:
#             product_choice = self.request_product_choice('For what end-product do you want to know the formula?')
#             self.give_formula(product_choice, self.total_formulas)
#         elif user_input in req_full_formula:
#             product_choice = self.request_product_choice('For what end-product do you want to know the FULL formula?')
#             full_formula = get_product_full_formula_and_materials(get_this='formula')
#             for product in full_formula.keys():
#                 self.give_formula(product, full_formula)
        # while True:
        #     user_input = give_options_and_request_choice(cc_input_options)
        #     valid_opt = check_if_valid_option(user_input, cc_input_options_all_variants)
        #     if not valid_opt:
        #         break
        #     else:
        #         if user_input in req_total_materials:
        #             give_numbered_list(self.total_materials)
        #         elif user_input in req_total_products:
        #             give_numbered_list(self.total_products)
        #         elif user_input in req_total_formulas:
        #             give_numbered_list(self.total_formulas)
        #         elif user_input in req_total_tiers:
        #             give_numbered_list(self.total_tiers)
        #
        #         elif user_input in req_product_raw_materials:
        #             product_choice = self.request_product_choice(
        #                 'For what end-product do you want to know the raw materials?')
        #             product_raw_materials = self.get_raw_materials(product_choice)
        #             give_numbered_list(product_raw_materials)
        #         elif user_input in req_product_materials:
        #             product_choice = self.request_product_choice(
        #                 'For what end-product do you want to know all related materials?')
        #             product_materials = self.get_product_full_formula_and_materials(product_choice,
        #                                                                             get_this='materials')
        #             give_numbered_list(product_materials)
        #         elif user_input in req_product_formula:
        #             product_choice = self.request_product_choice(
        #                 'For what end-product do you want to know the formula?')
        #             self.give_formula(product_choice, self.total_formulas)
        #         elif user_input in req_full_formula:
        #             product_choice = self.request_product_choice(
        #                 'For what end-product do you want to know the FULL formula?')
        #             full_formula = get_product_full_formula_and_materials(get_this='formula')
        #             for product in full_formula.keys():
        #                 self.give_formula(product, full_formula)
        #
        #         elif user_input in req_tier_x_products:
        #             # msg = 'For what tier would you like to know all the products included?'
        #             # tier_choice = give_options_and_request_choice(self.total_tiers, msg)
        #             # tier_choice = check_if_valid_option(tier_choice, self.total_products)
        #             print('Let\'s test this functionality later, Mira!')
        #         elif user_input in req_formulas_with_x:
        #             msg = 'For what material would you like to know all the products that they\'re included in?'
        #             material_choice = give_options_and_request_choice(self.total_materials, msg)
        #             material_choice = check_if_valid_option(tier_choice, self.total_materials)
        #             formulas_with_x = {}
        #             for product, materials in self.total_formulas.items():
        #                 if material_choice in materials:
        #                     formulas_with_x['product'] = materials
        #             for product in formulas_with_x.keys():
        #                 self.give_formula(product, formulas_with_x)
        #         else:
        #             print('Hey, Mira! Something went wrong >:[ !! FIX IT!')

    # def request_product_choice(self, msg='Please choose a product to analyze:'):
    #     """Request a choice from the list of all products given and return the product choice."""
    #     product_choice = give_options_and_request_choice(self.total_products, msg)
    #     product_choice = check_if_valid_option(product_choice, self.total_products)
    #     return product_choice




#####    ####    ####    ####1

compendium_test = CraftCompendium(ks_recipe_book)

def testing():
    print('TESTING!')
    print('My total materials:')
    print(compendium_test.total_materials)
    print('My total formulas:')
    print(compendium_test.total_formulas)
    print('My total products:')
    print(compendium_test.total_products)
    print('My total raw materials:')
    print(compendium_test.total_raw_materials)

    print('\n***** TESTING METHODS NOW *****\n')
    print('\tTesting Get Total Materials:')
    total_materials = compendium_test.get_all_materials(compendium_test.total_formulas)
    print(total_materials)

    print('\tTesting Get Raw Materials:')
    raw_materials = compendium_test.get_raw_materials(compendium_test.total_formulas)
    print(raw_materials)

    print('\n\tTesting Get Product\'s Full Formula:')
    egg_sandwich_full_formula_valid = compendium_test.get_product_full_formula('egg_sandwich')
    print(egg_sandwich_full_formula_valid)

    print('\n\tTesting Get Product\'s Full Material List:')
    #egg_sandwich_full_formula = compendium_test.get__product_full_formula('egg sandwich')
    egg_sandwich_full_formula_valid = compendium_test.get_product_full_formula('egg_sandwich')
    raws_egg_sandwich = compendium_test.get_raw_materials(egg_sandwich_full_formula_valid)
    print('All products within egg sandwich full formula:')
    print(egg_sandwich_full_formula_valid.keys())

    print('All raw ingredients in egg sandwich full formulas:')
    print(raws_egg_sandwich)
    print(egg_sandwich_full_formula_valid)

    print('\n\tTesting Get ALL Full Formulas:')
    for product, full_formula in compendium_test.total_full_formulas.items():
        print(product.title())
        print(full_formula)

    print('\n\tTesting Get Product\'s Tier 1 Product List:')
    tier_one_products = compendium_test.get_tier_one_products(compendium_test.total_formulas)
    print(tier_one_products)

    print('\n\tTesting Get Next Tier Product List')
    next_tier_products = compendium_test.get_next_tier_products(tier_one_products, compendium_test.total_formulas)
    print(next_tier_products)

    print('\n\tProducts by tier list and tier length:')
    print(compendium_test.total_tiers)
    print(compendium_test.total_tiers[0])

    print('\n\tSeparate crafting and final products:')
    print(compendium_test.total_products)
    print(compendium_test.total_raw_materials)

    compendium_test.give_formula('egg_sandwich', compendium_test.total_formulas)

print(compendium_test.action_options)
craft_system = Questionnaire(compendium_test.action_options)
while True:
    user_choice = craft_system.give_options_request_choice()
    user_choice = craft_system.check_if_valid_option(user_choice)
    compendium_test.option_output(user_choice)