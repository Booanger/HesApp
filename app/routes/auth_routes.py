from flask_restx import Namespace, Resource

from ..services import UserService
from ..utils.validations import RestxValidation


api = Namespace("auth", description="Authentication related operations")

restx_validation = RestxValidation(api=api)


@api.route("/login")
class Login(Resource):
    @api.expect(restx_validation.login_model, validate=True)
    @api.doc(
        responses={
            200: "Success",
            404: "User not found",
            401: "Bad username or password",
            400: "Bad Request",
            500: "Internal Server Error",
        }
    )
    def post(self):
        data = api.payload
        return UserService.login(data["email"], data["password"])


@api.route("/register")
class Register(Resource):
    @api.expect(restx_validation.register_customer_model, validate=True)
    @api.doc(
        responses={
            200: "Success",
            409: "Username or email already registered",
            400: "Bad Request",
            500: "Internal Server Error",
        }
    )
    def post(self):
        data = api.payload
        username = data["username"]
        email = data["email"]
        password = data["password"]
        phone = data["phone"]

        return UserService.register_customer(username, email, password, phone)


@api.route("/register/staff")
class RegisterStaff(Resource):
    @api.expect(restx_validation.register_staff_model, validate=True)
    @api.doc(
        responses={
            200: "Success",
            409: "Username or email already registered",
            400: "Bad Request",
            500: "Internal Server Error",
        }
    )
    def post(self):
        data = api.payload

        username = data["username"]
        email = data["email"]
        password = data["password"]
        phone = data["phone"]
        restaurant_name = data["restaurant_name"]
        restaurant_description = data["restaurant_description"]
        restaurant_address = data["restaurant_address"]
        restaurant_phone = data["restaurant_phone"]

        return UserService.register_staff(
            username,
            email,
            password,
            phone,
            restaurant_name,
            restaurant_description,
            restaurant_address,
            restaurant_phone,
        )
