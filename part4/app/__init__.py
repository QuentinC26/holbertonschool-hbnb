from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restx import Api
from app.api.v1.auth import api as auth_ns
from app.api.v1.users import api as users_ns
from app.api.v1.places import api as place_ns
from app.api.v1.amenities import api as amenity_ns
from app.api.v1.reviews import api as review_ns
from flask_bcrypt import Bcrypt
import config

jwt = JWTManager()
bcrypt = Bcrypt()

def create_app(config_class=config.DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/')
    jwt.init_app(app)

    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(place_ns, path='/api/v1/places')
    api.add_namespace(amenity_ns, path='/api/v1/amenities')
    api.add_namespace(review_ns, path='/api/v1/reviews')
    bcrypt.init_app(app)
    return app
