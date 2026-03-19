import sqlite3

DB_path = 'instance/students.db'

def get_db_connection():
    conn = sqlite3.connect(DB_path)
    conn.row_factory = sqlite3.Row