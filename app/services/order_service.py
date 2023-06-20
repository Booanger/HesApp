from datetime import datetime
from sqlalchemy import desc
from . import db, Order, MenuItem, OrderItem, Table, OrderStatus
from werkzeug.exceptions import NotFound


class OrderService:
    @staticmethod
    def create_order(user_id, restaurant_id, table_id, order_items):
        # Place a new order with the selected menu items and table assignment
        table = Table.query.filter_by(id=table_id, is_active=True).first()
        if not table:
            return {"msg": "Table not found"}, 404
        if table.restaurant.id != restaurant_id:
            return {"msg": "Access denied"}, 403

        order = Order(
            user_id=user_id,
            restaurant_id=restaurant_id,
            table_id=table_id,
            status=OrderStatus.PENDING,
            is_active=True,
            total_amount=0,
        )
        db.session.add(order)
        db.session.flush()

        total_amount = 0.0
        # Add order items
        for order_item_data in order_items:
            menu_item_id = order_item_data.get("menu_item_id")
            quantity = order_item_data.get("quantity")

            menu_item = MenuItem.query.filter_by(
                id=menu_item_id, is_active=True
            ).first()
            if menu_item and menu_item.category.restaurant_id == restaurant_id:
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

        return order.to_dict(), 201

    # TODO NEED WORK
    @staticmethod
    def get_order(user_id, order_id):
        # Retrieve order information
        return Order.query.get(order_id)

    # TODO NEED WORK
    @staticmethod
    def get_order_status(user_id, order_id):
        # Get the status of an order
        order = Order.query.get(order_id)
        if order:
            return order.status
        return None

    @staticmethod
    def get_order_history(customer_user_id, page=1, per_page=10):
        # Retrieve order history for a specific user with pagination, sorted by order_time in descending order
        try:
            # Retrieve order history for a specific user with pagination, sorted by order_time in descending order
            query = Order.query.filter_by(user_id=customer_user_id).order_by(
                desc(Order.order_time)
            )

            paginated_orders = query.paginate(page=page, per_page=per_page)

            orders = paginated_orders.items
            total_orders = paginated_orders.total
            total_pages = paginated_orders.pages

            return {
                "orders": [order.to_dict() for order in orders],
                "total_orders": total_orders,
                "total_pages": total_pages,
            }, 200

        except NotFound:
            return {"msg": "Page not found"}, 404

    @staticmethod
    def update_order_status(staff_user_id, order_id, data):
        # Update order information
        order = Order.query.filter_by(id=order_id, is_active=True).first()

        if order and order.restaurant.staff_user_id == staff_user_id:
            status = data.get("status", order.status)
            order.status = status

            if (
                status == OrderStatus.DELIVERED.value
                or status == OrderStatus.CANCELED.value
            ):
                order.is_active = False

                if status == OrderStatus.DELIVERED:
                    order.delivery_time = datetime.utcnow()

            db.session.commit()

            return order.to_dict(), 200

        return {"msg": "Order not found"}, 404

    @staticmethod
    def cancel_my_order(customer_user_id, order_id):
        # Cancel an order within a specific timeframe
        order = Order.query.filter_by(id=order_id, is_active=True).first()
        if (
            order
            and order.user_id == customer_user_id
            and order.status == OrderStatus.PENDING.value
        ):
            order.status = OrderStatus.CANCELED.value
            order.is_active = False
            db.session.commit()
            return {"msg": "Order canceled"}, 204
        return {"msg": "Order not found"}, 404
