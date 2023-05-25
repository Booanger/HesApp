from enum import Enum
from . import db
from .user import User
from .restaurant import Restaurant
from .. import enums

print("order.py")

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    status = db.Column(db.Enum(enums.OrderStatus))
    total_amount = db.Column(db.Float)

    order_items = db.relationship('OrderItem', backref='order', lazy='dynamic')
    payment_transactions = db.relationship('PaymentTransaction', backref='order', lazy='dynamic')


class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_items.id'))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
