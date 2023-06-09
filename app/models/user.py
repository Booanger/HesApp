from enum import Enum
from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from . import db, enums

class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(120), unique=True)
    password = Column(String(200))
    phone = Column(String(20))
    role = Column(Enum(enums.UserRole))

    orders = relationship('Order', backref='user', lazy='dynamic')
    restaurant = relationship('Restaurant', uselist=False, viewonly=True)

    def to_dict(self):
        data = {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'role': self.role.value,
            'phone': self.phone,
        }

        if self.role == enums.UserRole.STAFF and self.restaurant:
            data['restaurant'] = self.restaurant.to_dict()

        return data
