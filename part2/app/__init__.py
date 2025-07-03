from flask import Flask
from flask_restx import Api
from app.api.v1.users import api as users_ns
from flask_bcrypt import Bcrypt
import config

bcrypt = Bcrypt()

def create_app(config_class=config.DevelopmentConfig):
    app = Flask(__name__)
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/')
    app.config.from_object(config_class)

    api.add_namespace(users_ns, path='/api/v1/users')
    bcrypt.init_app(app)
    return app
