import sqlite3
from contextlib import contextmanager


DATABASE_PATH = "sqlite/system.db"

@contextmanager
def get_connection():
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row

        conn.execute("PRAGMA foreign_keys = ON")

        yield conn



    
    finally:
        if conn:
            conn.close()