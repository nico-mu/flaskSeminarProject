from demo import db
from demo.models import User, Server

nico = User(name='Nico', password_hash="12345")
luca = User(name='Luca', password_hash="123")
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
serverTwo.members.append(luca)
db.session.add_all([serverOne, serverTwo])
db.session.commit()
print("Database populated")