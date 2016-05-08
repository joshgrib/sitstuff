import sqlite3

conn = sqlite3.connect('test2.db')

c = conn.cursor()

#c.execute('CREATE TABLE users (first text, last text, age real)')
courses = c.execute('SELECT * FROM users')

for course in courses:
    print course
    print

conn.close()
