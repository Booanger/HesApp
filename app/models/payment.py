# from . import db
# from .order import Order
from enum import Enum
from .. import enums
from .base_models import BaseModel
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Float
from sqlalchemy.orm import relationship


class PaymentTransaction(BaseModel):
    __tablename__ = 'payment_transactions'

    order_id = Column(Integer, ForeignKey('orders.id'))
    transaction_id = Column(String(100))
    status = Column(Enum(enums.TransactionStatus))
    amount = Column(Float)
