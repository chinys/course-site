import sqlite3
import os
import shutil

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

db_path = os.path.join(project_root, 'database.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 1. Update the thumbnail_url in the DB
cursor.execute("SELECT id, thumbnail_url FROM course WHERE title LIKE '%FastAPI%'")
row = cursor.fetchone()
if row:
    course_id = row[0]
    old_url = row[1]
    
    if old_url and 'images' in old_url:
        new_url = old_url.replace('/static/images/', '/static/uploads/')
        cursor.execute("UPDATE course SET thumbnail_url = ? WHERE id = ?", (new_url, course_id))
        conn.commit()
        print(f"Updated DB thumbnail URL from {old_url} to {new_url}")

# 2. Move files from images/ to uploads/
images_dir = os.path.join(project_root, 'static', 'images')
uploads_dir = os.path.join(project_root, 'static', 'uploads')

if os.path.exists(images_dir):
    for filename in os.listdir(images_dir):
        if filename.endswith('.png') or filename.endswith('.jpg'):
            src = os.path.join(images_dir, filename)
            dst = os.path.join(uploads_dir, filename)
            shutil.move(src, dst)
            print(f"Moved {filename} to uploads directory.")
            
conn.close()
