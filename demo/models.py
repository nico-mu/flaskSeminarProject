#!/usr/bin/env python3
'''
Contains all the models for the application
'''
from demo import db, bycrypt, login_manager
from flask_login import UserMixin

# Association table for many-to-many relationship between users and servers
association_table = db.Table('association', db.Model.metadata,
    db.Column('user_id', db.ForeignKey('user.id'), primary_key=True),
    db.Column('server_id', db.ForeignKey('server.id'), primary_key=True)
)


@login_manager.user_loader
def load_user(user_id):
    '''
    This function is used by Flask-Login to load a user from the database
    '''
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    '''
    User table
    UserMixin is a class that provides default implementations for the methods
    that Flask-Login expects user objects to have.
    '''
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=16), unique=True, nullable=False)
    password_hash = db.Column(db.String(length=60), nullable=False)
    servers = db.relationship('Server', secondary=association_table,
        back_populates="members")
    admin = db.Column(db.Boolean, default=False)

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

    def getAll():
        '''
        Get all users
        Used by the API to get all users GET /api/user
        '''
        buffer = []
        for user in User.query.all():
            buffer.append(User.get(user.id))
        return { "data" : buffer }

    def get(userId):
        '''
        Get a user by id
        Used by the API to get a user GET /api/user/<id>
        '''
        user = User.query.get(userId)
        if user:
            return { "id" :  user.id, "name" : user.name, "admin" : user.admin, "servers" : [server.id for server in user.servers] }
        return {}

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

    def getAll():
        '''
        Get all users
        Used by the API to get all users GET /api/user
        '''
        buffer = []
        for server in Server.query.all():
            buffer.append(Server.get(server.id))
        return { "data" : buffer }

    def get(serverId):
        '''
        Get a user by id
        Used by the API to get a user GET /api/user/<id>
        '''
        server = Server.query.get(serverId)
        if server:
            return { "id" :  server.id, "name" : server.name, "owner" : server.owner, "status" : server.status , "members" : [member.id for member in server.members] }
        return {}

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
    timestamp = db.Column(db.Integer(), nullable=False)
    server = db.Column(db.Integer(), db.ForeignKey('server.id'))

    def getAll():
        '''
        Get all messages
        Used by the API to get all messages GET /api/message
        '''
        buffer = []
        for message in Message.query.all():
            buffer.append(Message.get(message.id))
        return { "data" : buffer }

    def get(messageId):
        '''
        Get a message by id
        Used by the API to get a message GET /api/message/<id>
        '''
        message = Message.query.get(messageId)
        if message:
            return { "id" :  message.id, "payload" : message.payload, "sender" : message.sender, "receiver" : message.receiver, "timestamp" : message.timestamp, "server" : message.server }
        return {}

    def __repr__(self):
        return f'<Message {self.id}>'