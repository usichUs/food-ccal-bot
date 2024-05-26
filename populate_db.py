import sqlite3

DATABASE = 'bot_database.db'

def populate_db():
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()

        # Добавляем данные в таблицу meals
        meals_data = [
            ('Овсянка', 'Овсянка с фруктами и орехами', 350),
            ('Куриная грудка', 'Запеченная куриная грудка с овощами', 400),
            ('Салат Цезарь', 'Салат с курицей, листьями салата, сыром и соусом Цезарь', 300),
            ('Смузи', 'Смузи из банана, клубники и йогурта', 250),
            ('Яичница', 'Яичница с помидорами и зеленью', 200),
            ('Сэндвич с индейкой', 'Сэндвич с индейкой, сыром и овощами', 450),
            ('Томатный суп', 'Томатный суп с базиликом', 150),
            ('Греческий салат', 'Салат с огурцами, помидорами, оливками и сыром фета', 200),
            ('Фрукты', 'Свежие фрукты', 100)
        ]
        cursor.executemany('''
            INSERT INTO meals (name, description, calories) VALUES (?, ?, ?)
        ''', meals_data)

        # Добавляем данные в таблицу ingredients
        ingredients_data = [
            ('Овсянка', 'Зерновой продукт'),
            ('Курица', 'Мясо курицы'),
            ('Листья салата', 'Свежие листья салата'),
            ('Банан', 'Свежий банан'),
            ('Клубника', 'Свежая клубника'),
            ('Йогурт', 'Натуральный йогурт'),
            ('Помидоры', 'Свежие помидоры'),
            ('Индейка', 'Мясо индейки'),
            ('Огурцы', 'Свежие огурцы'),
            ('Оливки', 'Маринованные оливки'),
            ('Сыр фета', 'Греческий сыр фета')
        ]
        cursor.executemany('''
            INSERT INTO ingredients (name, description) VALUES (?, ?)
        ''', ingredients_data)

        # Добавляем данные в таблицу meal_links
        meal_links_data = [
            (1, 'http://example.com/oatmeal'),
            (2, 'http://example.com/chicken'),
            (3, 'http://example.com/caesar_salad'),
            (4, 'http://example.com/smoothie'),
            (5, 'http://example.com/omelette'),
            (6, 'http://example.com/turkey_sandwich'),
            (7, 'http://example.com/tomato_soup'),
            (8, 'http://example.com/greek_salad'),
            (9, 'http://example.com/fruits')
        ]
        cursor.executemany('''
            INSERT INTO meal_links (meal_id, url) VALUES (?, ?)
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

        connection.commit()

if __name__ == "__main__":
    populate_db()
