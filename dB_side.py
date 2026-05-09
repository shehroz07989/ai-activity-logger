import sqlite3

conn = sqlite3.connect("practice.db")
cursor = conn.cursor()
cursor.execute("""
SELECT * FROM practice LEFT JOIN child
ON practice.id = child.parent_id;               """)

data = cursor.fetchall()
print(data)