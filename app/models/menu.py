# from . import db
# from .restaurant import Restaurant
from .base_models import BaseModel, DeletableModel
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Float, Text
from sqlalchemy.orm import relationship


class MenuCategory(DeletableModel):
    __tablename__ = "menu_categories"

    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)
    name = Column(String(100))

    menu_items = relationship("MenuItem", backref="category", lazy="dynamic")

    def to_dict(self):
        return {
            "id": self.id,
            "restaurant_id": self.restaurant_id,
            "name": self.name,
            "items": [item.to_dict() for item in self.menu_items if item.is_active],
        }


class MenuItem(DeletableModel):
    __tablename__ = "menu_items"

    category_id = Column(Integer, ForeignKey("menu_categories.id"), nullable=False)
    name = Column(String(100))
    description = Column(Text)
    price = Column(Float, nullable=False)
    image = Column(String(200))

    order_items = relationship("OrderItem", backref="menu_item", lazy="dynamic")

    def to_dict(self):
        return {
            "id": self.id,
            "category_id": self.category_id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "image": self.image,
        }
