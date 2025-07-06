from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restx import Api
from app.api.v1.users import api as users_ns
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
import config

jwt = JWTManager()
bcrypt = Bcrypt()
db = SQLAlchemy()

def create_app(config_class=config.DevelopmentConfig):
    app = Flask(__name__)
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/')
    app.config.from_object(config_class)
    jwt.init_app(app)

    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(users_ns, path='/api/v1/users')
    bcrypt.init_app(app)
    db.init_app(app)
    return app
