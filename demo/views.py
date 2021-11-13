'''
Contains the views for the application.
'''
import os
from flask.templating import render_template
from flask import send_from_directory
from demo import app


@app.route("/")
@app.route("/home")
def index():
    '''
    This function renders the index.j2 template
    '''
    return render_template("index.j2")


@app.route("/about")
def about():
    '''
    This function renders the about.j2 template
    '''
    return render_template("about.j2")


@app.route("/users")
def users():
    '''
    This function renders the users.html.j2 template
    '''
    data = [
        {'id': 1, 'name': 'test1'},
        {'id': 2, 'name': 'test2'},
        {'id': 3, 'name': 'test3'},
    ]
    return render_template('users.html.j2', users=data, userName="TestName")


@app.route('/favicon.ico')
def favicon():
    '''
    This function returns the favicon.ico file
    '''
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
