from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource

from ..services import RestaurantService
from ..utils.validations import RestxValidation
from ..utils.decorators import roles_required
from .. import enums

api = Namespace("menu", description="Menu related operations")

restx_validation = RestxValidation(api=api)


@api.route("/category")
class CreateMenuCategory(Resource):
    @api.expect(restx_validation.create_menu_category_model, validate=True)
    @api.doc(
        security="Bearer Auth",
        responses={
            201: "Category created",
            401: "Missing Authorization Header",
            403: "Access denied",
            500: "Internal Server Error",
        },
    )
    @jwt_required()
    @roles_required(enums.UserRole.STAFF, api=api)
    def post(self):
        data = api.payload
        name = data["name"]
        user_id = get_jwt_identity()

        return RestaurantService.create_menu_category(user_id, name)


@api.route("/categories/<int:restaurant_id>")
class GetMenuCategoriesByRestaurant(Resource):
    @api.doc(
        security="Bearer Auth",
        responses={
            200: "Success",
            401: "Missing Authorization Header",
            403: "Access denied",
            500: "Internal Server Error",
        },
    )
    @jwt_required()
    @roles_required(enums.UserRole.STAFF, enums.UserRole.CUSTOMER, api=api)
    def get(self, restaurant_id):
        return RestaurantService.get_menu_categories_by_restaurant_id(restaurant_id)


@api.route("/category/<int:category_id>")
class UpdateDeleteMenuCategory(Resource):
    @api.expect(restx_validation.update_menu_category_model, validate=True)
    @api.doc(
        security="Bearer Auth",
        responses={
            200: "Category updated",
            401: "Missing Authorization Header",
            403: "Access denied",
            404: "Category not found",
            500: "Internal Server Error",
        },
    )
    @jwt_required()
    @roles_required(enums.UserRole.STAFF, api=api)
    def put(self, category_id):
        data = api.payload
        user_id = get_jwt_identity()
        return RestaurantService.update_menu_category(category_id, data, user_id)

    @api.doc(
        security="Bearer Auth",
        responses={
            204: "Category deleted",
            401: "Missing Authorization Header",
            403: "Access denied",
            404: "Category not found",
            500: "Internal Server Error",
        },
    )
    @jwt_required()
    @roles_required(enums.UserRole.STAFF, api=api)
    def delete(self, category_id):
        user_id = get_jwt_identity()
        return RestaurantService.delete_menu_category(category_id, user_id)


#######################################################################


@api.route("/item")
class CreateMenuItem(Resource):
    @api.expect(restx_validation.create_menu_item_model, validate=True)
    @api.doc(
        security="Bearer Auth",
        responses={
            201: "Item created",
            401: "Missing Authorization Header",
            403: "Access denied",
            404: "Category not found",
            500: "Internal Server Error",
        },
    )
    @jwt_required()
    @roles_required(enums.UserRole.STAFF, api=api)
    def post(self):
        data = api.payload
        category_id = data["category_id"]
        name = data["name"]
        description = data["description"]
        price = data["price"]
        image = data["image"]
        user_id = get_jwt_identity()

        return RestaurantService.create_menu_item(
            user_id, category_id, name, description, price, image
        )


@api.route("/items/<int:category_id>")
class GetItemsByCategory(Resource):
    @api.doc(
        security="Bearer Auth",
        responses={
            200: "Success",
            401: "Missing Authorization Header",
            403: "Access denied",
            500: "Internal Server Error",
        },
    )
    @jwt_required()
    @roles_required(enums.UserRole.STAFF, enums.UserRole.CUSTOMER, api=api)
    def get(self, category_id):
        return RestaurantService.get_menu_items_by_category_id(category_id)


@api.route("/item/<int:item_id>")
class UpdateDeleteMenuItem(Resource):
    @api.expect(restx_validation.update_menu_item_model, validate=True)
    @api.doc(
        security="Bearer Auth",
        responses={
            200: "Item updated",
            401: "Missing Authorization Header",
            403: "Access denied",
            404: "Item not found",
            500: "Internal Server Error",
        },
    )
    @jwt_required()
    @roles_required(enums.UserRole.STAFF, api=api)
    def put(self, item_id):
        data = api.payload
        user_id = get_jwt_identity()
        return RestaurantService.update_menu_item(item_id, data, user_id)

    @api.doc(
        security="Bearer Auth",
        responses={
            200: "Item deleted",
            401: "Missing Authorization Header",
            403: "Access denied",
            404: "Item not found or not authorized",
            500: "Internal Server Error",
        },
    )
    @jwt_required()
    @roles_required(enums.UserRole.STAFF, api=api)
    def delete(self, item_id):
        user_id = get_jwt_identity()
        return RestaurantService.delete_menu_item(item_id, user_id)
