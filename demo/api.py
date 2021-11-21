import uuid

from flask import request
from flask.wrappers import Response

from demo import app, db
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


@app.post('/api/login')
def post_login():
    '''
    Login a user
    Body:
        {
            "name" : String,
            "password" : String
        }
    '''
    data = request.get_json()
    name = data.get("name")
    password = data.get("password")
    user = User.getByName(name)
    if user:
        if user.verify_password(password):
            token = str(uuid.uuid4())
            user.token = token
            user.online = True
            db.session.add(user)
            db.session.commit()
            return Response(str({'uuid': token}), status=200, mimetype='application/json')
    return Response(str({'error': 'Invalid credentials'}), status=401, mimetype='application/json')
    
@app.post('/api/logout')
def post_logout():
    '''
    Logout a user
    Body:
        {
            "uuid" : String
        }
    '''
    data = request.get_json()
    token = data.get("uuid")
    if token:
        user = User.getByToken(token)
        if user:
            user.token = None
            user.online = False
            db.session.add(user)
            db.session.commit()
            return Response(str({'status': 'OK'}), status=200, mimetype='application/json')
    return Response(str({'error': 'Invalid session token'}), status=401, mimetype='application/json')

@app.post('/api/server/join/<int:serverId>')
def post_server_join(serverId):
    '''
    Join a server
    Body:
        {
            "uuid" : String
        }
    '''
    data = request.get_json()
    token = data.get("uuid")
    if token:
        user = User.getByToken(token)
        if user:
            server = Server.query.get(serverId)
            if server:
                server.members.append(user)
                db.session.add(server)
                db.session.commit()
                return Response(str({'status': 'OK'}), status=200, mimetype='application/json')
    return Response(str({'error': 'Invalid session token'}), status=401, mimetype='application/json')

@app.post('/api/server/leave/<int:serverId>')
def post_server_leave(serverId):
    '''
    Leave a server
    Body:
        {
            "uuid" : String
        }
    '''
    data = request.get_json()
    token = data.get("uuid")
    if token:
        user = User.getByToken(token)
        if user:
            server = Server.query.get(serverId)
            if server:
                server.members.remove(user)
                db.session.add(server)
                db.session.commit()
                return Response(str({'status': 'OK'}), status=200, mimetype='application/json')
    return Response(str({'error': 'Invalid session token'}), status=401, mimetype='application/json')