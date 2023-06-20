from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource, abort
from flask import request

from ..services import (
    OrderService,
)
from ..utils.validations import RestxValidation
from ..utils.decorators import roles_required
from .. import enums

api = Namespace("order", description="Order related operations")

restx_validation = RestxValidation(api=api)


@api.route("")
class CreateOrder(Resource):
    @api.doc(
        security="Bearer Auth",
        responses={
            201: "Order created",
            401: "Missing Authorization Header",
            403: "Access denied",
            404: "Table not found / Menu item not found",
            500: "Internal Server Error",
        },
    )
    @api.expect(restx_validation.create_order_model, validate=True)
    @jwt_required()
    @roles_required(enums.UserRole.CUSTOMER, api=api)
    def post(self):
        data = api.payload
        user_id = get_jwt_identity()
        restaurant_id = data["restaurant_id"]
        table_id = data["table_id"]
        order_items = data["order_items"]

        return OrderService.create_order(user_id, restaurant_id, table_id, order_items)


@api.route("/customer-history")
class GetOrderHistory(Resource):
    @api.doc(
        security="Bearer Auth",
        responses={
            200: "Order history retrieved",
            401: "Missing Authorization Header",
            403: "Access denied",
            404: "Page not found",
            500: "Internal Server Error",
        },
    )
    # @api.expect(restx_validation.get_order_history_model, validate=True)
    @api.param("page", "Page number", required=False)
    @api.param("per_page", "Items per page", required=False)
    @jwt_required()
    @roles_required(enums.UserRole.CUSTOMER, api=api)
    def get(self):
        user_id = get_jwt_identity()

        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))

        return OrderService.get_order_history(user_id, page, per_page)


@api.route("/<int:order_id>/update-status")
class UpdateOrderStatus(Resource):
    @api.doc(
        security="Bearer Auth",
        responses={
            200: "Order status updated",
            401: "Missing Authorization Header",
            403: "Access denied",
            404: "Order not found",
            500: "Internal Server Error",
        },
    )
    @api.expect(restx_validation.update_order_status_model, validate=True)
    @jwt_required()
    @roles_required(enums.UserRole.STAFF, api=api)
    def put(self, order_id):
        user_id = get_jwt_identity()
        data = api.payload

        return OrderService.update_order_status(user_id, order_id, data)


@api.route("/<int:order_id>/cancel")
class CancelOrder(Resource):
    @api.doc(
        security="Bearer Auth",
        responses={
            204: "Order canceled",
            401: "Missing Authorization Header",
            403: "Access denied",
            404: "Order not found",
            500: "Internal Server Error",
        },
    )
    @jwt_required()
    @roles_required(enums.UserRole.CUSTOMER, api=api)
    def delete(self, order_id):
        user_id = get_jwt_identity()

        return OrderService.cancel_my_order(user_id, order_id)
