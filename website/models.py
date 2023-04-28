from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa

db = SQLAlchemy(add_models_to_shell=True)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"<User: {self.email}>"


class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(sa.DateTime, nullable=False)

    def __repr__(self):
        return f"<Reservation: {self.time}>"
