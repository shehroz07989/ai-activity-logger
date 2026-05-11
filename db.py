import sqlite3

conn = sqlite3.connect("system.db")


cursor = conn.cursor()

cursor.execute(
"""
                CREATE TABLE IF NOT EXISTS trace (
                        trace_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        request_id TEXT,
                        step_name TEXT,
                        step_order INTEGER,
                        status TEXT,
                        error TEXT,
                        created_at TIMESTAMP  DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (request_id)
                        REFERENCES logs(unique_id)
                                )             
                        """)
print("ho gya ")
