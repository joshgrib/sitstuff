from models import course_class

if __name__ == '__main__':
    (courses, sorted_courses, course_letters) = course_class.get_courses_page()
    print courses
