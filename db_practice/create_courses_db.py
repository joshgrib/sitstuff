import sqlite3
import dbtools

conn, c = dbtools.get_cursor()

#c.execute("""
#    UPDATE courses
#    SET lecture='',
#        recitation='',
#        homework='',
#        exams='',
#        final=''
#    WHERE dept='' AND number=''
#    """)

#conn.commit()

dbtools.print_courses(c)

dbtools.close_db(conn)
