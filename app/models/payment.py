from enum import Enum
from . import db
from .order import Order
from .. import enums

print("payment.py")

class PaymentTransaction(db.Model):
    __tablename__ = 'payment_transactions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    transaction_id = db.Column(db.String(100))
    status = db.Column(db.Enum(enums.TransactionStatus))
    amount = db.Column(db.Float)
    #order = db.relationship('Order')
