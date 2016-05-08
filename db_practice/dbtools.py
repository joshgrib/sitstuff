#############################################
#   A module for accessing a database to:   #
#   -Add courses                            #
#   -Edit course info                       #
#   -Other cool stuff I don't need yet      #
#############################################
import sqlite3

def get_cursor():
    DATABASE = 'course_info.db'
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    return conn, c

def print_courses(cursor):
    courses = cursor.execute("""
        SELECT * FROM courses
        ORDER BY dept ASC, number ASC
        """)
    for course in courses:
        print course
        print

def close_db(connection):
    connection.close()

def update_lecture(cursor, connection, dept, number, lecture_info):
    query = "UPDATE courses "
    query += "SET lecture='{}' ".format(lecture_info)
    query += "WHERE dept='{}' AND number='{}'".format(dept, number)
    cursor.execute(query)
    connection.commit()
