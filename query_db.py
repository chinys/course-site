import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'database.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT id, title, \"order\", course_id FROM lesson WHERE course_id = 5")
rows = cursor.fetchall()
for row in rows:
    print(row)

conn.close()
