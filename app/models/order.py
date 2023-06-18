# from . import db
# from .user import User
# from .restaurant import Restaurant
from enum import Enum
from .. import enums
from .base_models import BaseModel, DeletableModel
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime


class Order(DeletableModel):
    __tablename__ = "orders"

    user_id = Column(Integer, ForeignKey("users.id"))
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    table_id = Column(Integer, ForeignKey("tables.id"))
    status = Column(Enum(enums.OrderStatus))
    total_amount = Column(Float)
    order_time = Column(DateTime, default=datetime.utcnow())
    delivery_time = Column(DateTime)

    order_items = relationship("OrderItem", backref="order", lazy="dynamic")
    payment_transactions = relationship(
        "PaymentTransaction", backref="order", lazy="dynamic"
    )
    table = relationship("Table", backref="orders", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "restaurant_id": self.restaurant_id,
            "table_id": self.table_id,
            "status": self.status.value,
            "total_amount": self.total_amount,
            "order_time": self.order_time.isoformat(),
            "delivery_time": self.delivery_time.isoformat()
            if self.delivery_time
            else None,
            "order_items": [order_item.to_dict() for order_item in self.order_items],
            "payment_transactions": [
                transaction.to_dict() for transaction in self.payment_transactions
            ],
        }


class OrderItem(DeletableModel):
    __tablename__ = "order_items"

    order_id = Column(Integer, ForeignKey("orders.id"))
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"))
    menu_item_name = Column(String(100))
    quantity = Column(Integer)
    price = Column(Float)

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "menu_item_id": self.menu_item_id,
            "menu_item_name": self.menu_item_name,
            "quantity": self.quantity,
            "price": self.price,
        }
