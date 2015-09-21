#!/usr/bin/env python

# Standard libraries
import json
import os
import random
import smtplib
import random
import hashlib
# downloaded
from flask import Flask, render_template, request, make_response, redirect, session
# from flask.ext.sqlalchemy import SQLAlchemy #http://flask-sqlalchemy.pocoo.org/2.0/quickstart/
# files
from settings import DEBUG, PER_PAGE
import scheduler
import secrets
import course_class


app = Flask(__name__)

app.secret_key = secrets.app_secret()


@app.route('/')
@app.route('/index')
def index():
    visited = request.cookies.get('visited')
    if visited == 'True':
        resp = make_response(
            render_template("index.html", title='Home', visted='True'))
    else:
        resp = make_response(
            render_template("index.html", title='Home', visited='False'))
        resp.set_cookie('visited', 'True', max_age=2592000, path='/')
    return resp


@app.route('/donate')
def donate():
    return render_template("donate.html", title='Donate')


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

    visited = request.cookies.get('visited')
    if visited == 'True':
        resp = make_response(render_template('courses.html',
                                             title='Courses',
                                             courses=courses,
                                             sorted_c=sorted_courses,
                                             letter_links=course_letters,
                                             visited='True'))
    else:
        resp = make_response(render_template('courses.html',
                                             title='Courses',
                                             courses=courses,
                                             sorted_c=sorted_courses,
                                             letter_links=course_letters,
                                             visited='False'))
        resp.set_cookie('visited', 'True', max_age=2592000, path='/')
    return resp


@app.route('/how_many')
def how_many():
    visited = request.cookies.get('visited')
    if visited == 'True':
        resp = make_response(
            render_template("how_many.html", title='Scheduler', visited='True'))
    else:
        resp = make_response(
            render_template("how_many.html", title='Scheduler', visited='False'))
        resp.set_cookie('visited', 'True', max_age=2592000, path='/')
    return resp


@app.route('/how_many', methods=['GET', 'POST'])
def how_many_post():
    course_amount = request.form['course_amount']
    amount_of_courses = int(course_amount)
    # for messing with CSS - remove once fixed
    default_courses = [
        'BT 353', 'CS 135', 'HHS 468', 'BT 181', 'CS 146', 'CS 284']
    resp = make_response(render_template(
        "schedule_entry.html", quantity=amount_of_courses, title='Scheduler', default_vals=default_courses))
    resp.set_cookie('course_amount', str(amount_of_courses), max_age=None)
    return resp


@app.route('/schedules', methods=['GET', 'POST'])
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
    resp = make_response(redirect('/sched'))
    resp.set_cookie('course_combos', json.dumps(my_combos))
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
    count = len(deezCombos)
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
                           page=page,
                           last_page=last_page)


def sendMsg():
    '''Takes in the name to identify the phone number address, and a message, and sends the message to the number'''
    login = secrets.send_message()
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(login['emailUsername'], login['emailPassword'])
    rand_code = random.randint(0, 999999)
    msg = str(rand_code)
    server.sendmail(
        'Messages',
        login['phone_number'],
        msg)
    h = hashlib.md5()
    h.update(str(rand_code))
    hash_code = h.hexdigest()
    session['hash_code'] = hash_code


@app.route('/admin')
def admin_view():
    courses = course_class.load_data()
    course_list = []
    for x in courses:
        course_list.append(x)
    course_list = sorted(course_list, key=lambda x: str(x))
    sendMsg()  # sets global hash_code variable
    return render_template("admin_form.html", title='Admin', courses=course_list)


@app.route('/admin', methods=['GET', 'POST'])
def admin_view_post():
    text = request.form["admin_secret"]
    j = hashlib.md5()
    j.update(str(text))
    hash_text = j.hexdigest()
    hash_code = session['hash_code']
    # for debugging just make it if True:
    if True:  # hash_code == hash_text:
        if (str(request.form['action_choice']) == 'add_co'):
            return render_template('add_course_form.html', title='Add')
        elif str(request.form['action_choice']) == 'edit_co':
            courses = course_class.load_data()
            for x in courses:
                if str(x) == request.form['course_choice']:
                    course = x
            resp = make_response(render_template(
                'edit_course_form.html',
                course=course,
                title='Edit'))
            resp.set_cookie(
                'course_choice',
                str(request.form['course_choice']),
                max_age=None)
            return resp
        elif str(request.form['action_choice']) == 'remove_co':
            courses = course_class.load_data()
            courses = [item for item in courses if str(
                item) != request.form['course_choice']]
            course_class.save_data(courses)
            return render_template(
                "index.html",
                title='Home',
                visted='True')
        elif str(request.form['action_choice']) == 'add_book':
            courses = course_class.load_data()
            for x in courses:
                if str(x) == request.form['course_choice']:
                    course = x
            resp = make_response(render_template(
                'add_book_form.html',
                course=course,
                title='Add'))
            resp.set_cookie(
                'course_choice',
                str(request.form['course_choice']),
                max_age=None)
            return resp
        elif str(request.form['action_choice']) == 'edit_book':
            courses = course_class.load_data()
            for x in courses:
                if str(x) == request.form['course_choice']:
                    course = x
            count = 0
            urls = {}
            names = {}
            for book in x.books:
                urls[count] = book
                names[count] = x.books[book]
                count += 1
            resp = make_response(render_template(
                'edit_book_form.html',
                course=course,
                amount=count,
                urls=urls,
                names=names,
                title='Edit'))
            resp.set_cookie(
                'course_choice',
                str(request.form['course_choice']),
                max_age=None)
            resp.set_cookie(
                'amount',
                str(count),
                max_age=None)
            return resp
    return 'Sorry you cant use this page.<br><b>' + str(request.form["admin_secret"]) + '</b> is not the secret code. '


@app.route('/add_course', methods=['GET', 'POST'])
def add_course_view_post():
    text = request.form["admin_secret"]
    j = hashlib.md5()
    j.update(str(text))
    hash_text = j.hexdigest()
    hash_code = session['hash_code']
    # for debugging just make it if True:
    if hash_code == hash_text:
        c_dept = str(request.form['course_dept'])
        c_num = str(request.form['course_num'])
        c_name = str(request.form['course_name'])
        l_info_maybe = str(request.form['lecture_info'])
        r_info_maybe = str(request.form['recitation_info'])
        b_info_maybe = str(request.form['lab_info'])
        h_info_maybe = str(request.form['homework_info'])
        e_info_maybe = str(request.form['exams_info'])
        f_info_maybe = str(request.form['final_info'])

        new_c = course_class.Course(c_dept, c_num, c_name)

        if not l_info_maybe == "None":
            new_c.lecture = l_info_maybe
        if not r_info_maybe == "None":
            new_c.recitation = r_info_maybe
        if not b_info_maybe == "None":
            new_c.lab = b_info_maybe
        if not h_info_maybe == "None":
            new_c.homework = h_info_maybe
        if not e_info_maybe == "None":
            new_c.exams = e_info_maybe
        if not f_info_maybe == "None":
            new_c.final = f_info_maybe

        courses = course_class.load_data()
        courses = courses + [new_c]
        course_class.save_data(courses)

        return render_template("index.html", title='Home', visted='True')
    return 'Sorry you cant use this page.<br><b>' + str(request.form["admin_secret"]) + '</b> is not the secret code. '


@app.route('/edit_course', methods=['GET', 'POST'])
def edit_course_view_post():
    text = request.form["admin_secret"]
    j = hashlib.md5()
    j.update(str(text))
    hash_text = j.hexdigest()
    hash_code = session['hash_code']
    # for debugging just make it if True:
    if hash_code == hash_text:
        c_dept = str(request.form['course_dept'])
        c_num = str(request.form['course_num'])
        c_name = str(request.form['course_name'])
        new_c = course_class.Course(c_dept, c_num, c_name)

        l_info_maybe = str(request.form['lecture_info'])
        r_info_maybe = str(request.form['recitation_info'])
        b_info_maybe = str(request.form['lab_info'])
        h_info_maybe = str(request.form['homework_info'])
        e_info_maybe = str(request.form['exams_info'])
        f_info_maybe = str(request.form['final_info'])

        if l_info_maybe != "None":
            new_c.lecture = l_info_maybe
        if r_info_maybe != "None":
            new_c.recitation = r_info_maybe
        if b_info_maybe != "None":
            new_c.lab = b_info_maybe
        if h_info_maybe != "None":
            new_c.homework = h_info_maybe
        if e_info_maybe != "None":
            new_c.exams = e_info_maybe
        if f_info_maybe != "None":
            new_c.final = f_info_maybe

        courses = course_class.load_data()
        courses = [item for item in courses if str(item) != request.cookies.get(
            'course_choice')]  # remove the old course
        courses = courses + [new_c]  # add the new one
        course_class.save_data(courses)

        return render_template("index.html", title='Home', visted='True')
    return 'Sorry you cant use this page.<br><b>' + str(request.form["admin_secret"]) + '</b> is not the secret code. '


@app.route('/add_book', methods=['GET', 'POST'])
def add_book_view_post():
    text = request.form["admin_secret"]
    j = hashlib.md5()
    j.update(str(text))
    hash_text = j.hexdigest()
    hash_code = session['hash_code']
    # for debugging just make it if True:
    if hash_code == hash_text:
        book_name = str(request.form['book_name'])
        book_url = str(request.form['book_url'])
        c_name = request.cookies.get('course_choice')

        courses = course_class.load_data()
        for course in courses:
            if str(course) == c_name:
                course.books[book_url] = book_name
        course_class.save_data(courses)

        return render_template("index.html", title='Home', visted='True')


@app.route('/edit_book', methods=['GET', 'POST'])
def edit_book_view_post():
    text = request.form["admin_secret"]
    j = hashlib.md5()
    j.update(str(text))
    hash_text = j.hexdigest()
    hash_code = session['hash_code']
    # for debugging just make it if True:
    if True:  # hash_code == hash_text:
        amount = int(request.cookies.get('amount'))
        book_name = {}
        book_url = {}
        for i in range(amount):
            book_name[i] = str(request.form['book_name_' + str(i)])
            book_url[i] = str(request.form['book_url_' + str(i)])
        c_name = request.cookies.get('course_choice')

        courses = course_class.load_data()
        for course in courses:
            if str(course) == c_name:
                course.books = {}
                for i in range(amount):
                    course.books[book_url[i]] = book_name[i]
        course_class.save_data(courses)

        return render_template("index.html", title='Home', visted='True')


if __name__ == '__main__':
    app.run(debug=True)
    session['hash_code'] = ""
