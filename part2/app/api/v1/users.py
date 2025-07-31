from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity
)
from app.services.facade import HBnBFacade
from app.extensions import bcrypt

api = Namespace('users', description='User operations')
facade = HBnBFacade()

user_model = api.model('User', {
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'email': fields.String(required=True),
    'password': fields.String(required=True)
})

# -------------------------
# PUBLIC ENDPOINTS
# -------------------------

@api.route('/')
class UserList(Resource):
    @api.expect(user_model)
    def post(self):
        """Register a new user and return access token"""
        try:
            data = request.get_json()
            user = facade.create_user(data)

            # Génération du token dès l'inscription
            access_token = create_access_token(identity={
                "id": user.id,
                "is_admin": user.is_admin
            })

            return {
                'user': user.to_dict(),
                'access_token': access_token
            }, 201

        except Exception as e:
            return {'error': str(e)}, 400

    def get(self):
        """Retrieve all users (admin only)"""
        current_user = get_jwt_identity()
        if not current_user or not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        users = [u.to_dict() for u in facade.get_all_users()]
        return users, 200


@api.route('/<string:user_id>')
class UserResource(Resource):
    @jwt_required()
    def get(self, user_id):
        """Retrieve a user by ID"""
        try:
            user = facade.get_user(user_id)
            return user.to_dict(), 200
        except Exception as e:
            return {'error': str(e)}, 404

    @jwt_required()
    @api.expect(user_model)
    def put(self, user_id):
        """Update a user (admin only)"""
        current_user = get_jwt_identity()
        if not current_user or not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        try:
            user = facade.update_user(user_id, request.get_json())
            return user.to_dict(), 200
        except Exception as e:
            return {'error': str(e)}, 400

# -------------------------
# ADMIN: CRÉATION PAR ADMIN
# -------------------------

@api.route('/admin')
class AdminUserCreate(Resource):
    @jwt_required()
    @api.expect(user_model)
    def post(self):
        """Admin: create new user manually"""
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        data = request.get_json()
        email = data.get('email')
        if not email:
            return {'error': 'Email is required'}, 400

        if facade.get_user_by_email(email):
            return {'error': 'Email already registered'}, 400

        user = facade.create_user(data)
        return {'message': 'User created successfully', 'user': user.to_dict()}, 201


@api.route('/admin/<string:user_id>')
class AdminUserModify(Resource):
    @jwt_required()
    def put(self, user_id):
        """Admin: update user fields"""
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        data = request.get_json()

        # Email update
        email = data.get('email')
        if email:
            existing = facade.get_user_by_email(email)
            if existing and existing.id != user.id:
                return {'error': 'Email already in use'}, 400
            user.email = email

        # Other fields
        if 'password' in data:
            user.password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']

        facade.save_user(user)
        return {'message': 'User updated', 'user': user.to_dict()}, 200
