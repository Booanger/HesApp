from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource
from ..services import QRCodeService
from ..utils.validations import RestxValidation
from ..utils.decorators import roles_required
from .. import enums

api = Namespace("qr", description="QR code related operations")

restx_validation = RestxValidation(api=api)


@api.route("/table/<int:table_id>")
class GetTableAndRestaurantID(Resource):
    @api.doc(
        security="Bearer Auth",
        responses={
            200: "Success",
            401: "Missing Authorization Header",
            404: "Table not found",
            500: "Internal Server Error",
        },
    )
    @jwt_required()
    def get(self, table_id):
        return QRCodeService.get_table_id_and_restaurant_id(table_id)
