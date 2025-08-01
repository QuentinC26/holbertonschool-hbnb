from flask import Flask
from app.extensions import db, bcrypt, jwt
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

from app.api.v1 import api_v1_bp
from app.persistence.repository import storage  # L'instance de stockage (DB)
from config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Init extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    CORS(app)

    # Register blueprints
    app.register_blueprint(api_v1_bp, url_prefix='/api/v1')

    # Close DB connection after each request
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        storage.close()

    return app
