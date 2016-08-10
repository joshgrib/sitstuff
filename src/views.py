################################################
#                     VIEWS                    #
#     Used for displaying things to users      #
#       Uses models to get stuff to show       #
################################################
from flask import Flask, render_template, request, make_response, redirect, session, jsonify
from src import app


#######################
#    Static pages     #
#     and errors      #
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
from models import dbtools
@app.route('/courses')
def courses():
    db = dbtools.CourseDB('src/models/course_info.db', 'courses')
    courses = db.get_HTML()
    depts = db.get_depts()
    db.close_db()
    resp = render_template('courses.html',
                            title='Courses',
                            courses=courses,
                            letter_links=depts)
    return resp


#######################
#     Scheduling      #
#######################
from models import scheduler
import json
PER_PAGE = 10
AMOUNT_OF_COURSES = 10

@app.route('/sched_entry')
def how_many_post():
    """
    Goes to form with AMOUNT_OF_COURSES text boxes to input
    courses to schedule, form action=/schedules, method=POST
    """
    default_courses = ['CS 442', 'CS 392', 'CS 519', 'MA 331']
    resp = make_response(render_template(
        "sched_entry.html",
        quantity=AMOUNT_OF_COURSES,
        title='Scheduler',
        default_vals=default_courses))
    resp.set_cookie('course_combos', '', expires=0)
    return resp

@app.route('/schedules', methods=['GET','POST'])
def my_form_post():
    """
    Gets input from form, puts it in a list, gets the schedules,
    send JSON of course combinations and send then to /sched as
    a cookie
    """
    text_list = []
    #make list of form inputs
    for i in range(1, AMOUNT_OF_COURSES + 1):
        form_num = 'text' + str(i)
        text_list.append(request.form[form_num])
    #remove items with no input, generate string of courses
    final_list = []
    for text in text_list:
        if not text == "":
            final_list.append(text)
    courses_str = ""
    for course in final_list[:-1]:
        courses_str += (str(course) + ',')
    courses_str += str(final_list[-1])
    courses_str = courses_str.upper()
    #turn string of courses entered into list
    c_list = courses_str.split(',')
    #get the schedules
    #print "\nCourse list:"
    #print str(c_list) + "\n"
    my_combos = scheduler.schedule(c_list)
    resp = make_response(redirect('/sched'))
    resp.set_cookie('course_combos', '', expires=0)
    resp.set_cookie('course_combos', json.dumps(my_combos))
    return resp

@app.route('/get_combos', methods=['GET'])
def getCombosAPI():
    """
    Upon a GET request containing csv course names in a query string...
    Find the combos and send them as JSON
    """
    all_args = request.args.lists()
    course_list = all_args[0][1][0].split(",")
    u_COURSE_LIST = map((lambda x: x.upper()), course_list)#make all caps just in case
    COURSE_LIST = map( str, u_COURSE_LIST)#unicode list -> list of python strs
    combos = scheduler.schedule(COURSE_LIST)
    return jsonify(combos)

def getCombosForPage(page_num, per_page, count_of_combos, combos):
    """Returns the set of combos for the current page"""
    combos_start = (per_page * (page_num - 1)) + 1
    combos_end = combos_start + per_page
    these_combos = {}
    for key in range(combos_start, combos_end):
        try:
            # if new dict is not an int schedules are not sorted on the page
            these_combos[key] = combos[str(key)]
        except KeyError:
            pass
    return these_combos

def isLastPage(page_num, count_of_combos, per_page):
    """Return True if this is the last page in the pagination"""
    if count_of_combos <= (page_num * per_page):
        return True
    return False

@app.route('/sched/', defaults={'page': 1})
@app.route('/sched/page/<int:page>')
def scheduleMe(page):
    """
    Display schedules as links and iframes
    """
    querystring_combos = request.cookies.get('course_combos')
    if not querystring_combos:
       return render_template('404.html'), 404
    combos = json.loads(querystring_combos)
    #print querystring_combos

    count = len(combos)
    pagination_needed = count > PER_PAGE
    this_page_combos = combos
    if pagination_needed:
        this_page_combos = getCombosForPage(page, PER_PAGE, count, combos)
    last_page = isLastPage(page, count, PER_PAGE)
    if not this_page_combos and page != 1:
        return render_template('404.html'), 404
    return render_template("sched.html",
                           title="Scheduler",
                           combos=this_page_combos,
                           combo_amount=str(count),
                           page=page,
                           last_page=last_page,
                           pagination=pagination_needed)


########################
#     Random stuff     #
########################
