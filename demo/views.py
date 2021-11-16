#!/usr/bin/env python3
'''
Contains the views for the application.
'''
import os
from flask.templating import render_template
from flask import send_from_directory
from demo import app
from demo.models import *
from demo.forms import RegisterForm, LoginForm


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
    users = User.query.all()
    return render_template('users.html.j2', users=users, userName="TestName")


@app.route('/favicon.ico')
def favicon():
    '''
    This function returns the favicon.ico file
    '''
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/register')
def register():
    '''
    This function renders the register.html.j2 template
    '''
    form = RegisterForm()
    return render_template('register.html.j2', form=form)

@app.route('/login')
def login():
    '''
    This function renders the register.html.j2 template
    '''
    form = LoginForm()
    return render_template('login.html.j2', form=form)