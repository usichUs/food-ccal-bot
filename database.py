import sqlite3

DATABASE = 'bot_database.db'

def init_db():
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.executescript('''
        -- Создаем таблицу пользователя
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            weight REAL,
            height REAL,
            age INTEGER,
            gender TEXT,
            physical_activity_level TEXT
        );

        -- Создаем таблицу блюд
        CREATE TABLE IF NOT EXISTS meals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            calories REAL
        );

        -- Создаем таблицу ингредиентов
        CREATE TABLE IF NOT EXISTS ingredients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT
        );

        -- Создаем таблицу ссылок на приготовление блюд
        CREATE TABLE IF NOT EXISTS meal_links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meal_id INTEGER NOT NULL,
            url TEXT NOT NULL,
            FOREIGN KEY(meal_id) REFERENCES meals(id)
        );

        -- Создаем таблицу полезных продуктов и блюд
        CREATE TABLE IF NOT EXISTS healthy_foods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL
        );

        -- Создаем таблицу советов по питанию
        CREATE TABLE IF NOT EXISTS nutrition_tips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tip TEXT NOT NULL
        );

        -- Создаем таблицу советов по активности
        CREATE TABLE IF NOT EXISTS activity_tips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tip TEXT NOT NULL
        );

        -- Создаем таблицу планов питания пользователя
        CREATE TABLE IF NOT EXISTS user_meal_plan (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date DATE NOT NULL,
            breakfast_id INTEGER,
            lunch_id INTEGER,
            dinner_id INTEGER,
            snack_id INTEGER,
            FOREIGN KEY(user_id) REFERENCES user(id),
            FOREIGN KEY(breakfast_id) REFERENCES meals(id),
            FOREIGN KEY(lunch_id) REFERENCES meals(id),
            FOREIGN KEY(dinner_id) REFERENCES meals(id),
            FOREIGN KEY(snack_id) REFERENCES meals(id),
            UNIQUE(user_id, date)
        );

        -- Создаем промежуточную таблицу для связи блюд и ингредиентов
        CREATE TABLE IF NOT EXISTS meal_ingredients (
            meal_id INTEGER NOT NULL,
            ingredient_id INTEGER NOT NULL,
            quantity TEXT,
            PRIMARY KEY (meal_id, ingredient_id),
            FOREIGN KEY(meal_id) REFERENCES meals(id),
            FOREIGN KEY(ingredient_id) REFERENCES ingredients(id)
        );
        ''')
        connection.commit()

def clear_db():
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.executescript('''
        DROP TABLE IF EXISTS user;
        DROP TABLE IF EXISTS meals;
        DROP TABLE IF EXISTS ingredients;
        DROP TABLE IF EXISTS meal_links;
        DROP TABLE IF EXISTS healthy_foods;
        DROP TABLE IF EXISTS nutrition_tips;
        DROP TABLE IF EXISTS activity_tips;
        DROP TABLE IF EXISTS user_meal_plan;
        DROP TABLE IF EXISTS meal_ingredients;
        ''')
        connection.commit()

def reset_db():
    clear_db()
    init_db()

if __name__ == "__main__":
    reset_db()
    print("Database reset successfully.")
