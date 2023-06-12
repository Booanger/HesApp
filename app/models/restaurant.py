# from . import db
# from .user import User
from .base_model import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship

class Restaurant(BaseModel):
    __tablename__ = 'restaurants'

    staff_user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String(100))
    description = Column(Text)
    address = Column(String(200))
    phone = Column(String(20))
    logo = Column(String(200))

    menu_categories = relationship('MenuCategory', backref='restaurant', lazy='dynamic')
    orders = relationship('Order', backref='restaurant', lazy='dynamic')
    tables = relationship('Table', backref='restaurant', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'staff_user_id': self.staff_user_id,
            'name': self.name,
            'description': self.description,
            'address': self.address,
            'phone': self.phone,
            'logo': self.logo,
        }
