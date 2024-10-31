import psycopg2
from psycopg2 import sql

def create_database():
    """Create the library_db database if it doesn't exist."""
    try:
        # Connect to the default database (usually 'postgres' or similar)
        conn = psycopg2.connect(dbname="postgres", user="admin", password="123456", host="db")
        conn.autocommit = True  # Set autocommit to true to create database
        cur = conn.cursor()
        
        # Create the database if it doesn't exist
        cur.execute(sql.SQL("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s"), ['library_db'])
        if not cur.fetchone():
            cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier('library_db')))
            print("Database 'library_db' created successfully.")
        else:
            print("Database 'library_db' already exists.")

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error creating database: {error}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def create_tables():
    commands = [
        """
        CREATE TABLE IF NOT EXISTS Books (
            book_id SERIAL PRIMARY KEY,
            author VARCHAR(255) NOT NULL,
            title VARCHAR(255) NOT NULL,
            section VARCHAR(50) CHECK (section IN ('технічна', 'художня', 'економічна')),
            year INT CHECK (year > 0),
            pages INT CHECK (pages > 0),
            price DECIMAL(10, 2) CHECK (price > 0),
            type VARCHAR(50) CHECK (type IN ('посібник', 'книга', 'періодичне видання')),
            copies INT CHECK (copies >= 1),
            max_loan_days INT DEFAULT 14 CHECK (max_loan_days >= 1)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Readers (
            reader_id SERIAL PRIMARY KEY,
            last_name VARCHAR(50) NOT NULL,
            first_name VARCHAR(50) NOT NULL,
            phone VARCHAR(15) CHECK (phone ~ '^380\\d{9}$'),
            address VARCHAR(255),
            course INT CHECK (course BETWEEN 1 AND 4),
            group_name VARCHAR(50)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS BookLoans (
            loan_id SERIAL PRIMARY KEY,
            loan_date DATE NOT NULL,
            reader_id INT REFERENCES Readers(reader_id) ON DELETE CASCADE,
            book_id INT REFERENCES Books(book_id) ON DELETE CASCADE
        )
        """
    ]
    try:
        conn = psycopg2.connect(dbname="library_db", user="admin", password="123456", host="db")
        cur = conn.cursor()
        for command in commands:
            cur.execute(command)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

def insert_initial_data():
    books = [
        ('Джордж Орвелл', '1984', 'художня', 1949, 328, 55.00, 'книга', 10, 30),
        ('Френсіс Фукуяма', 'Кінець історії та остання людина', 'економічна', 1992, 418, 89.50, 'книга', 5, 21),
        ('Джеймс Клір', 'Атомні звички', 'економічна', 2018, 320, 70.99, 'посібник', 3, 14),
        ('Рей Бредбері', '451 градус за Фаренгейтом', 'художня', 1953, 256, 45.99, 'книга', 8, 30),
        ('Стівен Хокінг', 'Коротка історія часу', 'технічна', 1988, 212, 78.00, 'книга', 4, 15),
        ('Юваль Ной Харарі', 'Sapiens', 'технічна', 2014, 512, 120.00, 'посібник', 6, 25),
        ('Дейл Карнегі', 'Як здобувати друзів і впливати на людей', 'технічна', 1936, 288, 65.50, 'посібник', 12, 20),
        ('Айн Ренд', 'Атлант розправив плечі', 'художня', 1957, 1168, 100.00, 'книга', 2, 60),
        ('Адам Сміт', 'Багатство народів', 'економічна', 1776, 1040, 150.00, 'періодичне видання', 1, 45),
        ('Карл Маркс', 'Капітал', 'економічна', 1867, 800, 90.00, 'періодичне видання', 5, 30),
        ('Габріель Гарсіа Маркес', 'Сто років самотності', 'художня', 1967, 432, 85.00, 'книга', 9, 30),
        ('Вільям Шекспір', 'Гамлет', 'художня', 1603, 160, 25.00, 'періодичне видання', 6, 15),
        ('Альберт Камю', 'Чума', 'художня', 1947, 224, 50.00, 'книга', 4, 20),
    ]
    
    readers = [
        ('Іванов', 'Іван', '380631234567', 'Київ', 1, 'Група1'),
        ('Петренко', 'Олена', '380661234567', 'Львів', 3, 'Група2'),
        ('Сидоров', 'Петро', '380671234567', 'Одеса', 4, 'Група3'),
        ('Шевченко', 'Марія', '380681234567', 'Харків', 2, 'Група4'),
        ('Коваленко', 'Сергій', '380691234567', 'Дніпро', 3, 'Група5'),
        ('Гончаренко', 'Анастасія', '380631237890', 'Луцьк', 1, 'Група6'),
        ('Дяченко', 'Богдан', '380661237890', 'Чернігів', 4, 'Група7'),
        ('Мельник', 'Юлія', '380671237890', 'Полтава', 2, 'Група8'),
        ('Лисенко', 'Тарас', '380681237890', 'Запоріжжя', 1, 'Група9'),
    ]
    
    loans = [
        ('2023-01-15', 1, 1),
        ('2023-02-20', 2, 2),
        ('2023-03-10', 3, 3),
        ('2023-04-05', 4, 4),
        ('2023-05-01', 5, 5),
        ('2023-06-11', 6, 6),
        ('2023-07-20', 7, 7),
        ('2023-08-15', 8, 8),
        ('2023-09-01', 9, 9),
        ('2023-10-07', 1, 10),
        ('2023-11-12', 2, 11),
        ('2023-12-05', 3, 12),
        ('2024-01-10', 4, 13),
    ]

    try:
        conn = psycopg2.connect(dbname="library_db", user="admin", password="123456", host="db")
        cur = conn.cursor()

        # Check if the tables are empty before inserting data
        cur.execute("SELECT COUNT(*) FROM Books;")
        if cur.fetchone()[0] == 0:
            cur.executemany(
                "INSERT INTO Books (author, title, section, year, pages, price, type, copies, max_loan_days) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                books
            )
            print("Initial book data inserted.")
        else:
            print("Books table already contains data; skipping insertion.")

        cur.execute("SELECT COUNT(*) FROM Readers;")
        if cur.fetchone()[0] == 0:
            cur.executemany(
                "INSERT INTO Readers (last_name, first_name, phone, address, course, group_name) VALUES (%s, %s, %s, %s, %s, %s)",
                readers
            )
            print("Initial reader data inserted.")
        else:
            print("Readers table already contains data; skipping insertion.")

        cur.execute("SELECT COUNT(*) FROM BookLoans;")
        if cur.fetchone()[0] == 0:
            cur.executemany(
                "INSERT INTO BookLoans (loan_date, reader_id, book_id) VALUES (%s, %s, %s)",
                loans
            )
            print("Initial loan data inserted.")
        else:
            print("BookLoans table already contains data; skipping insertion.")

        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    create_database()
    create_tables()
    insert_initial_data()
