import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), '..', 'database.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT id, title FROM course")
print("COURSES:", cursor.fetchall())

cursor.execute("SELECT id, title, \"order\", course_id FROM lesson WHERE title LIKE '%건설법규%' OR course_id = 5")
print("LESSONS in course 5:", cursor.fetchall())

conn.close()
