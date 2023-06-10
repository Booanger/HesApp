from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash
from flask_restx import Namespace, Resource

from ..services import UserService
from ..utils.validations import RestxValidation
from ..utils.decorators import roles_required
from .. import enums

api = Namespace('user', description='User related operations')

restx_validation = RestxValidation(api=api)

@api.route('/profile')
class Profile(Resource):
    @api.doc(security='Bearer Auth',
             responses={
                200: 'Success',
                401: 'Missing Authorization Header',
                404: 'User not found'
             })
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = UserService.get(user_id)

        if user:
            return user.to_dict(), 200
        else:
            return {"msg": "User not found"}, 404


@api.route('/update')
class UpdateUser(Resource):
    @api.doc(security='Bearer Auth',
             responses={
                 200: 'Success',
                 401: 'Missing Authorization Header',
                 500: 'User update failed'
             })
    @api.expect(restx_validation.update_user_model, validate=True)
    @jwt_required()
    def put(self):
        data = api.payload
        user_id = get_jwt_identity()

        # Hash the password if it's being updated.
        if 'password' in data:
            hashed_password = generate_password_hash(data['password'], method='sha256')
            data['password'] = hashed_password

        result = UserService.update(user_id, data)

        if result:
            return {"msg": "User updated successfully"}, 200
        else:
            return {"msg": "User update failed"}, 500


@api.route('/delete')
class DeleteUser(Resource):
    @api.doc(security='Bearer Auth',
             responses={
                 200: 'Success',
                 401: 'Missing Authorization Header',
                 500: 'User deletion failed',
                 404: 'User not found'
             })
    @jwt_required()
    @roles_required(enums.UserRole.ADMIN, api=api)
    def delete(self):
        user_id = get_jwt_identity()

        result = UserService.delete(user_id)

        if result:
            return {"msg": "User deleted successfully"}, 200
        else:
            return {"msg": "User deletion failed"}, 500
