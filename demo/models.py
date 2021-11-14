#!/usr/bin/env python3
'''
Contains all the models for the application
'''
from demo import db


class User(db.Model):
    '''
    User table
    '''
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True, nullable=False, unique=True)
    username = db.Column(db.String(length=16), unique=True, nullable=False)
    password = db.Column(db.String(length=16), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username
