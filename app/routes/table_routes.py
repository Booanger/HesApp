from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource

from ..services import TableService, RestaurantService
from ..utils.validations import RestxValidation
from ..utils.decorators import roles_required
from .. import enums

api = Namespace('table', description='Table related operations')

restx_validation = RestxValidation(api=api)

@api.route('/')
class CreateTable(Resource):
    @api.expect(restx_validation.create_table_model, validate=True)
    @api.doc(security='Bearer Auth',
             responses={
                 200: 'Table created',
                 401: 'Missing Authorization Header',
                 403: 'Access denied',
                 409: 'Table already exists'
             })
    @jwt_required()
    @roles_required(enums.UserRole.STAFF, api=api)
    def post(self):
        data = api.payload
        user_id = get_jwt_identity()
        restaurant = RestaurantService.get_by_staff_user_id(user_id)
        if not restaurant:
            return {"msg": "Restaurant not found"}, 404

        data['restaurant_id'] = restaurant.id
        new_table = TableService.create(data)
        return new_table.to_dict(), 200

@api.route('/<int:id>')
class ReadUpdateDeleteTable(Resource):
    @api.expect(restx_validation.update_table_model, validate=True)
    @api.doc(security='Bearer Auth',
             responses={
                 200: 'Table updated',
                 401: 'Missing Authorization Header',
                 403: 'Access denied',
                 404: 'Table not found or not authorized'
             })
    @jwt_required()
    @roles_required(enums.UserRole.STAFF, api=api)
    def put(self, id):
        data = api.payload
        table = TableService.get(id)
        if not table or table.restaurant.staff_user_id != get_jwt_identity():
            return {"msg": "Table not found or not authorized"}, 404

        data['restaurant_id'] = table.restaurant_id

        updated_table = TableService.update(id, data)
        return updated_table.to_dict(), 200

    @api.doc(security='Bearer Auth',
             responses={
                 200: 'Table deleted',
                 401: 'Missing Authorization Header',
                 403: 'Access denied',
                 404: 'Table not found or not authorized'
             })
    @jwt_required()
    @roles_required(enums.UserRole.STAFF, api=api)
    def delete(self, id):
        table = TableService.get(id)
        if not table or table.restaurant.staff_user_id != get_jwt_identity():
            return {"msg": "Table not found or not authorized"}, 404

        TableService.delete(id)
        return {"msg": "Table deleted"}, 200

    @api.doc(security='Bearer Auth',
             responses={
                 200: 'Success',
                 401: 'Missing Authorization Header',
                 403: 'Access denied',
                 404: 'Table not found or not authorized'
             })
    @jwt_required()
    def get(self, id):
        table = TableService.get(id)
        if not table or table.restaurant.staff_user_id != get_jwt_identity():
            return {"msg": "Table not found or not authorized"}, 404
        return table.to_dict(), 200

@api.route('/restaurant/<int:restaurant_id>')
class GetTablesByRestaurant(Resource):
    @api.doc(security='Bearer Auth',
             responses={
                 200: 'Success',
                 401: 'Missing Authorization Header',
                 403: 'Access denied',
                 404: 'No tables found for this restaurant'
             })
    @jwt_required()
    def get(self, restaurant_id):
        tables = TableService.get_all_by_restaurant_id(restaurant_id)
        if tables is None or len(tables) == 0:
            return {"msg": "No tables found for this restaurant"}, 404
        return [table.to_dict() for table in tables], 200
