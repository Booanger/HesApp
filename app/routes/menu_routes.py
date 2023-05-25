from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..services import MenuService, RestaurantService
from ..utils.validations import (create_menu_category_validator,
                                 create_menu_item_validator,
                                 update_menu_category_validator,
                                 update_menu_item_validator)
from ..utils.decorators import roles_required, validate_json_input
from .. import enums

menu_bp = Blueprint('menu', __name__, url_prefix='/menu')

@menu_bp.route('/category', methods=['POST'])
@jwt_required()
@roles_required(enums.UserRole.STAFF)
@validate_json_input(create_menu_category_validator)
def create_menu_category(data):
    user_id = get_jwt_identity()
    restaurant = RestaurantService.get_restaurant_by_staff_user_id(user_id)
    if not restaurant:
        return jsonify({"msg": "Restaurant not found"}), 404

    data['restaurant_id'] = restaurant.id
    new_category = MenuService.create_category(data)
    return jsonify(new_category.to_dict()), 201

@menu_bp.route('/item', methods=['POST'])
@jwt_required()
@roles_required(enums.UserRole.STAFF)
@validate_json_input(create_menu_item_validator)
def create_menu_item(data):
    category = MenuService.get_category(data['category_id'])
    if not category or category.restaurant.staff_user_id != get_jwt_identity():
        return jsonify({"msg": "Category not found or not authorized"}), 404

    new_item = MenuService.create_item(data)
    return jsonify(new_item.to_dict()), 201

@menu_bp.route('/categories/<int:restaurant_id>', methods=['GET'])
@jwt_required()
@roles_required(enums.UserRole.STAFF, enums.UserRole.CUSTOMER)
def get_categories_by_restaurant(restaurant_id):
    categories = MenuService.get_categories_by_restaurant_id(restaurant_id)
    if categories is None or len(categories) == 0:
        return jsonify({"msg": "No categories found for this restaurant"}), 404
    return jsonify([category.to_dict() for category in categories]), 200

@menu_bp.route('/items/<int:category_id>', methods=['GET'])
@jwt_required()
@roles_required(enums.UserRole.STAFF, enums.UserRole.CUSTOMER)
def get_items_by_category(category_id):
    items = MenuService.get_items_by_category_id(category_id)
    if items is None or len(items) == 0:
        return jsonify({"msg": "No items found for this category"}), 404
    return jsonify([item.to_dict() for item in items]), 200

@menu_bp.route('/category/<int:id>', methods=['PUT'])
@jwt_required()
@roles_required(enums.UserRole.STAFF)
@validate_json_input(update_menu_category_validator)
def update_menu_category(id, data):
    category = MenuService.get_category(id)
    if not category or category.restaurant.staff_user_id != get_jwt_identity():
        return jsonify({"msg": "Category not found or not authorized"}), 404

    data['restaurant_id'] = category.restaurant_id

    updated_category = MenuService.update_category(id, data)
    return jsonify(updated_category.to_dict()), 200

@menu_bp.route('/item/<int:id>', methods=['PUT'])
@jwt_required()
@roles_required(enums.UserRole.STAFF)
@validate_json_input(update_menu_item_validator)
def update_menu_item(id, data):
    item = MenuService.get_item(id)
    if not item or item.category.restaurant.staff_user_id != get_jwt_identity():
        return jsonify({"msg": "Item not found or not authorized"}), 404

    # Ensure category_id is not from another restaurant
    new_category_id = data.get('category_id')
    new_category = new_category_id and MenuService.get_category(new_category_id)
    if new_category and new_category.restaurant.staff_user_id != get_jwt_identity():
        return jsonify({"msg": "Can't update to an unauthorized category"}), 403

    updated_item = MenuService.update_item(id, data)
    return jsonify(updated_item.to_dict()), 200


@menu_bp.route('/category/<int:id>', methods=['DELETE'])
@jwt_required()
@roles_required(enums.UserRole.STAFF)
def delete_menu_category(id):
    category = MenuService.get_category(id)
    if not category or category.restaurant.staff_user_id != get_jwt_identity():
        return jsonify({"msg": "Category not found or not authorized"}), 404

    MenuService.delete_category(id)
    return jsonify({"msg": "Category deleted"}), 200

@menu_bp.route('/item/<int:id>', methods=['DELETE'])
@jwt_required()
@roles_required(enums.UserRole.STAFF)
def delete_menu_item(id):
    item = MenuService.get_item(id)
    if not item or item.category.restaurant.staff_user_id != get_jwt_identity():
        return jsonify({"msg": "Item not found or not authorized"}), 404

    MenuService.delete_item(id)
    return jsonify({"msg": "Item deleted"}), 200
