################################################
#                  CONTROLLERS                 #
#          Used for getting use input          #
#           Uses models to get result          #
################################################
from flask import Flask, render_template, request, make_response, redirect, session
from src import app
from settings import PER_PAGE
from models import scheduler
import json

#######################
#     Scheduling      #
#######################
@app.route('/how_many')
def how_many():
    resp = make_response(
            render_template("how_many.html", title='Scheduler'))
    return resp

@app.route('/how_many', methods=['GET', 'POST'])
def how_many_post():
    """
    Asks the user how many courses they want to schedule
    """
    course_amount = request.form['course_amount']
    amount_of_courses = int(course_amount)
    # for messing with CSS - remove once fixed
    default_courses = [
        'CS 392', 'CS 496', 'CS 347', 'MA 222']
    resp = make_response(render_template(
        "schedule_entry.html", quantity=amount_of_courses, title='Scheduler', default_vals=default_courses))
    resp.set_cookie('course_amount', str(amount_of_courses), max_age=None)
    resp.set_cookie('course_errors', '', expires=0)#redundancy because it keeps saving errors
    resp.set_cookie('course_combos', '', expires=0)
    return resp

@app.route('/schedules', methods=['GET','POST'])
def my_form_post():
    text_list = []
    amount_of_courses = int(request.cookies.get('course_amount'))
    for i in range(1, amount_of_courses + 1):
        form_num = 'text' + str(i)
        text_list.append(request.form[form_num])
    final_list = []
    for text in text_list:
        if not text == "":
            final_list.append(text)
    course_list = ""
    for course in final_list[:-1]:
        course_list += (str(course) + ',')
    course_list += str(final_list[-1])
    course_list = course_list.upper()
    #my_url = '/sched'

    real_course_list = course_list.split(',')
    my_combos = scheduler.schedule(real_course_list)
    my_errors = scheduler.get_errors()
    resp = make_response(redirect('/sched'))
    resp.set_cookie('course_combos', '', expires=0)
    resp.set_cookie('course_combos', json.dumps(my_combos))
    resp.set_cookie('course_errors', '', expires=0)#redundancy because it keeps saving errors
    resp.set_cookie('course_errors', json.dumps(my_errors))
    return resp

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
    deezCombos = json.loads(request.cookies.get('course_combos'))
    deezErrors = json.loads(request.cookies.get('course_errors'))
    count = len(deezCombos)
    err_count = len(deezErrors)
    if count > PER_PAGE:
        this_page_combos = getCombosForPage(page, PER_PAGE, count, deezCombos)
    else:
        this_page_combos = deezCombos
    last_page = isLastPage(page, count, PER_PAGE)
    if not this_page_combos and page != 1:
        return '404 - Not that many schedules'
    return render_template("sched.html",
                           title="Scheduler",
                           combos=this_page_combos,
                           combo_amount=str(count),
                           err_amount=str(err_count),
                           page=page,
                           last_page=last_page,
                           errors=deezErrors)
