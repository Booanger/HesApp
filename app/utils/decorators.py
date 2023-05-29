from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity
from functools import wraps
from ..services import UserService

def roles_required(*roles, api):
    def decorator(f):
        @wraps(f)
        @api.doc(responses={
            403: 'Access denied'
        })
        def wrapper(*args, **kwargs):
            user_id = get_jwt_identity()
            user = UserService.get_user_by_id(user_id)
            if not user or user.role not in roles:
                return jsonify({"msg": "Access denied"}), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator

"""
def validate_json_input(schema):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not request.is_json:
                return jsonify({"msg": "Missing JSON in request"}), 400

            data = request.get_json()
            if not schema.validate(data):
                return jsonify({"msg": "Bad request parameters", "errors": schema.errors}), 400

            return func(data, *args, **kwargs)

        return wrapper

    return decorator
"""

def validate_json_input(validator, api):
    def decorator(f):
        @wraps(f)
        @api.doc(responses={
            400: 'Missing JSON in request / Missing JSON data / Bad Request'
        })
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                return jsonify({"msg": "Missing JSON in request"}), 400

            data = request.get_json()
            if not data:
                return jsonify({"msg": "Missing JSON data"}), 400

            if not validator.validate(data):
                return jsonify({"msg": "Bad Request", "errors": validator.errors}), 400

            kwargs['data'] = data
            return f(*args, **kwargs)
        return decorated_function
    return decorator
