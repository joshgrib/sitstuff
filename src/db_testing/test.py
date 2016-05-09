from models2 import dbtools

if __name__ == '__main__':
    """Below: feature testing"""
    db = dbtools.CourseDB('course_info2.db', 'courses')
    courses = db.get_HTML()
    print courses
    depts = db.get_depts()
    print depts
    db.close_db()
