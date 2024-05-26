import sqlite3

DATABASE = 'bot_database.db'

def init_db():
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()

        # Создаем таблицы
        cursor.executescript('''
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            weight REAL,
            height REAL,
            age INTEGER,
            physical_activity_level TEXT
        );

        CREATE TABLE IF NOT EXISTS meals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            calories INTEGER
        );

        CREATE TABLE IF NOT EXISTS ingredients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT
        );

        CREATE TABLE IF NOT EXISTS meal_link (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meal_id INTEGER NOT NULL,
            url TEXT NOT NULL,
            FOREIGN KEY(meal_id) REFERENCES meals(id)
        );

        CREATE TABLE IF NOT EXISTS healthy_foods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS nutrition_tips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tip TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS activity_tips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tip TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS meal_breakfast (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meal_id INTEGER NOT NULL,
            FOREIGN KEY(meal_id) REFERENCES meals(id)
        );

        CREATE TABLE IF NOT EXISTS meal_lunch (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meal_id INTEGER NOT NULL,
            FOREIGN KEY(meal_id) REFERENCES meals(id)
        );

        CREATE TABLE IF NOT EXISTS meal_dinner (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meal_id INTEGER NOT NULL,
            FOREIGN KEY(meal_id) REFERENCES meals(id)
        );

        CREATE TABLE IF NOT EXISTS meal_snacks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meal_id INTEGER NOT NULL,
            FOREIGN KEY(meal_id) REFERENCES meals(id)
        );

        CREATE TABLE IF NOT EXISTS user_meal_plan (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            breakfast_id INTEGER,
            lunch_id INTEGER,
            dinner_id INTEGER,
            snack_id INTEGER,
            FOREIGN KEY(user_id) REFERENCES user(id),
            FOREIGN KEY(breakfast_id) REFERENCES meal_breakfast(id),
            FOREIGN KEY(lunch_id) REFERENCES meal_lunch(id),
            FOREIGN KEY(dinner_id) REFERENCES meal_dinner(id),
            FOREIGN KEY(snack_id) REFERENCES meal_snacks(id)
        );

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

# Вызов функции инициализации базы данных
if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
