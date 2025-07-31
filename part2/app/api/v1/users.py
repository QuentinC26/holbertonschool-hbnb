from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import create_access_token
from app.services.facade import HBnBFacade

api = Namespace('users', description='User operations')
facade = HBnBFacade()

user_model = api.model('User', {
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'email': fields.String(required=True),
    'password': fields.String(required=True)
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model)
    def post(self):
        """Create a new user and return access token"""
        try:
            data = request.get_json()
            user = facade.create_user(data)

            # Générer un access token dès l'inscription
            access_token = create_access_token(identity=str(user.id), additional_claims={
                "is_admin": user.is_admin
            })

            return {
                'user': user.to_dict(),
                'access_token': access_token
            }, 201

        except Exception as e:
            return {'error': str(e)}, 400

    def get(self):
        """Retrieve all users"""
        users = [u.to_dict() for u in facade.get_all_users()]
        return users, 200

@api.route('/<string:user_id>')
class UserResource(Resource):
    def get(self, user_id):
        """Retrieve a single user"""
        try:
            user = facade.get_user(user_id)
            return user.to_dict(), 200
        except Exception as e:
            return {'error': str(e)}, 404

    @api.expect(user_model)
    def put(self, user_id):
        """Update an existing user"""
        try:
            user = facade.update_user(user_id, request.get_json())
            return user.to_dict(), 200
        except Exception as e:
            return {'error': str(e)}, 400
