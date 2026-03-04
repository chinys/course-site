import sqlite3
import os

db_path = os.path.join(r'd:\workai\course-site\course-site', 'database.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT content FROM lesson WHERE course_id = (SELECT id FROM course WHERE title LIKE '%건설법규%') AND title LIKE '%계약서 모음%'")
row = cursor.fetchone()

if row:
    content = row[0]
    if "물품매매" in content:
        print("Success: '물품매매' found in DB.")
    else:
        print("Fail: '물품매매' NOT found in DB.")
else:
    print("Lesson not found.")

conn.close()
