# from enum import Enum
# from . import db, enums
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .base_models import BaseModel, DeletableModel


class Table(DeletableModel):
    __tablename__ = "tables"

    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)
    name = Column(String(50), nullable=False)
    # capacity = Column(Integer, nullable=False)

    def to_dict(self):
        user_orders = {}
        for order in self.orders:
            if order.is_active:
                user_dict = order.user.to_dict()
                user_id = user_dict["id"]
                if user_id not in user_orders:
                    user_orders[user_id] = {
                        "user": user_dict,
                        "orders": [],
                    }
                user_orders[user_id]["orders"].append(order.to_dict())

        return {
            "id": self.id,
            "restaurant_id": self.restaurant_id,
            "name": self.name,
            "users": list(user_orders.values()),
        }
