from . import db, Order, MenuItem, OrderItem, Table


class OrderService:
    def create_order(self, user_id, restaurant_id, table_id, menu_items):
        # Place a new order with the selected menu items and table assignment
        table = Table.query.get(table_id)
        if not table:
            return {"msg": "Table not found"}, 404
        if table.restaurant.id != restaurant_id:
            return {"msg": "Access denied"}, 403

        order = Order(
            user_id=user_id,
            restaurant_id=restaurant_id,
            table_id=table_id,
            status="pending",
            is_active=True,
        )
        db.session.add(order)
        db.session.flush()

        total_amount = 0.0
        # Add order items
        for menu_item_id, quantity in menu_items.items():
            menu_item = MenuItem.query.get(menu_item_id)
            if menu_item:
                total_amount += menu_item.price * quantity

                order_item = OrderItem(
                    order_id=order.id,
                    menu_item_id=menu_item_id,
                    menu_item_name=menu_item.name,
                    quantity=quantity,
                    price=menu_item.price,
                )
                db.session.add(order_item)
            else:
                return {"msg": "Menu item not found"}, 404

        order.total_amount = total_amount
        db.session.commit()

        # publish(f"127.0.0.1/restaurants/{restaurant_id}/order", order.id)

        return order, 201

    def get_order(self, order_id):
        # Retrieve order information
        return Order.query.get(order_id)

    def update_order(self, order_id, data):
        # Update order information
        order = Order.query.get(order_id)
        if order:
            order.status = data.get("status", order.status)
            # order.total_amount = data.get("total_amount", order.total_amount)
            db.session.commit()
            return order
        return None

    # def delete_order(self, order_id):
    #     # Delete an order
    #     order = Order.query.get(order_id)
    #     if order:
    #         db.session.delete(order)
    #         db.session.commit()
    #         return True
    #     return False

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
