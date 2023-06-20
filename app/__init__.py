from flask import Flask, request, Response
from werkzeug.security import check_password_hash, generate_password_hash
from config import FLASK_ENV, DevelopmentConfig, ProductionConfig, TestingConfig
from flask_jwt_extended import JWTManager
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
    order_routes,
    # payment_routes,
    qr_code_routes,
)


def create_app():
    app = Flask(__name__)
    if FLASK_ENV == "development":
        app.config.from_object(DevelopmentConfig)
    elif FLASK_ENV == "testing":
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(ProductionConfig)
    CORS(app)
    db.init_app(app)
    jwt = JWTManager(app)
    migrate = Migrate(app, db)

    # Swagger UI authentication
    username = app.config["SWAGGER_UI_USERNAME"]
    hashed_password = generate_password_hash(app.config["SWAGGER_UI_PASSWORD"])

    @app.before_request
    def require_login():
        if request.path == "/":
            auth = request.authorization
            if not auth or not auth.username or not auth.password:
                return Response(
                    "Login required",
                    401,
                    {"WWW-Authenticate": 'Basic realm="Login required"'},
                )
            elif auth.username != username or not check_password_hash(
                hashed_password, auth.password
            ):
                return Response(
                    "Invalid credentials",
                    401,
                    {"WWW-Authenticate": 'Basic realm="Login required"'},
                )

    api = Api(
        app,
        version="1.0",
        title="HesApp API",
        description="A simple demonstration of a Flask RestPlus powered API",
        authorizations={
            "Bearer Auth": {"type": "apiKey", "in": "header", "name": "Authorization"}
        },
    )

    api.add_namespace(auth_routes.api, path="/auth")
    api.add_namespace(customer_routes.api, path="/customer")
    api.add_namespace(staff_routes.api, path="/staff")
    api.add_namespace(menu_routes.api, path="/menu")
    api.add_namespace(table_routes.api, path="/table")
    api.add_namespace(order_routes.api, path="/order")
    # api.add_namespace(payment_routes.api, path="/payment")
    api.add_namespace(qr_code_routes.api, path="/qr")

    return app
