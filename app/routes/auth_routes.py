from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash, generate_password_hash
from flask_restx import Namespace, Resource
from datetime import timedelta

from ..services import UserService
from ..utils.validations import RestxValidation
from .. import enums


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
            409: "Email already registered",
            400: "Bad Request",
            500: "Internal Server Error",
        }
    )
    def post(self):
        data = api.payload
        first_name = data["first_name"]
        last_name = data["last_name"]
        email = data["email"]
        password = data["password"]
        phone = data["phone"]

        return UserService.register_customer(
            first_name, last_name, email, password, phone
        )


@api.route("/register/staff")
class RegisterStaff(Resource):
    @api.expect(restx_validation.register_staff_model, validate=True)
    @api.doc(
        responses={
            200: "Success",
            409: "Email already registered",
            400: "Bad Request",
            500: "Internal Server Error",
        }
    )
    def post(self):
        data = api.payload

        first_name = data["first_name"]
        last_name = data["last_name"]
        email = data["email"]
        password = data["password"]
        phone = data["phone"]
        restaurant_name = data["restaurant_name"]
        restaurant_description = data["restaurant_description"]
        restaurant_address = data["restaurant_address"]
        restaurant_phone = data["restaurant_phone"]
        restaurant_logo = data["restaurant_logo"]

        return UserService.register_staff(
            first_name,
            last_name,
            email,
            password,
            phone,
            restaurant_name,
            restaurant_description,
            restaurant_address,
            restaurant_phone,
            restaurant_logo,
        )
