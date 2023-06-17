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
        return {
            "id": self.id,
            "restaurant_id": self.restaurant_id,
            "name": self.name,
        }
