def get_time_by_type(recipe_type):
    if recipe_type == 'Breakfast':
        return '8:00'
    elif recipe_type == 'Lunch':
        return '12:00'
    elif recipe_type == 'Dinner':
        return '18:00'

def format_recipe_message(recipe):
    message = (
        f"{get_time_by_type(recipe['type'])}\n"
        f"{recipe['name']} - {', '.join(recipe['ingredients'])}\n"
        f"Рецепт: {recipe['receipt_link']}\n"
        f"Калории: {recipe['calories']}\n"
    )
    return message