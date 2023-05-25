from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)

# Import and register blueprints
from .routes import auth_routes, user_routes, restaurant_routes, menu_routes
app.register_blueprint(auth_routes.auth_bp)
app.register_blueprint(user_routes.user_bp)
app.register_blueprint(restaurant_routes.restaurant_bp)
app.register_blueprint(menu_routes.menu_bp)
