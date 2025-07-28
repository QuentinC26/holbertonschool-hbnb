from flask_restx import Api
from flask import Blueprint

api_bp = Blueprint('api', __name__, url_prefix='/api')

api = Api(api_bp, title="HBnB API", version="1.0", description="HBnB API")

# Import namespaces depuis le dossier v1 (version 1 de l'API)
from .v1 import users, places, amenities, reviews, auth

api.add_namespace(users.api)
api.add_namespace(places.api)
api.add_namespace(amenities.api)
api.add_namespace(reviews.api)
api.add_namespace(auth.api)

# Enregistrement des blueprints enfants dans le blueprint parent
api_bp.register_blueprint(users.api)
api_bp.register_blueprint(places.api)
api_bp.register_blueprint(amenities.api)
api_bp.register_blueprint(reviews.api)
api_bp.register_blueprint(auth.api)