from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity
from functools import wraps
from ..services import UserService

def roles_required(*roles):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user_id = get_jwt_identity()
            user = UserService.get_user_by_id(user_id)
            if not user or user.role not in roles:
                return jsonify({"msg": "Access denied"}), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator
