
# The class 'CraftCompendium' can be used for any crafting system.
# TODO Add ability to sort by category and tags.

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

    def sort_formulas_materials(self, formulas):
        """Sort all the formula material lists."""
        for materials in formulas.values():
            materials.sort()
        return formulas

    def get_formula_products(self, req_product):
        """Return a list of all the products created within a full formula."""
        products = [req_product]
        full_formula = self.get_product_full_formula(req_product)
        for product in full_formula.keys():
            products.append(product)
        return products

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
        """Return the inputted formula like so: [ PRODUCT = Material 1, Material 2, Material 3, ... ]"""
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

    # def assign_tags(self):
    #
    #     tags = {
    #         'seasoning': ['dressing', 'herbs', 'salt', 'vinegar', 'oil', ],
    #         'meat': ['red meat', ],
    #         'dairy': [],
    #         'animal byproduct': ['egg', ],
    #         'fruit': ['apple', 'orange', ],
    #         'vegetable': ['carrot', 'lettuce', ],
    #         'grain': ['bread', 'dough', 'wheat'],
    #         'other': ['water', 'yeast', ],
    #
    #         'beverage': ['water', 'orange juice', ],
    #         'dish': ['eggs and bacon', 'salad', ],
    #         'meal': ['classic breakfast', ],
    #         'snack': [],
    #         'dessert': [],
    #         }

