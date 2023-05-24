from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash

from ..services import UserService
from ..utils.validations import update_user_validator
from ..utils.decorators import roles_required
from .. import enums

user_bp = Blueprint('user', __name__, url_prefix='/user')


@user_bp.route('/profile', methods=['GET'])
@jwt_required
def profile():
    user_id = get_jwt_identity()
    user = UserService.get_user_by_id(user_id)

    if user:
        return jsonify({
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "phone": user.phone,
            "role": user.role
        }), 200
    else:
        return jsonify({"msg": "User not found"}), 404


@user_bp.route('/update', methods=['POST'])
@jwt_required
# @validate_json_input(update_user_validator)
def update(data):
    user_id = get_jwt_identity()

    # Hash the password if it's being updated.
    if 'password' in data:
        hashed_password = generate_password_hash(data['password'], method='sha256')
        data['password'] = hashed_password

    result = UserService.update_user(user_id, data)

    if result:
        return jsonify({"msg": "User updated successfully"}), 200
    else:
        return jsonify({"msg": "User update failed"}), 500



@user_bp.route('/delete', methods=['DELETE'])
@jwt_required
@roles_required(enums.UserRole.ADMIN)
def delete():
    user_id = get_jwt_identity()

    result = UserService.delete_user(user_id)

    if result:
        return jsonify({"msg": "User deleted successfully"}), 200
    else:
        return jsonify({"msg": "User deletion failed"}), 500
