from demo import socket, db, models
import flask_login

'''
    Broadcast messages incoming from on client to all other clients.
'''
@socket.on("message")
def handleMessage(msg):
    message = models.Message(payload=msg, sender=flask_login.current_user)
    db.session.add(message)
    db.session.commit()
    sendMessage(message)

def sendMessage(message):
    socket.send(f"[{message.timestamp}] {message.sender.name} : {message.payload}" , broadcast=True)