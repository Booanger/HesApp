from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash, generate_password_hash

from ..services import UserService
from ..utils.validations import register_validator, login_validator
# from ..utils.decorators import validate_json_input

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['POST'])
# @validate_json_input(login_validator)
def login():
    if not request.is_json:
        return jsonify({"msg": "Invalid Content-Type, JSON data expected"}), 400
    
    data = request.get_json()
    
    if not login_validator.validate(data):
        return jsonify({"msg": "Bad request parameters", "errors": login_validator.errors}), 400
    
    user = UserService.get_user_by_email(data['email'])
    if not user:
        return jsonify({"msg": "User not found"}), 404

    if not check_password_hash(user.password, data['password']):
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token), 200


@auth_bp.route('/register', methods=['POST'])
# validate_json_input(register_validator)
def register(data):
    if UserService.get_user_by_email(data['email']):
        return jsonify({"error": "Email already registered"}), 400

    hashed_password = generate_password_hash(data['password'], method='sha256')
    data['password'] = hashed_password
    user = UserService.create_user(data)

    access_token = create_access_token(identity=user.id)
    return jsonify({
        "message": f"User {user.first_name} registered successfully",
        "access_token": access_token
    }), 200
