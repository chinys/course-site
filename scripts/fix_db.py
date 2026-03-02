import sqlite3
import os
import sys

# Add project root to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from scripts.seed_law_ultimate_pt3 import seed_law_course_ultimate_pt3
import inspect

db_path = os.path.join(project_root, 'database.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Manually grab the lessons array from the file by reading it
# Actually, since seed_law_course_ultimate_pt3 doesn't return the lessons, let's just parse the file or rebuild it.
# Wait, let's just use Python to read seed_law_ultimate_pt3.py and extract the string.
# Or better yet, we can just delete the old rows and re-seed!

cursor.execute("SELECT id FROM course WHERE title LIKE '%건설법규%'")
course_id = cursor.fetchone()[0]

# Delete lessons 11, 12, 13
cursor.execute("DELETE FROM lesson WHERE course_id = ? AND title LIKE '11.%'", (course_id,))
cursor.execute("DELETE FROM lesson WHERE course_id = ? AND title LIKE '12.%'", (course_id,))
cursor.execute("DELETE FROM lesson WHERE course_id = ? AND title LIKE '13.%'", (course_id,))
conn.commit()

seed_law_course_ultimate_pt3()

print("Re-seeded pt3 lessons.")
