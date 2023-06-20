import os
from dotenv import load_dotenv
import secrets

load_dotenv()

FLASK_ENV = os.getenv("FLASK_ENV") or "production"


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv("SECRET_KEY") or secrets.token_hex(32)
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SWAGGER_UI_USERNAME = os.getenv("SWAGGER_UI_USERNAME") or secrets.token_hex(32)
    SWAGGER_UI_PASSWORD = os.getenv("SWAGGER_UI_PASSWORD") or secrets.token_hex(32)


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///development.db"


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///testing.db"
