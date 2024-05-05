def get_recipes_by_products(recipes, user_products):
    suitable_dishes = []
    for recipe in recipes:
        if all(ingredient in user_products for ingredient in recipe["ingredients"]):
            suitable_dishes.append(recipe)
    return suitable_dishes