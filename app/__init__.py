from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

hostname = "hesapp.cmozq5eq2b1s.eu-north-1.rds.amazonaws.com"
port = 5432
username = "postgresql"
password = "F7gH9#2kL4"
database = "postgres"

app = Flask(__name__)
app.config.from_object(Config)
# app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
# app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgresql:F7gH9#2kL4@hesapp.cmozq5eq2b1s.eu-north-1.rds.amazonaws.com:5432/postgres'
db = SQLAlchemy(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)

# Import and register blueprints
from .routes import auth_routes, user_routes
app.register_blueprint(auth_routes.auth_bp)
# app.register_blueprint(user_routes.user_bp)
