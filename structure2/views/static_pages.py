from flask import Flask, render_template, request, make_response, redirect, session
from courses.course_class import file_name, load_data

if __name__ == '__main__':
    app = Flask(__name__)
    course_info = load_data()
    print course_info
else:
    from sitstuff import app

@app.route('/')
@app.route('/index')
def index():
    """
    Returns the home page
    """
    resp = make_response(render_template("index.html", title='Home'))
    return resp

@app.route('/donate')
def donate():
    return render_template("donate.html", title='Donate')

@app.route('/courses')
def courses():
    courses = load_data()
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

@app.errorhandler(500)
def internal_error(error):
    return render_template('505.html'), 505

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(403)
def forbidden_error(error):
    return render_template('403.html'), 403