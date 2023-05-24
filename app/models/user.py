from enum import Enum
from . import db, enums

print("user.py")

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    role = db.Column(db.Enum(enums.UserRole))
    
    orders = db.relationship('Order', backref='user', lazy='dynamic')
    restaurants = db.relationship('Restaurant', backref='staff_user', lazy='dynamic')