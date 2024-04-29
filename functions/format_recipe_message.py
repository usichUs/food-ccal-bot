def get_time_by_type(recipe_type):
    if recipe_type == 'Breakfast':
        return '8:00'
    elif recipe_type == 'Lunch':
        return '12:00'
    elif recipe_type == 'Dinner':
        return '18:00'

def format_recipe_message(recipe):
    message = (
        f"<b>{get_time_by_type(recipe['type'])}</b>\n"
        f"<b>{recipe['name']}</b> <i>- {', '.join(recipe['ingredients'])}</i>\n"
        f"<b>Рецепт:</b> <i>{recipe['receipt_link']}</i>\n"
        f"<b>Калории:</b> <i>{recipe['calories']}</i>\n"
    )
    return message