from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from app.api.v1 import api_v1_bp
from app.models.engine.db_storage import DBStorage  # L'instance de stockage (DB)
from config import Config

db = SQLAlchemy()
jwt = JWTManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Init extensions
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)

    # Register blueprints
    app.register_blueprint(api_v1_bp, url_prefix='/api/v1')

    # Close DB connection after each request
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        storage.close()

    return app