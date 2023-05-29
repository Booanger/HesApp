from enum import Enum
from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship, query_expression
from . import db, enums

print("user.py")

class User(db.Model):
    __tablename__ = 'users'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    first_name: str = Column(String(50))
    last_name: str = Column(String(50))
    email: str = Column(String(120), unique=True)
    password: str = Column(String(200))
    phone: str = Column(String(20))
    role: enums.UserRole = Column(Enum(enums.UserRole))

    orders: query_expression = relationship('Order', backref='user', lazy='dynamic')
    restaurant: query_expression = relationship('Restaurant', uselist=False, viewonly=True)

    # @staticmethod
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
