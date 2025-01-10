import random
import sqlite3

connection = sqlite3.connect('Bot_database.db')
cursor = connection.cursor()


def initiate_db():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INT NOT NULL
    );
    ''')

    cursor.execute("SELECT COUNT(*) FROM Products")
    count = cursor.fetchone()[0]

    if count == 0:
        for i in range(1, 5):
            cursor.execute(f'INSERT INTO Products (title, description, price) VALUES (?, ?, ?)',
                           (f'Полезная добавка {i}', f'Витамины {i}', f'{i*100}'))
        connection.commit()


def get_all_products():
    cursor.execute("SELECT * FROM Products")
    all_prod = cursor.fetchall()
    connection.close()
    return all_prod


initiate_db()

