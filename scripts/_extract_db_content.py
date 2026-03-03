# -*- coding: utf-8 -*-
"""DB에서 lesson 55 콘텐츠를 추출하여 파일로 저장"""
import os, sqlite3

db_path = os.path.join(os.path.dirname(__file__), '..', 'database.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT id, title, content FROM lesson WHERE id = 55")
row = cursor.fetchone()

if row:
    lid, ltitle, content = row
    print(f"Lesson ID={lid}: {ltitle}")
    print(f"Content length: {len(content)} chars")
    out_path = os.path.join(os.path.dirname(__file__), '_db_lesson_55.txt')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Saved to: {out_path}")
else:
    print("Lesson 55 not found!")

conn.close()
