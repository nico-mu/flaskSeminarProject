from demo import app
from demo.models import *

@app.get('/api/user')
def get_users():
    '''
    Get all users
    '''
    return User.getAll()

@app.get('/api/user/<int:userId>')
def get_user(userId):
    '''
    Get a user by id
    '''
    return User.get(userId)

@app.get('/api/server')
def get_servers():
    '''
    Get all servers
    '''
    return Server.getAll()

@app.get('/api/server/<int:serverId>')
def get_server(serverId):
    '''
    Get a server by id
    '''
    return Server.get(serverId)

@app.get('/api/message')
def get_messages():
    '''
    Get all messages
    '''
    return Message.getAll()

@app.get('/api/message/<int:messageId>')
def get_message(messageId):
    '''
    Get a message by id
    '''
    return Message.get(messageId)