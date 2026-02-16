import sqlite3

DB_NAME = "expense.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            description TEXT
        )
    """)

    conn.commit()
    conn.close()


def fetch_expenses():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM expenses ORDER BY date DESC")
    expenses = cursor.fetchall()

    conn.close()
    return expenses


def add_expense(date, category, amount, description):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO expenses (date, category, amount, description)
        VALUES (?, ?, ?, ?)
    """, (date, category, amount, description))

    conn.commit()
    conn.close()


def delete_expense(expense_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))

    conn.commit()
    conn.close()

def get_total_balance():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(amount) FROM expenses")
    result = cursor.fetchone()[0]

    conn.close()
    return result if result else 0


def get_monthly_summary():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT substr(date, 1, 7) as month,
               SUM(amount)
        FROM expenses
        GROUP BY month
        ORDER BY month DESC
    """)

    data = cursor.fetchall()
    conn.close()
    return data


def get_category_distribution():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        GROUP BY category
    """)

    data = cursor.fetchall()
    conn.close()
    return data
