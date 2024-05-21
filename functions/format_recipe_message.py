def format_recipe_message(recipe):
    message = f"<b>{recipe['name']}</b>\n"
    message += f"Ингредиенты: {', '.join(recipe['ingredients'])}\n"
    message += f"Калории: {recipe['calories']} ккал\n"
    message += f"Ссылка на рецепт: <a href='{recipe['receipt_link']}'>Ссылка</a>\n"
    return message
