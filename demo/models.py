#!/usr/bin/env python3
'''
Contains all the models for the application
'''
from demo import db

# Association table for many-to-many relationship between users and servers
association_table = db.Table('association', db.Model.metadata,
    db.Column('user_id', db.ForeignKey('user.id'), primary_key=True),
    db.Column('server_id', db.ForeignKey('server.id'), primary_key=True)
)

class User(db.Model):
    '''
    User table
    '''
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=16), unique=True, nullable=False)
    password_hash = db.Column(db.String(length=60), nullable=False)
    servers = db.relationship('Server', secondary=association_table,
        back_populates="members")

    def __repr__(self):
        return f'<User {self.name}>'

class Server(db.Model):
    '''
    Server table
    '''
    __tablename__ = 'server'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=16), unique=True, nullable=False)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))
    status = db.Column(db.Boolean, nullable=False)
    members = db.relationship('User', secondary=association_table, back_populates='servers')

    def __repr__(self):
        return f'<Server {self.name}>'
