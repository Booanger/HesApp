from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource

from ..services import RestaurantService
from ..utils.validations import RestxValidation
from ..utils.decorators import roles_required
from .. import enums

api = Namespace("table", description="Table related operations")

restx_validation = RestxValidation(api=api)


@api.route("")
class CreateTable(Resource):
    @api.expect(restx_validation.create_table_model, validate=True)
    @api.doc(
        security="Bearer Auth",
        responses={
            200: "Table created",
            401: "Missing Authorization Header",
            403: "Access denied",
            409: "Table already exists",
        },
    )
    @jwt_required()
    @roles_required(enums.UserRole.STAFF, api=api)
    def post(self):
        data = api.payload
        name = data["name"]
        user_id = get_jwt_identity()

        return RestaurantService.create_table(user_id, name)


@api.route("s/<int:restaurant_id>")
class GetTablesByRestaurant(Resource):
    @api.doc(
        security="Bearer Auth",
        responses={
            200: "Success",
            401: "Missing Authorization Header",
            403: "Access denied",
            404: "No tables found for this restaurant",
        },
    )
    @jwt_required()
    @roles_required(enums.UserRole.STAFF, enums.UserRole.CUSTOMER, api=api)
    def get(self, restaurant_id):
        return RestaurantService.get_tables_by_restaurant_id(restaurant_id)


@api.route("/<int:table_id>")
class UpdateDeleteTable(Resource):
    @api.expect(restx_validation.update_table_model, validate=True)
    @api.doc(
        security="Bearer Auth",
        responses={
            200: "Table updated",
            401: "Missing Authorization Header",
            403: "Access denied",
            404: "Table not found or not authorized",
        },
    )
    @jwt_required()
    @roles_required(enums.UserRole.STAFF, api=api)
    def put(self, table_id):
        data = api.payload
        user_id = get_jwt_identity()
        return RestaurantService.update_table(table_id, data, user_id)

    @api.doc(
        security="Bearer Auth",
        responses={
            200: "Table deleted",
            401: "Missing Authorization Header",
            403: "Access denied",
            404: "Table not found or not authorized",
        },
    )
    @jwt_required()
    @roles_required(enums.UserRole.STAFF, api=api)
    def delete(self, table_id):
        user_id = get_jwt_identity()
        return RestaurantService.delete_table(table_id, user_id)

    # @api.doc(
    #     security="Bearer Auth",
    #     responses={
    #         200: "Success",
    #         401: "Missing Authorization Header",
    #         403: "Access denied",
    #         404: "Table not found or not authorized",
    #     },
    # )
    # @jwt_required()
    # def get(self, id):
    #     table = TableService.get(id)
    #     if not table or table.restaurant.staff_user_id != get_jwt_identity():
    #         return {"msg": "Table not found or not authorized"}, 404
    #     return table.to_dict(), 200
