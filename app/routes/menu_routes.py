from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource

from ..services import MenuCategoryService, MenuItemService, RestaurantService
from ..utils.validations import RestxValidation
from ..utils.decorators import roles_required
from .. import enums

api = Namespace('menu', description='Menu related operations')

restx_validation = RestxValidation(api=api)

@api.route('/category')
class CreateMenuCategory(Resource):
    @api.expect(restx_validation.create_menu_category_model, validate=True)
    @api.doc(security='Bearer Auth',
             responses={
                 200: 'Category created',
                 401: 'Missing Authorization Header',
                 403: 'Access denied',
                 409: 'Category already exists'
             })
    @jwt_required()
    @roles_required(enums.UserRole.STAFF, api=api)
    def post(self):
        data = api.payload
        user_id = get_jwt_identity()
        restaurant = RestaurantService.get_by_staff_user_id(user_id)
        if not restaurant:
            return {"msg": "Restaurant not found"}, 404

        data['restaurant_id'] = restaurant.id
        new_category = MenuCategoryService.create(data)
        return new_category.to_dict(), 200

@api.route('/item')
class CreateMenuItem(Resource):
    @api.expect(restx_validation.create_menu_item_model, validate=True)
    @api.doc(security='Bearer Auth',
             responses={
                 200: 'Item created',
                 401: 'Missing Authorization Header',
                 403: 'Access denied',
                 404: 'Category not found or not authorized'
             })
    @jwt_required()
    @roles_required(enums.UserRole.STAFF, api=api)
    def post(self):
        data = api.payload
        category = MenuCategoryService.get(data['category_id'])
        if not category or category.restaurant.staff_user_id != get_jwt_identity():
            return {"msg": "Category not found or not authorized"}, 404

        new_item = MenuItemService.create(data)
        return new_item.to_dict(), 200

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
        categories = MenuCategoryService.get_all_by_restaurant_id(restaurant_id)
        if categories is None or len(categories) == 0:
            return {"msg": "No categories found for this restaurant"}, 404
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
        items = MenuItemService.get_all_by_category_id(category_id)
        if items is None or len(items) == 0:
            return {"msg": "No items found for this category"}, 404
        return [item.to_dict() for item in items], 200

@api.route('/category/<int:id>')
class UpdateMenuCategory(Resource):
    @api.expect(restx_validation.update_menu_category_model, validate=True)
    @api.doc(security='Bearer Auth',
             responses={
                 200: 'Category updated',
                 401: 'Missing Authorization Header',
                 403: 'Access denied',
                 404: 'Category not found or not authorized'
             })
    @jwt_required()
    @roles_required(enums.UserRole.STAFF, api=api)
    def put(self, id):
        data = api.payload
        category = MenuCategoryService.get(id)
        if not category or category.restaurant.staff_user_id != get_jwt_identity():
            return {"msg": "Category not found or not authorized"}, 404

        data['restaurant_id'] = category.restaurant_id

        updated_category = MenuCategoryService.update(id, data)
        return updated_category.to_dict(), 200

@api.route('/item/<int:id>')
class UpdateMenuItem(Resource):
    @api.expect(restx_validation.update_menu_item_model, validate=True)
    @api.doc(security='Bearer Auth',
             responses={
                 200: 'Item updated',
                 401: 'Missing Authorization Header',
                 403: 'Access denied',
                 404: 'Item not found or not authorized'
             })
    @jwt_required()
    @roles_required(enums.UserRole.STAFF, api=api)
    def put(self, id):
        data = api.payload
        item = MenuItemService.get(id)
        if not item or item.category.restaurant.staff_user_id != get_jwt_identity():
            return {"msg": "Item not found or not authorized"}, 404

        # Ensure category_id is not from another restaurant
        new_category_id = data.get('category_id')
        new_category = new_category_id and MenuCategoryService.get(new_category_id)
        if new_category and new_category.restaurant.staff_user_id != get_jwt_identity():
            return {"msg": "Can't update to an unauthorized category"}, 403

        updated_item = MenuItemService.update(id, data)
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
        category = MenuCategoryService.get(id)
        if not category or category.restaurant.staff_user_id != get_jwt_identity():
            return {"msg": "Category not found or not authorized"}, 404

        MenuCategoryService.delete(id)
        return {"msg": "Category deleted"}, 200

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
        item = MenuItemService.get(id)
        if not item or item.category.restaurant.staff_user_id != get_jwt_identity():
            return {"msg": "Item not found or not authorized"}, 404

        MenuItemService.delete(id)
        return {"msg": "Item deleted"}, 200
