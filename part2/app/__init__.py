from flask import Flask
from flask_restx import Api
from app.api.v1.users import api as users_ns
from flask_jwt_extended import JWTManager

from config import DevelopmentConfig

jwt = JWTManager()

def create_app(config_class=config.DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    jwt.init_app(app)

    return app
