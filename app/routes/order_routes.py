from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource, abort

from ..services import (
    OrderService,
    OrderItemService,
    TableService,
    UserService,
    RestaurantService,
    MenuItemService,
    BaseService,
)
from ..utils.validations import RestxValidation
from ..utils.decorators import roles_required
from .. import enums

api = Namespace("order", description="Order related operations")

restx_validation = RestxValidation(api=api)


@api.route("/orders")
class CreateOrder(Resource):
    @api.doc(
        security="Bearer Auth",
        responses={
            200: "Order created",
            401: "Missing Authorization Header",
            404: "Restaurant or table not found",
            500: "Failed to create order",
        },
    )
    @api.expect(restx_validation.create_order_model, validate=True)
    @jwt_required()
    def post(self):
        data = api.payload
        user_id = get_jwt_identity()
        restaurant_id = data["restaurant_id"]
        table_id = data["table_id"]
        order_items = data["order_items"]

        # Check if the restaurant and table exist
        restaurant = RestaurantService.get(restaurant_id)
        table = TableService.get(table_id)
        if not restaurant or not table:
            return {"msg": "Restaurant or table not found"}, 404

        total_amount = 0.0
        created_order_items = []

        with BaseService.db.session.begin():
            for order_item in order_items:
                menu_item_id = order_item["menu_item_id"]
                quantity = order_item["quantity"]

                menu_item = MenuItemService.get(menu_item_id)
                if not menu_item or menu_item.category.restaurant_id != restaurant_id:
                    abort(
                        400,
                        message=f"No menu item found with {menu_item_id} or the menu item is not related to the specified restaurant",
                    )

                price = menu_item.price * quantity
                total_amount += price

                created_order_item = OrderItemService.create(
                    {
                        "order_id": None,
                        "menu_item_id": menu_item_id,
                        "quantity": quantity,
                        "price": price,
                    }
                )
                created_order_items.append(created_order_item)

            order = OrderService.create(
                {
                    "user_id": user_id,
                    "restaurant_id": restaurant_id,
                    "table_id": table_id,
                    "status": enums.OrderStatus.PENDING,
                    "total_amount": total_amount,
                }
            )

            for order_item in created_order_items:
                order_item.order_id = order.id

        # Commit the changes
        db.session.commit()

        # Return the created order
        return order.to_dict(), 200


@api.route("/<int:id>")
class ReadUpdateDeleteOrder(Resource):
    @api.doc(
        security="Bearer Auth",
        responses={
            200: "Success",
            401: "Missing Authorization Header",
            403: "Access denied",
            404: "Order not found or not authorized",
        },
    )
    @jwt_required()
    def get(self, id):
        order = OrderService.get(id)

        # Check if the order exists and belongs to the user
        if not order or order.user_id != get_jwt_identity():
            return {"msg": "Order not found or not authorized"}, 404

        return order.to_dict(), 200

    @api.expect(restx_validation.update_order_model, validate=True)
    @api.doc(
        security="Bearer Auth",
        responses={
            200: "Order updated",
            401: "Missing Authorization Header",
            403: "Access denied",
            404: "Order not found or not authorized",
        },
    )
    @jwt_required()
    @roles_required(enums.UserRole.STAFF, api=api)
    def put(self, id):
        data = api.payload
        order = OrderService.get(id)

        # Check if the order exists and belongs to the user
        if not order or order.user_id != get_jwt_identity():
            return {"msg": "Order not found or not authorized"}, 404

        with BaseService.db.session.begin():
            updated_order = OrderService.update(id, data)
        return updated_order.to_dict(), 200

    @api.doc(
        security="Bearer Auth",
        responses={
            200: "Order deleted",
            401: "Missing Authorization Header",
            403: "Access denied",
            404: "Order not found or not authorized",
        },
    )
    @jwt_required()
    @roles_required(enums.UserRole.ADMIN, api=api)
    def delete(self, id):
        order = OrderService.get(id)

        # Check if the order exists and belongs to the user
        if not order or order.user_id != get_jwt_identity():
            return {"msg": "Order not found or not authorized"}, 404

        OrderService.delete(id)
        return {"msg": "Order deleted"}, 200


@api.route("/user/<int:user_id>")
class GetUserOrders(Resource):
    @api.doc(
        security="Bearer Auth",
        responses={
            200: "Success",
            401: "Missing Authorization Header",
            403: "Access denied",
            404: "User not found or not authorized",
        },
    )
    @jwt_required()
    def get(self, user_id):
        user = UserService.get(user_id)

        # Check if the user exists and the requested orders belong to the user
        if not user or user.id != get_jwt_identity():
            return {"msg": "User not found or not authorized"}, 404

        orders = OrderService.get_by_user_id(user_id)
        return [order.to_dict() for order in orders], 200


@api.route("/restaurant/<int:restaurant_id>")
class GetRestaurantOrders(Resource):
    @api.doc(
        security="Bearer Auth",
        responses={
            200: "Success",
            401: "Missing Authorization Header",
            403: "Access denied",
            404: "Restaurant not found or not authorized",
        },
    )
    @jwt_required()
    def get(self, restaurant_id):
        restaurant = RestaurantService.get(restaurant_id)

        # Check if the restaurant exists and the authenticated user is a staff member
        if not restaurant or restaurant.staff_user_id != get_jwt_identity():
            return {"msg": "Restaurant not found or not authorized"}, 404

        orders = OrderService.get_by_restaurant_id(restaurant_id)
        return [order.to_dict() for order in orders], 200


@api.route("/table/<int:table_id>")
class GetTableOrders(Resource):
    @api.doc(
        security="Bearer Auth",
        responses={
            200: "Success",
            401: "Missing Authorization Header",
            403: "Access denied",
            404: "Table not found or not authorized",
        },
    )
    @jwt_required()
    def get(self, table_id):
        table = TableService.get(table_id)

        # Check if the table exists and belongs to the restaurant of the authenticated user
        if not table or table.restaurant.staff_user_id != get_jwt_identity():
            return {"msg": "Table not found or not authorized"}, 404

        orders = OrderService.get_by_table_id(table_id)
        return [order.to_dict() for order in orders], 200
