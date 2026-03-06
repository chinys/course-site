import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'database.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# FastAPI course 확인 (course_id = 6)
print("=== FastAPI Course Lessons ===")
cursor.execute("SELECT id, title, \"order\", course_id FROM lesson WHERE course_id = 6 ORDER BY \"order\"")
rows = cursor.fetchall()
for row in rows:
    print(row)

print(f"\n총 {len(rows)}개 레슨")

conn.close()
