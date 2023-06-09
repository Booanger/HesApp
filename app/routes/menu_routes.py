from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource

from ..services import MenuService, RestaurantService
from ..utils.validations import RestxValidation, create_menu_category_validator, create_menu_item_validator, update_menu_category_validator, update_menu_item_validator
from ..utils.decorators import roles_required, validate_json_input
from .. import enums

api = Namespace('menu', description='Menu related operations')

restx_validation = RestxValidation(api=api)

@api.route('/category')
class CreateMenuCategory(Resource):
    @api.expect(restx_validation.create_menu_category_model)
    @api.doc(security='Bearer Auth',
             responses={
                 201: 'Category created',
                 401: 'Missing Authorization Header',
                 403: 'Access denied',
                 409: 'Category already exists'
             })
    @jwt_required()
    @roles_required(enums.UserRole.STAFF, api=api)
    @validate_json_input(create_menu_category_validator, api)
    def post(self, data):
        user_id = get_jwt_identity()
        restaurant = RestaurantService.get_restaurant_by_staff_user_id(user_id)
        if not restaurant:
            return jsonify({"msg": "Restaurant not found"}), 404

        existing_category = MenuService.get_category_by_name(restaurant.id, data['name'])
        if existing_category:
            return jsonify({"msg": "Category already exists"}), 409

        data['restaurant_id'] = restaurant.id
        new_category = MenuService.create_category(data)
        return new_category.to_dict(), 201

@api.route('/item')
class CreateMenuItem(Resource):
    @api.expect(restx_validation.create_menu_item_model)
    @api.doc(security='Bearer Auth',
             responses={
                 201: 'Item created',
                 401: 'Missing Authorization Header',
                 403: 'Access denied',
                 404: 'Category not found or not authorized'
             })
    @jwt_required()
    @roles_required(enums.UserRole.STAFF, api=api)
    @validate_json_input(create_menu_item_validator, api)
    def post(self, data):
        category = MenuService.get_category(data['category_id'])
        if not category or category.restaurant.staff_user_id != get_jwt_identity():
            return jsonify({"msg": "Category not found or not authorized"}), 404

        new_item = MenuService.create_item(data)
        return new_item.to_dict(), 201

@api.route('/categories/<int:restaurant_id>')
class GetCategoriesByRestaurant(Resource):
    @api.doc(security='Bearer Auth',
             responses={
                 200: 'Success',
                 401: 'Missing Authorization Header',
                 403: 'Access denied',
                 404: 'No categories found for this restaurant'
             })
    @jwt_required()
    @roles_required(enums.UserRole.STAFF, enums.UserRole.CUSTOMER, api=api)
    def get(self, restaurant_id):
        categories = MenuService.get_categories_by_restaurant_id(restaurant_id)
        if categories is None or len(categories) == 0:
            return jsonify({"msg": "No categories found for this restaurant"}), 404
        return [category.to_dict() for category in categories], 200

@api.route('/items/<int:category_id>')
class GetItemsByCategory(Resource):
    @api.doc(security='Bearer Auth',
             responses={
                 200: 'Success',
                 401: 'Missing Authorization Header',
                 403: 'Access denied',
                 404: 'No items found for this category'
             })
    @jwt_required()
    @roles_required(enums.UserRole.STAFF, enums.UserRole.CUSTOMER, api=api)
    def get(self, category_id):
        items = MenuService.get_items_by_category_id(category_id)
        if items is None or len(items) == 0:
            return jsonify({"msg": "No items found for this category"}), 404
        return [item.to_dict() for item in items], 200

@api.route('/category/<int:id>')
class UpdateMenuCategory(Resource):
    @api.expect(restx_validation.update_menu_category_model)
    @api.doc(security='Bearer Auth',
             responses={
                 200: 'Category updated',
                 401: 'Missing Authorization Header',
                 403: 'Access denied',
                 404: 'Category not found or not authorized'
             })
    @jwt_required()
    @roles_required(enums.UserRole.STAFF, api=api)
    @validate_json_input(update_menu_category_validator, api)
    def put(self, id, data):
        category = MenuService.get_category(id)
        if not category or category.restaurant.staff_user_id != get_jwt_identity():
            return jsonify({"msg": "Category not found or not authorized"}), 404

        data['restaurant_id'] = category.restaurant_id

        updated_category = MenuService.update_category(id, data)
        return updated_category.to_dict(), 200

@api.route('/item/<int:id>')
class UpdateMenuItem(Resource):
    @api.expect(restx_validation.update_menu_item_model)
    @api.doc(security='Bearer Auth',
             responses={
                 200: 'Item updated',
                 401: 'Missing Authorization Header',
                 403: 'Access denied',
                 404: 'Item not found or not authorized'
             })
    @jwt_required()
    @roles_required(enums.UserRole.STAFF, api=api)
    @validate_json_input(update_menu_item_validator, api)
    def put(self, id, data):
        item = MenuService.get_item(id)
        if not item or item.category.restaurant.staff_user_id != get_jwt_identity():
            return jsonify({"msg": "Item not found or not authorized"}), 404

        # Ensure category_id is not from another restaurant
        new_category_id = data.get('category_id')
        new_category = new_category_id and MenuService.get_category(new_category_id)
        if new_category and new_category.restaurant.staff_user_id != get_jwt_identity():
            return jsonify({"msg": "Can't update to an unauthorized category"}), 403

        updated_item = MenuService.update_item(id, data)
        return updated_item.to_dict(), 200

@api.route('/category/<int:id>')
class DeleteMenuCategory(Resource):
    @api.doc(security='Bearer Auth',
             responses={
                 200: 'Category deleted',
                 401: 'Missing Authorization Header',
                 403: 'Access denied',
                 404: 'Category not found or not authorized'
             })
    @jwt_required()
    @roles_required(enums.UserRole.STAFF, api=api)
    def delete(self, id):
        category = MenuService.get_category(id)
        if not category or category.restaurant.staff_user_id != get_jwt_identity():
            return jsonify({"msg": "Category not found or not authorized"}), 404

        MenuService.delete_category(id)
        return jsonify({"msg": "Category deleted"}), 200

@api.route('/item/<int:id>')
class DeleteMenuItem(Resource):
    @api.doc(security='Bearer Auth',
             responses={
                 200: 'Item deleted',
                 401: 'Missing Authorization Header',
                 403: 'Access denied',
                 404: 'Item not found or not authorized'
             })
    @jwt_required()
    @roles_required(enums.UserRole.STAFF, api=api)
    def delete(self, id):
        item = MenuService.get_item(id)
        if not item or item.category.restaurant.staff_user_id != get_jwt_identity():
            return jsonify({"msg": "Item not found or not authorized"}), 404

        MenuService.delete_item(id)
        return jsonify({"msg": "Item deleted"}), 200
