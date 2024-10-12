import sqlite3
import os

# Path to the database
DATABASE = "database/users.db"

def init_db():

    # Ensure the directory for the database exists
    database_dir = os.path.dirname(DATABASE)
    if not os.path.exists(database_dir):
        os.makedirs(database_dir)
        print(f"Created directory: {database_dir}")

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Create a table for users (if it doesn't already exist)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        text_field TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

# Call this function at startup to initialize the database
init_db()

def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn
