from flask import Flask, render_template, request, make_response, redirect, session
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

@app.errorhandler(500)
def internal_error(error):
    return render_template('505.html'), 505

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(403)
def forbidden_error(error):
    return render_template('403.html'), 403
