# from enum import Enum
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
# from . import db, enums
from .base_model import BaseModel


class Table(BaseModel):
    __tablename__ = 'tables'

    restaurant_id = Column(Integer, ForeignKey('restaurants.id'), nullable=False)
    name = Column(String(50), nullable=False)
    description = Column(String(200))
    capacity = Column(Integer, nullable=False)

    restaurant = relationship('Restaurant', backref='tables', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'restaurant_id': self.restaurant_id,
            'name': self.name,
            'description': self.description,
            'capacity': self.capacity
        }
