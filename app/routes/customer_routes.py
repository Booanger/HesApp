from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource

from ..services import UserService
from ..utils.validations import RestxValidation
from ..utils.decorators import roles_required
from .. import enums

api = Namespace("customer", description="Customer related operations")

restx_validation = RestxValidation(api=api)


@api.route("")
class Customer(Resource):
    @api.doc(
        security="Bearer Auth",
        responses={
            200: "Success",
            401: "Missing Authorization Header",
            404: "User not found",
        },
    )
    @jwt_required()
    @roles_required(enums.UserRole.CUSTOMER, api=api)
    def get(self):
        user_id = get_jwt_identity()
        return UserService.get_customer(user_id)

    @api.doc(
        security="Bearer Auth",
        responses={
            200: "Success",
            401: "Missing Authorization Header",
            500: "User update failed",
        },
    )
    @api.expect(restx_validation.update_customer_model, validate=True)
    @jwt_required()
    @roles_required(enums.UserRole.CUSTOMER, api=api)
    def put(self):
        data = api.payload
        user_id = get_jwt_identity()

        return UserService.update_customer(user_id, data)
