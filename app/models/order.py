from enum import Enum
# from . import db
# from .user import User
# from .restaurant import Restaurant
from .. import enums
from .base_model import BaseModel
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Float
from sqlalchemy.orm import relationship

class Order(BaseModel):
    __tablename__ = 'orders'

    user_id = Column(Integer, ForeignKey('users.id'))
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    table_id = Column(Integer, ForeignKey('tables.id'))  # New table_id field
    status = Column(Enum(enums.OrderStatus))
    total_amount = Column(Float)

    order_items = relationship('OrderItem', backref='order', lazy='dynamic')
    payment_transactions = relationship('PaymentTransaction', backref='order', lazy='dynamic')
    table = relationship('Table', backref='orders', lazy=True)


class OrderItem(BaseModel):
    __tablename__ = 'order_items'

    order_id = Column(Integer, ForeignKey('orders.id'))
    menu_item_id = Column(Integer, ForeignKey('menu_items.id'))
    quantity = Column(Integer)
    price = Column(Float)
