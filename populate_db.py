#!/usr/bin/env python3
from demo import db
from demo.models import User, Server, Message
from datetime import datetime

nico = User(name='Nico', password="12345", admin=True)
luca = User(name='Luca', password="123")
serverOne = Server(name='serverOne', status=False)
serverTwo = Server(name='serverTwo', status=True)
db.drop_all()
db.create_all()
db.session.add_all([nico, luca, serverOne, serverTwo])
db.session.commit()

nico = User.query.filter_by(name='Nico').first()
luca = User.query.filter_by(name='Luca').first()
serverOne = Server.query.filter_by(name='serverOne').first()
serverTwo = Server.query.filter_by(name='serverTwo').first()
serverOne.owner = nico.id
serverOne.members.append(nico)
serverOne.members.append(luca)
serverTwo.owner = luca.id
serverTwo.members.append(luca)
db.session.add_all([serverOne, serverTwo])
db.session.commit()

nico = User.query.filter_by(name='Nico').first()
luca = User.query.filter_by(name='Luca').first()
serverOne = Server.query.filter_by(name='serverOne').first()
serverTwo = Server.query.filter_by(name='serverTwo').first()
messageOne = Message(payload="Hello World", sender=nico.id, receiver=luca.id, server=serverOne.id, timestamp=datetime.now())
messageTwo = Message(payload="Hello World back!", sender=luca.id, receiver=nico.id, server=serverOne.id, timestamp=datetime.now())
messageThree = Message(payload="Private Message", sender=luca.id, receiver=nico.id, timestamp=datetime.now())
db.session.add_all([messageOne, messageTwo, messageThree])
db.session.commit()
print("Database populated")