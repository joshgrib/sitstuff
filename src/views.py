################################################
#                     VIEWS                    #
#     Used for displaying things to users      #
#       Uses models to get stuff to show       #
################################################
from flask import Flask, render_template, request, make_response, redirect, session
from src import app
import dbtools


#######################
#    Static pages     #
#######################
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

@app.errorhandler(500)
def internal_error(error):
    return render_template('505.html'), 505

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(403)
def forbidden_error(error):
    return render_template('403.html'), 403

#######################
#     Course info     #
#######################
#import course_class

@app.route('/courses')
def courses():
    db = dbtools.CourseDB('course_info.db', 'courses')
    courses = db.get_HTML()
    depts = db.get_depts()
    db.close_db()
    resp = render_template('courses.html',
                            title='Courses',
                            courses=courses,
                            letter_links=depts)
    return resp
