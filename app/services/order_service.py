from ..models import db, Order, OrderItem

print("order service.py")

class OrderService:
    @staticmethod
    def create_order(data):
        order = Order(**data)
        db.session.add(order)
        db.session.commit()
        return order

    @staticmethod
    def get_orders(user_id=None, restaurant_id=None):
        if user_id:
            return Order.query.filter_by(user_id=user_id).all()
        elif restaurant_id:
            return Order.query.filter_by(restaurant_id=restaurant_id).all()
        else:
            return Order.query.all()
        
    @staticmethod
    def update_order(order_id, updated_data):
        order = Order.query.get(order_id)
        if order:
            for key, value in updated_data.items():
                setattr(order, key, value)
            db.session.commit()
        return order

    @staticmethod
    def delete_order(order_id):
        order = Order.query.get(order_id)
        if order:
            db.session.delete(order)
            db.session.commit()

    ################################################################

    @staticmethod
    def add_item_to_order(order_id, item_data):
        item = OrderItem(order_id=order_id, **item_data)
        db.session.add(item)
        db.session.commit()
        return item

    @staticmethod
    def get_order_items(order_id):
        return OrderItem.query.filter_by(order_id=order_id).all()

    @staticmethod
    def update_order_item(order_item_id, updated_data):
        order_item = OrderItem.query.get(order_item_id)
        if order_item:
            for key, value in updated_data.items():
                setattr(order_item, key, value)
            db.session.commit()
        return order_item

    @staticmethod
    def delete_order_item(order_item_id):
        order_item = OrderItem.query.get(order_item_id)
        if order_item:
            db.session.delete(order_item)
            db.session.commit()
