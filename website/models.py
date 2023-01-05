from . import db
from flask_login import UserMixin

# Represents a reservation at a specifig time for the gym
class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary key -> unique identifier to represent the object
    date = db.Column(db.DateTime(timezone=True), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) # primary key -> unique identifier to represent the object
    email = db.Column(db.String(150), unique=True) # unique -> only one user can have a specifi email
    password = db.Column(db.String(150))
    firstname = db.Column(db.String(150))
    lastname = db.Column(db.String(150))
    reservations = db.relationship('Reservation')
