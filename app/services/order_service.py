from .base_service import BaseService
from ..models import Order, OrderItem


class OrderService(BaseService):
    model = Order

    @classmethod
    def get_by_user_id(self, user_id):
        return self.model.query.filter_by(user_id=user_id).first()

    @classmethod
    def get_by_restaurant_id(self, restaurant_id):
        return self.model.query.filter_by(restaurant_id=restaurant_id).first()

    @classmethod
    def get_by_table_id(self, table_id):
        return self.model.query.filter_by(table_id=table_id).first()

class OrderItemService(BaseService):
    model = OrderItem

    @classmethod
    def get_by_order_id(self, order_id):
        return self.model.query.filter_by(order_id=order_id).first()
