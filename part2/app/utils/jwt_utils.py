from flask_jwt_extended import create_access_token
from datetime import timedelta

def generate_token(identity, is_admin=False):
    additional_claims = {"is_admin": is_admin}
    return create_access_token(identity=identity, additional_claims=additional_claims, expires_delta=timedelta(days=1))
