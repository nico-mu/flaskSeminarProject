#!/usr/bin/env python3
'''
Main Module for the app
'''
# Versions  Python   3.8.10
#           Flask    2.0.2

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_principal import Permission, Principal, RoleNeed, identity_loaded

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thisissecret'
app.config['DEBUG'] = True

db = SQLAlchemy(app)
bycrypt = Bcrypt(app)
principals = Principal(app)
admin_permission = Permission(RoleNeed('admin'))
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

'''
Handle Roles and Permissions
'''
@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    user = db.session.query(demo.models.User).get(identity.id)
    if user and user.admin == True:
        identity.provides.add(RoleNeed('admin'))

'''
add import statements here to avoid circular imports
'''
#pylint: disable=wrong-import-position
import demo.views
import demo.models
#pylint: enable=wrong-import-position
