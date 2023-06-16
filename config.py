import os
from dotenv import load_dotenv
import secrets

load_dotenv()


class Config(object):
    SECRET_KEY = os.getenv("SECRET_KEY") or secrets.token_hex(32)
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SWAGGER_UI_USERNAME = os.getenv("SWAGGER_UI_USERNAME") or secrets.token_hex(32)
    SWAGGER_UI_PASSWORD = os.getenv("SWAGGER_UI_PASSWORD") or secrets.token_hex(32)
