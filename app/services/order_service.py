from . import db, Order, MenuItem, OrderItem


class OrderService:
    def create_order(self, user_id, restaurant_id, table_id, menu_items):
        # Place a new order with the selected menu items and table assignment
        order = Order(
            user_id=user_id,
            restaurant_id=restaurant_id,
            table_id=table_id,
            status="pending",
        )
        db.session.add(order)
        db.session.commit()

        # Add order items
        for menu_item_id, quantity in menu_items.items():
            menu_item = MenuItem.query.get(menu_item_id)
            if menu_item:
                order_item = OrderItem(
                    order_id=order.id,
                    menu_item_id=menu_item_id,
                    quantity=quantity,
                    price=menu_item.price,
                )
                db.session.add(order_item)

        db.session.commit()
        return order

    def get_order(self, order_id):
        # Retrieve order information
        return Order.query.get(order_id)

    def update_order(self, order_id, data):
        # Update order information
        order = Order.query.get(order_id)
        if order:
            order.status = data.get("status", order.status)
            order.total_amount = data.get("total_amount", order.total_amount)
            db.session.commit()
            return order
        return None

    def delete_order(self, order_id):
        # Delete an order
        order = Order.query.get(order_id)
        if order:
            db.session.delete(order)
            db.session.commit()
            return True
        return False

    def get_order_status(self, order_id):
        # Get the status of an order
        order = Order.query.get(order_id)
        if order:
            return order.status
        return None

    def get_order_history(self, user_id):
        # Retrieve order history for a specific user
        return Order.query.filter_by(user_id=user_id).all()

    def cancel_order(self, order_id):
        # Cancel an order within a specific timeframe
        order = Order.query.get(order_id)
        if order and order.status == "pending":
            order.status = "canceled"
            db.session.commit()
            return True
        return False
