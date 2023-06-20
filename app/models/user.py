from enum import Enum
from sqlalchemy import Column, String, Enum
from sqlalchemy.orm import relationship
from . import enums
from .base_models import BaseModel, DeletableModel


class User(DeletableModel):
    __tablename__ = "users"

    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(200))
    phone = Column(String(20))
    role = Column(Enum(enums.UserRole))

    orders = relationship("Order", backref="user", lazy="dynamic")
    restaurant = relationship("Restaurant", uselist=False, viewonly=True)

    def to_dict(self):
        data = {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role.value,
            "phone": self.phone,
        }

        return data
