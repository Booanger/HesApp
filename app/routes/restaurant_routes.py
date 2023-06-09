from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource

from ..services import RestaurantService
from ..utils.validations import RestxValidation, restaurant_update_validator
from ..utils.decorators import roles_required, validate_json_input
from .. import enums

api = Namespace('restaurant', description='Restaurant related operations')

restx_validation = RestxValidation(api=api)

@api.route('/')
class GetAllRestaurants(Resource):
    @api.doc(responses={
        200: 'Success'
    })
    def get(self):
        restaurants = RestaurantService.get_restaurants()
        return ([restaurant.to_dict() for restaurant in restaurants]), 200

@api.route('/<int:id>')
class GetRestaurantById(Resource):
    @api.doc(responses={
        200: 'Success',
        404: 'Restaurant not found'
    })
    def get(self, id):
        restaurant = RestaurantService.get_restaurant(id)
        if restaurant:
            return restaurant.to_dict(), 200
        else:
            return jsonify({"msg": "Restaurant not found"}), 404

@api.route('/update')
class UpdateRestaurant(Resource):
    @api.expect(restx_validation.restaurant_update_model)
    @api.doc(security='Bearer Auth',
             responses={
                 200: 'Restaurant updated',
                 401: 'Missing Authorization Header',
                 403: 'Access denied',
                 404: 'Restaurant not found'
             })
    @jwt_required()
    @roles_required(enums.UserRole.STAFF, api=api)
    @validate_json_input(restaurant_update_validator, api)
    def put(self, data):
        user_id = get_jwt_identity()
        restaurant = RestaurantService.get_restaurant_by_staff_user_id(user_id)
        if not restaurant:
            return jsonify({"msg": "Restaurant not found"}), 404

        result = RestaurantService.update_restaurant(restaurant.id, data)

        if result:
            return jsonify({"msg": "Restaurant updated successfully"}), 200
        else:
            return jsonify({"msg": "Restaurant update failed"}), 500
