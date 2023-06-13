from flask import Flask
from config import Config
from flask_jwt_extended import JWTManager, NoAuthorizationError
from flask_migrate import Migrate
from flask_cors import CORS
from flask_restx import Api

from .models import db
from .routes import (
    auth_routes,
    customer_routes,
    staff_routes,
    menu_routes,
    table_routes,
    # order_routes,
    # payment_routes,
    # qr_code_routes,
)

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
db.init_app(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)

api = Api(
    app,
    version="1.0",
    title="HesApp API",
    description="A simple demonstration of a Flask RestPlus powered API",
    authorizations={
        "Bearer Auth": {"type": "apiKey", "in": "header", "name": "Authorization"}
    },
)

@app.errorhandler(NoAuthorizationError)
def handle_no_authorization_error(error):
    return {'message': 'Missing Authorization Header'}, 401

api.add_namespace(auth_routes.api, path="/auth")
api.add_namespace(customer_routes.api, path="/customer")
api.add_namespace(staff_routes.api, path="/staff")
api.add_namespace(menu_routes.api, path="/menu")
api.add_namespace(table_routes.api, path="/table")
# TODO add order routes
# TODO add payment routes
# TODO add qr code routes
