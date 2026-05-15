import sqlite3

conn = sqlite3.connect("system.db")


cursor = conn.cursor()

cursor.execute(
            "ALTER TABLE logs ADD COLUMN ai_explanation TEXT")
print("ho gya ")
