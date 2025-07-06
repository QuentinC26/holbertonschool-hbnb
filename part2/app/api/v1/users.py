from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request

api = Namespace('admin', description='Admin operations')

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        # Simulate email uniqueness check (to be replaced by real validation with persistence)
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        new_user = facade.create_user(user_data)
        return {'id': new_user.id, 'first_name': new_user.first_name, 'last_name': new_user.last_name, 'email': new_user.email}, 201

    @api.response(200, 'OK')
    def get(self):
        users = facade.get_all_users()
        return [{'id': user.id, 'first_name': user.first_name,
            'last_name': user.last_name, 'email': user.email} for user in users], 200

@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}, 200

    @api.response(200, 'OK')
    @api.response(404, 'Not found')
    @api.response(400, 'Bad Request')
    def put(self, user_id):
        user = facade.get_user(user_id)
        if user is None:
            return {'error': 'User not found'}, 404
        else:
            user_data = api.payload
            user.first_name = user_data['first_name']
            user.last_name = user_data['last_name']
            user.email = user_data['email']
            return {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}, 200

@api.route('/users/')
class AdminUserCreate(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        user_data = request.json
        email = user_data.get('email')
        
        if facade.get_user_by_email(email):
            return {'error': 'Email already registered'}, 400

        new_user = facade.create_user(user_data)
        return {'message': 'User created', 'user': new_user.to_dict()}, 201
