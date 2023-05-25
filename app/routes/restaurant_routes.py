from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..services import RestaurantService
from ..utils.validations import restaurant_update_validator
from ..utils.decorators import roles_required, validate_json_input
from .. import enums

restaurant_bp = Blueprint('restaurant', __name__, url_prefix='/restaurant')

@restaurant_bp.route('/', methods=['GET'])
def get_all():
    restaurants = RestaurantService.get_restaurants()
    return jsonify([restaurant.to_dict() for restaurant in restaurants]), 200

@restaurant_bp.route('/<int:id>', methods=['GET'])
def get_by_id(id):
    restaurant = RestaurantService.get_restaurant(id)
    if restaurant:
        return jsonify(restaurant.to_dict()), 200
    else:
        return jsonify({"msg": "Restaurant not found"}), 404

@restaurant_bp.route('/update', methods=['PUT'])
@jwt_required()
@roles_required(enums.UserRole.STAFF)
@validate_json_input(restaurant_update_validator)
def update_restaurant(data):
    user_id = get_jwt_identity()
    restaurant = RestaurantService.get_restaurant_by_staff_user_id(user_id)
    if not restaurant:
        return jsonify({"msg": "Restaurant not found"}), 404

    result = RestaurantService.update_restaurant(restaurant.id, data)

    if result:
        return jsonify({"msg": "Restaurant updated successfully"}), 200
    else:
        return jsonify({"msg": "Restaurant update failed"}), 500
