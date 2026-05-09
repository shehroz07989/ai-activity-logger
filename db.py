import sqlite3

conn = sqlite3.connect("system.db")

conn.row_factory = sqlite3.Row

cursor = conn.cursor()

cursor.execute("SELECT * FROM logs")

row = cursor.fetchall()
for i in row:
    print(dict(i))