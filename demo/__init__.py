#!/usr/bin/env python3
'''
Main Module for the app
'''
# Versions  Python   3.8.10
#           Flask    2.0.2

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thisissecret'
app.config['DEBUG'] = True
db = SQLAlchemy(app)

'''
add import statements here to avoid circular imports
'''
#pylint: disable=wrong-import-position
import demo.views
import demo.models
#pylint: enable=wrong-import-position
