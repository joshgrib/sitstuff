import sqlite3
"""
from flask import g

DATABASE = 'test.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
"""

conn = sqlite3.connect('test.db')

c = conn.cursor()

#c.execute('CREATE TABLE users (first text, last text, age real)')
"""
josh = ['Josh', 'Gribbon', '20']
liam = ['Liam', 'OCallaghan', '19']
binder = ['Austin', 'Binder', '19']
jon = ['Jonathan', 'Schwarz', '20']
lindsey = ['Lindsey', 'Metz', '19']
users = {}
users[0] = josh
users[1] = liam
users[2] = binder
users[3] = jon
users[4] = lindsey

for x in users:
    c.execute("INSERT INTO users VALUES ('" +\
        users[x][0] + "','" +\
        users[x][1] + "','" +\
        users[x][2] + "')")

conn.commit()
"""

users = c.execute("SELECT * from users")
for user in users:
    vals = ['First', 'Last', 'Age']
    for i in range(len(vals)):
        print vals[i] + ":" + str(user[i])
    print "\n"

conn.close()
