from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from flask import request
from app.services import facade

api = Namespace('auth', description='Authentication operations')

# Model for input validation
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        """Authenticate user and return a JWT token"""
        try:
            credentials = api.payload or request.get_json()
            if not credentials or 'email' not in credentials or 'password' not in credentials:
                return {'error': 'Missing email or password'}, 400

            user = facade.get_user_by_email(credentials['email'])

            if not user or not user.verify_password(credentials['password']):
                return {'error': 'Invalid credentials'}, 401

            access_token = create_access_token(identity={
                'id': str(user.id),
                'is_admin': bool(user.is_admin)
            })

            return {'access_token': access_token}, 200

        except Exception as e:
            # Log the error if needed: print(e) or use logger
            return {'error': f'Internal server error: {str(e)}'}, 500
