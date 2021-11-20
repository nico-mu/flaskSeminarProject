#!/usr/bin/env python3
'''
Main Module for the app
'''
# Versions  Python              3.8.10
#           Flask               2.0.2
#           flask_sqlalchemy    2.5.1
#           flask-wtf           1.0.0
#           wtforms             3.0.0
#           flask_bcrypt        0.7.1
#           flask_login         0.5.0
#           flask-principal     0.4.0

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_principal import Permission, Principal, RoleNeed, identity_loaded
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thisissecret'
app.config['DEBUG'] = True
app.url_map.strict_slashes = False

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
import demo.api
import demo.models
import demo.views
#pylint: enable=wrong-import-position
