from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
from flask_restx import Api

from .models import db
from .routes import auth_routes, user_routes, restaurant_routes, menu_routes, table_routes

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
db.init_app(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)

api = Api(
    app,
    version='1.0',
    title='HesApp API',
    description='A simple demonstration of a Flask RestPlus powered API',
    authorizations={
        'Bearer Auth': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    }
)

api.add_namespace(auth_routes.api, path="/auth")
api.add_namespace(user_routes.api, path="/user")
api.add_namespace(restaurant_routes.api, path="/restaurant")
api.add_namespace(menu_routes.api, path="/menu")
api.add_namespace(table_routes.api, path="/table")