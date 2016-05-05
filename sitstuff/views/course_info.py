from flask import Flask, render_template, request, make_response, redirect, session
from sitstuff import app
from courses import course_class

@app.route('/courses')
def courses():
    courses = course_class.load_data()

    # get sorted course list
    sorted_courses = sorted(courses, key=lambda x: x.dept + x.num)

    # get unique depts for links
    course_letters = []
    for course in sorted_courses:
        if not course.dept in course_letters:
            course_letters.append(course.dept)

    resp = make_response(render_template('courses.html',
                                             title='Courses',
                                             courses=courses,
                                             sorted_c=sorted_courses,
                                             letter_links=course_letters))
    return resp

if __name__ == '__main__':
    print "hello"
