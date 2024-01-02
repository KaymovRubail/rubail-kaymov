import sqlite3

def create_database():
    conn = sqlite3.connect('school_database.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS countries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL
        )
    ''')

    cursor.executemany('INSERT INTO countries (title) VALUES (?)', [
        ('Kyrgyzstan',),
        ('Germany',),
        ('China',),
    ])

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            area REAL DEFAULT 0,
            country_id INTEGER,
            FOREIGN KEY (country_id) REFERENCES countries (id)
        )
    ''')

    cursor.executemany('INSERT INTO cities (title, area, country_id) VALUES (?, ?, ?)', [
        ('Bishkek', 123.45, 1),
        ('Berlin', 456.78, 2),
        ('Beijing', 789.01, 3),
        ('Osh', 234.56, 1),
        ('Munich', 567.89, 2),
        ('Shanghai', 901.23, 3),
        ('Frankfurt', 345.67, 2),
    ])

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            city_id INTEGER,
            FOREIGN KEY (city_id) REFERENCES cities (id)
        )
    ''')

    cursor.executemany('INSERT INTO students (first_name, last_name, city_id) VALUES (?, ?, ?)', [
        ('John', 'Doe', 1),
        ('Jane', 'Smith', 2),
        ('Alice', 'Johnson', 3),
        ('Bob', 'Williams', 1),
        ('Eva', 'Davis', 2),
        ('Michael', 'Brown', 3),
        ('Sophia', 'Jones', 1),
        ('Daniel', 'Miller', 2),
        ('Olivia', 'Wilson', 3),
        ('Matthew', 'Moore', 1),
        ('Emily', 'Anderson', 2),
        ('David', 'Taylor', 3),
        ('Emma', 'White', 1),
        ('Andrew', 'Martin', 2),
        ('Isabella', 'Lee', 3),
    ])

    conn.commit()
    conn.close()

def display_cities_and_students():
    conn = sqlite3.connect('school_database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT id, title FROM cities')
    cities = cursor.fetchall()

    print("Список городов:")
    for city in cities:
        print(f"{city[0]}. {city[1]}")

    selected_city_id = int(input("\nВведите id города (для выхода введите 0): "))

    if selected_city_id == 0:
        conn.close()
        print("Программа завершена.")
        return

    cursor.execute('''
        SELECT students.first_name, students.last_name, countries.title, cities.title, cities.area
        FROM students
        JOIN cities ON students.city_id = cities.id
        JOIN countries ON cities.country_id = countries.id
        WHERE cities.id = ?
    ''', (selected_city_id,))

    print("\nИнформация о учениках в выбранном городе:")
    for row in cursor.fetchall():
        print(f"Имя: {row[0]}, Фамилия: {row[1]}, Страна: {row[2]}, Город: {row[3]}, Площадь города: {row[4]}")

    conn.close()

create_database()
display_cities_and_students()
