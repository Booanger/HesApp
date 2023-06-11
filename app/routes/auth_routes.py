from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash, generate_password_hash
from flask_restx import Namespace, Resource
from datetime import timedelta

from ..services import UserService, RestaurantService
from ..utils.validations import RestxValidation
from .. import enums


api = Namespace('auth', description='Authentication related operations')

restx_validation = RestxValidation(api=api)

@api.route('/login')
class Login(Resource):
    @api.expect(restx_validation.login_model, validate=True)
    @api.doc(responses={
        200: 'Success',
        404: 'User not found',
        401: 'Bad username or password',
        400: "Bad Request",
        500: "Internal Server Error"
    })
    def post(self):
        data = api.payload
        user = UserService.get_by_email(data['email'])
        if not user:
            return {"msg": "User not found"}, 404

        if not check_password_hash(user.password, data['password']):
            return {"msg": "Bad username or password"}, 401

        access_token = create_access_token(identity=user.id, expires_delta=timedelta(days=365*100))
        return {'access_token': access_token}, 200


@api.route('/register')
class Register(Resource):
    @api.expect(restx_validation.register_customer_model, validate=True)
    @api.doc(responses={
        200: 'Success',
        409: 'Email already registered',
        400: "Bad Request",
        500: "Internal Server Error"
    })
    def post(self):
        data = api.payload
        if UserService.get_by_email(data['email']):
            return {"error": "Email already registered"}, 409

        hashed_password = generate_password_hash(data['password'], method='scrypt')
        user = UserService.create(
            {
                'first_name': data['first_name'],
                'last_name': data['last_name'],
                'email': data['email'],
                'password': hashed_password,
                'phone': data['phone'],
                'role': enums.UserRole.CUSTOMER
            }
        )

        access_token = create_access_token(identity=user.id)
        return {
            "message": f"User {user.first_name} registered successfully",
            "access_token": access_token
        }, 200

@api.route('/register/staff')
class RegisterStaff(Resource):
    @api.expect(restx_validation.register_staff_model, validate=True)
    @api.doc(responses={
        200: 'Success',
        409: 'Email already registered',
        400: "Bad Request",
        500: "Internal Server Error"
    })
    def post(self):
        data = api.payload
        if UserService.get_by_email(data['email']):
            return {"error": "Email already registered"}, 409

        hashed_password = generate_password_hash(data['password'], method='scrypt')
        user = UserService.create(
            {
                'first_name': data['first_name'],
                'last_name': data['last_name'],
                'email': data['email'],
                'password': hashed_password,
                'phone': data['phone'],
                'role': enums.UserRole.STAFF
            }
        )

        # Create a restaurant
        restaurant_data = {
            'staff_user_id': user.id,
            'name': data['restaurant_name'],
            'description': data['restaurant_description'],
            'address': data['restaurant_address'],
            'phone': data['restaurant_phone'],
            'logo': data['restaurant_logo'] if 'restaurant_logo' in data else None,
        }
        restaurant = RestaurantService.create(restaurant_data)

        access_token = create_access_token(identity=user.id)
        return {
            "message": f"Staff {user.first_name} and their restaurant {restaurant.name} registered successfully",
            "access_token": access_token
        }, 200