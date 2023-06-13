from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity
from functools import wraps
from ..services import UserService


def roles_required(*roles, api):
    def decorator(f):
        @wraps(f)
        @api.doc(
            responses={
                403: "Access denied",
                500: "Internal Server Error",
            }
        )
        def wrapper(*args, **kwargs):
            user_id = get_jwt_identity(optional=True)
            if not user_id:
                return {"message": "Missing Authorization Header"}, 401
            user_role = UserService.get_role(user_id)
            if not user_role or user_role not in roles:
                return {"msg": "Access denied"}, 403
            return f(*args, **kwargs)

        return wrapper

    return decorator
