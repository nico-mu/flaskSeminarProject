#!/usr/bin/env python3
'''
Contains all the models for the application
'''
from demo import db, bycrypt

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

    @property
    def password(self):
        '''
        Prevent password from being accessed
        '''
        raise AttributeError('password is not a readable attribute.')
    
    @password.setter
    def password(self, password):
        '''
        Set password to a hashed password
        '''
        self.password_hash = bycrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        '''
        Check if hashed password matches actual password
        '''
        return bycrypt.check_password_hash(self.password_hash, password)

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

class Message(db.Model):
    '''
    Message table
    '''
    __tablename__ = 'message'
    id = db.Column(db.Integer(), primary_key=True)
    payload = db.Column(db.String(length=256), nullable=False)
    sender = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    receiver = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    server = db.Column(db.Integer(), db.ForeignKey('server.id'))