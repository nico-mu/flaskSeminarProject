from demo import socket, db, models
import flask_login

'''
    Broadcast messages incoming from on client to all other clients.
'''
@socket.on("message")
def handleMessage(msg):
    message = models.Message(payload=msg, timestamp=db.func.now(), sender_id=flask_login.current_user.get_id(), receiver_id=-1, sender_name=flask_login.current_user.name)
    socket.send(message.sender_name + " : " + message.payload , broadcast=True)
    db.session.add(message)
    db.session.commit()