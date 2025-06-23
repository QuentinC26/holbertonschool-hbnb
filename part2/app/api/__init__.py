from flask_restx import Namespace, Api
from app import api 
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns 

amenities_ns = Namespace('amenities')
api.add_namespace(amenities_ns, path='/api/v1/amenities')