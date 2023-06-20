from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from functools import wraps
from flask_restx import Namespace

from ..services import UserService
from ..enums import UserRole


def roles_required(*roles: UserRole, api: Namespace):
    def decorator(f):
        @wraps(f)
        @api.doc(
            responses={
                403: "Access denied",
                500: "Internal Server Error",
            }
        )
        def wrapper(*args, **kwargs):
            try:
                user_id = get_jwt_identity()
                user_role = UserService.get_role(user_id)
                if not user_role or user_role not in roles:
                    return {"msg": "Access denied"}, 403
                return f(*args, **kwargs)
            except Exception as e:
                # Log the error for debugging purposes
                print(f"An error occurred: {e}")
                # Return a meaningful error response
                return jsonify(error=e), 400

        return wrapper

    return decorator
