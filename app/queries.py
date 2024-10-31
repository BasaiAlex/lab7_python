import psycopg2

def execute_query(query, params=None):
    conn = psycopg2.connect(dbname="library_db", user="admin", password="123456", host="db")
    cur = conn.cursor()
    cur.execute(query, params)
    result = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return result

# Відобразити всі книги, видані після 2001 року
def get_books_after_2001():
    query = "SELECT title FROM Books WHERE year > 2001 ORDER BY title"
    return execute_query(query)

# Кількість книг кожного виду
def count_books_by_type():
    query = "SELECT type, COUNT(*) FROM Books GROUP BY type"
    return execute_query(query)

# Читачі, які брали посібники
def readers_borrowed_manuals():
    query = """
        SELECT r.last_name, r.first_name 
        FROM Readers r 
        JOIN BookLoans bl ON r.reader_id = bl.reader_id
        JOIN Books b ON bl.book_id = b.book_id
        WHERE b.type = 'посібник'
        ORDER BY r.last_name
    """
    return execute_query(query)

# Книги за вказаним розділом
def get_books_by_section(section):
    query = "SELECT title FROM Books WHERE section = %s"
    return execute_query(query, (section,))

# Кінцевий термін повернення
def calculate_return_deadline():
    query = """
        SELECT b.title, bl.loan_date + b.max_loan_days AS return_date
        FROM Books b
        JOIN BookLoans bl ON b.book_id = bl.book_id
    """
    return execute_query(query)

# Перехресний запит для кількості видань по розділам
def count_publications_by_section():
    query = """
        SELECT section, type, COUNT(*) 
        FROM Books 
        GROUP BY section, type
    """
    return execute_query(query)
