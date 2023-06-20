# from . import db
# from .order import Order
from enum import Enum
from .. import enums
from .base_models import BaseModel
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Float
from sqlalchemy.orm import relationship


class PaymentTransaction(BaseModel):
    __tablename__ = "payment_transactions"

    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    transaction_id = Column(String(100), nullable=False)
    status = Column(Enum(enums.TransactionStatus), nullable=False)
    amount = Column(Float, nullable=False)

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "transaction_id": self.transaction_id,
            "status": self.status.value,
            "amount": self.amount,
        }
