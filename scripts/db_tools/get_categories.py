import sqlite3

db = sqlite3.connect('database.db')
cursor = db.cursor()

cursor.execute('SELECT id, name FROM category')
categories = cursor.fetchall()
print("Categories:", categories)

cursor.execute('SELECT id, title FROM course LIMIT 5')
courses = cursor.fetchall()
print("Courses:", courses)

db.close()
