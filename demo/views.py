#!/usr/bin/env python3
'''
Contains the views for the application.
'''
import os
from flask.templating import render_template
from flask import send_from_directory, redirect, url_for, flash, request
import flask_login
from demo import app, db
from demo.models import *
from demo.forms import AddUserForm, RegisterForm, LoginForm, RemoveUserForm

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


@app.route("/users", methods=["GET"])
@flask_login.login_required
def users():
    '''
    This function renders the users.html.j2 template
    '''
    addUserForm = AddUserForm()
    removeUserForm = RemoveUserForm()
    users = User.query.all()
    return render_template('users.html.j2', users=users, removeUserForm=removeUserForm, addUserForm=addUserForm)

@app.route("/users/removeUser", methods=["GET", "POST"])
@flask_login.login_required
def removeUser():
    '''
    Subroute of users. This funtions handles removing users.
    '''
    removeUserForm = RemoveUserForm()
    addUserForm = AddUserForm()
    if request.method == "POST":
        user = User.query.filter_by(id=request.form.get("removeUser")).first()
        db.session.delete(user)
        db.session.commit()
        flash("User deleted successfully!", "success")
        return redirect(url_for("users"))
    users = User.query.all()
    return render_template('users.html.j2', users=users, removeUserForm=removeUserForm, addUserForm=addUserForm)

@app.route("/users/addUser", methods=["GET", "POST"])
@flask_login.login_required
def addUser():
    '''
    Subroute of users. This funtions handles adding users.
    '''
    removeUserForm = RemoveUserForm()
    addUserForm = AddUserForm()
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        admin = request.form.get("admin")
        if admin == "y":
            admin = True
        user = User(name=name, password=password, admin=admin)
        db.session.add(user)
        db.session.commit()
        flash("User added successfully!", "success")
        return redirect(url_for("users"))
    users = User.query.all()
    return render_template('users.html.j2', users=users, removeUserForm=removeUserForm, addUserForm=addUserForm)

@app.route('/favicon.ico')
def favicon():
    '''
    This function returns the favicon.ico file
    '''
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

# Cross Site Request Forgery (CSRF) protection needed in register.html.j2 and login.html.j2 by adding {{ form.hidden_tag() }}
@app.route('/register', methods=['GET', 'POST'])
def register():
    '''
    This function renders the register.html.j2 template
    '''
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(name=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flask_login.login_user(user)
        # show an alert message
        flash('User successfully registered', category='success')
        return redirect(url_for('index'))
    if form.errors:
        for error in form.errors.values():
            flash(error[0])
    return render_template('register.html.j2', form=form)

# Cross Site Request Forgery (CSRF) protection needed in register.html.j2 and login.html.j2 by adding {{ form.hidden_tag() }}
@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
    This function renders the login.html.j2 template
    '''
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.username.data).first()
        if user is None or not user.verify_password(form.password.data):
            flash('Invalid username or password', category='error')
            return redirect(url_for('login'))
        # show an alert message
        flask_login.login_user(user)
        flash('User successfully logged in', category='success')
        return redirect(url_for('index'))
    return render_template('login.html.j2', form=form)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    '''
    This function logs out the user
    '''
    # show an alert message
    flask_login.logout_user()
    flash('User successfully logged out', category='success')
    return redirect(url_for('index'))