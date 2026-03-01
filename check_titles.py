import sqlite3
import os

db_path = os.path.join(r"d:\workai\course-site", 'database.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT id FROM course WHERE title = '[건설법규]'")
row = cursor.fetchone()
if row:
    course_id = row[0]
    cursor.execute('SELECT id, "order", title FROM lesson WHERE course_id = ? ORDER BY "order" ASC, id ASC', (course_id,))
    lessons = cursor.fetchall()
    for l in lessons:
        print(f"ID: {l[0]}, Order: {l[1]}, Title: {l[2]}")
else:
    print("Course not found")
        
conn.close()
