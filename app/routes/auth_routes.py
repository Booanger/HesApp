from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash, generate_password_hash

from ..services import UserService, RestaurantService
from ..utils.validations import register_customer_validator, register_staff_validator, login_validator
from ..utils.decorators import validate_json_input
from .. import enums

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['POST'])
@validate_json_input(login_validator)
def login(data):
    print(data)
    user = UserService.get_user_by_email(data['email'])
    if not user:
        return jsonify({"msg": "User not found"}), 404

    if not check_password_hash(user.password, data['password']):
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token), 200


@auth_bp.route('/register', methods=['POST'])
@validate_json_input(register_customer_validator)  # Here we use a customer-specific validator
def register(data):
    if UserService.get_user_by_email(data['email']):
        return jsonify({"error": "Email already registered"}), 400

    hashed_password = generate_password_hash(data['password'], method='scrypt')
    user = UserService.create_user(
        {
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'email': data['email'],
            'password': hashed_password,
            'phone': data['phone'],
            'role': enums.UserRole.CUSTOMER
        }
    )

    access_token = create_access_token(identity=user.id)
    return jsonify({
        "message": f"User {user.first_name} registered successfully",
        "access_token": access_token
    }), 200



@auth_bp.route('/register/staff', methods=['POST'])
@validate_json_input(register_staff_validator)  # Here we use a staff-specific validator
def register_staff(data):
    if UserService.get_user_by_email(data['email']):
        return jsonify({"error": "Email already registered"}), 400

    hashed_password = generate_password_hash(data['password'], method='scrypt')
    user = UserService.create_user(
        {
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'email': data['email'],
            'password': hashed_password,
            'phone': data['phone'],
            'role': enums.UserRole.STAFF
        }
    )

    # Create a restaurant
    restaurant_data = {
        'staff_user_id': user.id,
        'name': data['restaurant_name'],
        'description': data['restaurant_description'],
        'address': data['restaurant_address'],
        'phone': data['restaurant_phone'],
        'logo': data['restaurant_logo'] if 'restaurant_logo' in data else None,
    }
    restaurant = RestaurantService.create_restaurant(restaurant_data)

    access_token = create_access_token(identity=user.id)
    return jsonify({
        "message": f"Staff {user.first_name} and their restaurant {restaurant.name} registered successfully",
        "access_token": access_token
    }), 200