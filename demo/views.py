#!/usr/bin/env python3
'''
Contains the views for the application.
'''
import os
from flask.templating import render_template
from flask import send_from_directory, redirect, url_for, flash, request, current_app
import flask_login
from flask_principal import AnonymousIdentity, Identity, identity_changed
from demo import app, db, admin_permission
from demo.models import *
from demo.forms import AddServerForm, AddUserForm, JoinServerForm, RegisterForm, LoginForm, RemoveServerForm, RemoveUserForm

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
@admin_permission.require(http_exception=403)
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
@admin_permission.require(http_exception=403)
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
            flash(error[0], category='danger')
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
            flash('Invalid username or password', category='danger')
            return redirect(url_for('login'))
        # show an alert message
        flask_login.login_user(user)
        identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))
        flash('User successfully logged in', category='success')
        return redirect(url_for('index'))
    return render_template('login.html.j2', form=form)

@app.route('/logout', methods=['GET', 'POST'])
@flask_login.login_required
def logout():
    '''
    This function logs out the user
    '''
    # show an alert message
    flask_login.logout_user()
    identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())
    flash('User successfully logged out', category='success')
    return redirect(url_for('index'))

@app.route('/server')
@flask_login.login_required
def server():
    '''
    This function renders the servers.html.j2 template
    '''
    return render_template('servers.html.j2', servers=Server.query.all(), addServerForm=AddServerForm(), removeServerForm=RemoveServerForm(), joinServerForm=JoinServerForm())

@app.route('/server/remove', methods=['GET', 'POST'])
@flask_login.login_required
@admin_permission.require(http_exception=403)
def removeServer():
    '''
    Subroute of server. This funtions handles removing server.
    '''
    addServerForm = AddServerForm()
    removeServerForm = RemoveServerForm()
    joinServerForm = JoinServerForm()
    if request.method == "POST":
        server = Server.query.filter_by(id=request.form.get("removeServer")).first()
        db.session.delete(server)
        db.session.commit()
        flash("Server deleted successfully!", "success")
        return redirect(url_for("server"))
    return render_template('servers.html.j2', servers=Server.query.all(), addServerForm=addServerForm, removeServerForm=removeServerForm, joinServerForm=joinServerForm)

@app.route('/server/add', methods=['GET', 'POST'])
@flask_login.login_required
@admin_permission.require(http_exception=403)
def addServer():
    '''
    Subroute of server. This funtions handles adding server.
    '''
    addServerForm = AddServerForm()
    removeServerForm = RemoveServerForm()
    joinServerForm = JoinServerForm()
    if request.method == "POST" and addServerForm.validate_on_submit():
        name = request.form.get("name")
        owner = request.form.get("owner")
        status = request.form.get("status")
        if status == "y":
            status = True
        server = Server(name=name, owner=owner, status=status)
        db.session.add(server)
        db.session.commit()
        flash("Server added successfully!", "success")
        return redirect(url_for("server"))
    if addServerForm.errors:
        for error in addServerForm.errors.values():
            flash(error[0], category='danger')
    return render_template('servers.html.j2', servers=Server.query.all(), addServerForm=addServerForm, removeServerForm=removeServerForm, joinServerForm=joinServerForm)

@app.route('/server/join', methods=['GET', 'POST'])
@flask_login.login_required
@admin_permission.require(http_exception=403)
def joinServer():
    '''
    Subroute of server. This funtions handles adding users to a server.
    '''
    addServerForm = AddServerForm()
    removeServerForm = RemoveServerForm()
    joinServerForm = JoinServerForm()
    if request.method == "POST" and joinServerForm.validate_on_submit():
        userId = request.form.get("user")
        serverId = request.form.get("serverId")
        user = User.query.filter_by(id=userId).first()
        server = Server.query.filter_by(id=serverId).first()
        user.servers.append(server)
        db.session.commit()
        flash("User successfully added to server!", "success")
        return redirect(url_for("server"))
    if joinServerForm.errors:
        for error in joinServerForm.errors.values():
            flash(error[0], category='danger')
    return render_template('servers.html.j2', servers=Server.query.all(), addServerForm=addServerForm, removeServerForm=removeServerForm, joinServerForm=joinServerForm)
