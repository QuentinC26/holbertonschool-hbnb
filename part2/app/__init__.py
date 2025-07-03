from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restx import Api
from app.api.v1.users import api as users_ns
from app.api.v1.places import api as place_ns
from app.api.v1.amenities import api as amenity_ns


import config

jwt = JWTManager()

def create_app(config_class=config.DevelopmentConfig):
    app = Flask(__name__)
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/')
    app.config.from_object(config_class)
    jwt.init_app(app)

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(place_ns, path='/api/v1/places')
    api.add_namespace(amenity_ns, path='/api/v1/amenities')
    api.add_namespace(review_ns, path='/api/v1/reviews')
    return app
