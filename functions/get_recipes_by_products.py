import json

with open("receipts/receipts.json", "r") as file:
    dishes = json.load(file)

def find_matching_dishes(user_products):
    matching_dishes = []
    for dish in dishes:
        if all(ingredient in user_products for ingredient in dish["ingredients"]):
            matching_dishes.append(dish)
    return matching_dishes

def filter_dishes_by_preferences_and_exclusions(preferences, exclusions):
    filtered_dishes = []
    for dish in dishes:
        if all(ingredient not in exclusions for ingredient in dish["ingredients"]) and all(ingredient in dish["ingredients"] for ingredient in preferences):
            filtered_dishes.append(dish)
    return filtered_dishes
