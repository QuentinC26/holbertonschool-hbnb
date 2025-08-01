from flask_jwt_extended import verify_jwt_in_request, get_jwt
from functools import wraps
from flask import jsonify

def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except Exception as e:
            return jsonify({"error": "Missing or invalid token"}), 401
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()
            claims = get_jwt()
            if not claims.get("is_admin"):
                return jsonify({"error": "Admin access required"}), 403
        except Exception:
            return jsonify({"error": "Missing or invalid token"}), 401
        return f(*args, **kwargs)
    return decorated
