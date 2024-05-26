import sqlite3

DATABASE = 'bot_database.db'

def populate_db():
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()

        # Добавляем данные в таблицу meals
        meals_data = [
            ('Овсянка', 'Овсянка с фруктами и орехами'),
            ('Куриная грудка', 'Запеченная куриная грудка с овощами'),
            ('Салат Цезарь', 'Салат с курицей, листьями салата, сыром и соусом Цезарь'),
            ('Смузи', 'Смузи из банана, клубники и йогурта')
        ]
        cursor.executemany('''
            INSERT INTO meals (name, description) VALUES (?, ?)
        ''', meals_data)

        # Добавляем данные в таблицу ingredients
        ingredients_data = [
            ('Овсянка', 'Зерновой продукт'),
            ('Курица', 'Мясо курицы'),
            ('Листья салата', 'Свежие листья салата'),
            ('Банан', 'Свежий банан'),
            ('Клубника', 'Свежая клубника'),
            ('Йогурт', 'Натуральный йогурт')
        ]
        cursor.executemany('''
            INSERT INTO ingredients (name, description) VALUES (?, ?)
        ''', ingredients_data)

        # Добавляем данные в таблицу meal_link
        meal_links_data = [
            (1, 'http://example.com/oatmeal'),
            (2, 'http://example.com/chicken'),
            (3, 'http://example.com/caesar_salad'),
            (4, 'http://example.com/smoothie')
        ]
        cursor.executemany('''
            INSERT INTO meal_link (meal_id, url) VALUES (?, ?)
        ''', meal_links_data)

        # Добавляем данные в таблицу healthy_foods
        healthy_foods_data = [
            ('Яблоко', 'Свежие яблоки'),
            ('Морковь', 'Свежая морковь'),
            ('Орехи', 'Ассорти из орехов'),
            ('Авокадо', 'Свежий авокадо')
        ]
        cursor.executemany('''
            INSERT INTO healthy_foods (name, description) VALUES (?, ?)
        ''', healthy_foods_data)

        # Добавляем данные в таблицу nutrition_tips
        nutrition_tips_data = [
            ('Пейте больше воды'),
            ('Ешьте больше овощей'),
            ('Избегайте сахара'),
            ('Ешьте регулярно')
        ]
        cursor.executemany('''
            INSERT INTO nutrition_tips (tip) VALUES (?)
        ''', [(tip,) for tip in nutrition_tips_data])

        # Добавляем данные в таблицу activity_tips
        activity_tips_data = [
            ('Занимайтесь спортом регулярно'),
            ('Делайте утреннюю зарядку'),
            ('Ходите пешком вместо лифта'),
            ('Плавайте')
        ]
        cursor.executemany('''
            INSERT INTO activity_tips (tip) VALUES (?)
        ''', [(tip,) for tip in activity_tips_data])

        # Добавляем данные в таблицу meal_breakfast
        meal_breakfast_data = [
            (1,), (4,)
        ]
        cursor.executemany('''
            INSERT INTO meal_breakfast (meal_id) VALUES (?)
        ''', meal_breakfast_data)

        # Добавляем данные в таблицу meal_lunch
        meal_lunch_data = [
            (2,), (3,)
        ]
        cursor.executemany('''
            INSERT INTO meal_lunch (meal_id) VALUES (?)
        ''', meal_lunch_data)

        # Добавляем данные в таблицу meal_dinner
        meal_dinner_data = [
            (2,), (3,)
        ]
        cursor.executemany('''
            INSERT INTO meal_dinner (meal_id) VALUES (?)
        ''', meal_dinner_data)

        # Добавляем данные в таблицу meal_snacks
        meal_snacks_data = [
            (4,)
        ]
        cursor.executemany('''
            INSERT INTO meal_snacks (meal_id) VALUES (?)
        ''', meal_snacks_data)

        # Привязка ингредиентов к блюдам
        meal_ingredients_data = [
            (1, 1, '100 г'),
            (2, 2, '200 г'),
            (3, 3, '50 г'),
            (4, 4, '1 шт.'),
            (4, 5, '50 г'),
            (4, 6, '100 мл')
        ]
        cursor.executemany('''
            INSERT INTO meal_ingredients (meal_id, ingredient_id, quantity) VALUES (?, ?, ?)
        ''', meal_ingredients_data)

        connection.commit()

if __name__ == "__main__":
    populate_db()
