from flask_restx import Api
from flask import Blueprint
from .auth import api as auth_api
from .users import api as users_api
from .places import api as places_api
from .amenities import api as amenities_api
from .reviews import api as reviews_api

bp = Blueprint('api', name, url_prefix='/api/v1')
api = Api(bp, version='1.0', title='HBnB API', description='HBnB REST API')

api.add_namespace(auth_api, path='/auth')
api.add_namespace(users_api, path='/users')
api.add_namespace(places_api, path='/places')
api.add_namespace(amenities_api, path='/amenities')
api.add_namespace(reviews_api, path='/reviews')