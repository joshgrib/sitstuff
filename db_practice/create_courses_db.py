import sqlite3
import dbtools

conn, c = dbtools.open_db('course_info.db')

dbtools.print_courses(c)

dbtools.close_db(conn)
