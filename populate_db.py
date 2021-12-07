#!/usr/bin/env python3
from demo import db
from demo.models import User, Server, Message

nico = User(name='Nico', password="12345", admin=True)
luca = User(name='Luca', password="123")
db.drop_all()
db.create_all()
db.session.add_all([nico, luca])
db.session.commit()

nico = User.query.filter_by(name='Nico').first()
luca = User.query.filter_by(name='Luca').first()
serverOne = Server(name='serverOne', status=False, owner_id=nico.id)
serverTwo = Server(name='serverTwo', status=True, owner_id=luca.id)
db.session.add_all([serverOne, serverTwo])
db.session.commit()

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
messageOne = Message(payload="Hello World", sender=nico)
messageTwo = Message(payload="Hello World back!", sender=luca)
messageThree = Message(payload="Test", sender=nico)
db.session.add_all([messageOne, messageTwo, messageThree, nico, luca])
db.session.commit()

serverOne = Server.query.filter_by(name='serverOne').first()
for index in range(1, 100):
    user = User(name='User' + str(index), password="12345")
    serverOne.members.append(user)
    db.session.add(user)
db.session.add(serverOne)
db.session.commit()
print("Database populated")
