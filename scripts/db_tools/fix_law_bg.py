import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), '..', 'database.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT id, content FROM lesson WHERE title LIKE '%재하도급 제한과 불법 파견의 회피 전략%'")
row = cursor.fetchone()
if row:
    lesson_id = row[0]
    content = row[1]
    
    # We may have already replaced it in DB earlier with bg-gray-100.
    # We need to make sure the target gradient or the old bg-gray-100 are handled properly.
    # Let's just forcefully replace the entire HTML block starting with <div class...
    # Since we previously changed bg-blue-50 to bg-gray-100 in the DB, let's just use the seed script's content directly.
    pass

conn.close()
