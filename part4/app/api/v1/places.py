from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import HBnBFacade
from app.models.user import User
from app.persistence.repository import storage

api = Namespace('places', description='Place operations')
facade = HBnBFacade()

# === Modèle Swagger sans owner_id ===
place_model = api.model('Place', {
    'title': fields.String(required=True),
    'description': fields.String,
    'price': fields.Float(required=True),
    'latitude': fields.Float(required=True),
    'longitude': fields.Float(required=True),
    'amenities': fields.List(fields.String, required=True)
})

# === POST /places/ et GET /places/ ===
@api.route('/')
class PlaceList(Resource):
    @jwt_required()
    @api.expect(place_model)
    def post(self):
        """Create a new place"""
        try:
            user_id = get_jwt_identity()
            current_user = storage.get(User, user_id)
            if not current_user:
                return {"error": "User not found"}, 404

            data = request.get_json()
            place = facade.create_place(data, current_user)
            return place.to_dict(with_owner=True, with_amenities=True), 201

        except ValueError as ve:
            return {'error': str(ve)}, 400
        except Exception as e:
            return {'error': 'Internal server error'}, 500

    def get(self):
        """Retrieve all places"""
        places = facade.get_all_places()
        return [p.to_dict(with_owner=True, with_amenities=True) for p in places], 200

# === GET /places/<id> et PUT /places/<id> ===
@api.route('/<string:place_id>')
class PlaceResource(Resource):
    def get(self, place_id):
        """Retrieve a single place with owner & amenities"""
        try:
            place = facade.get_place(place_id)
            return place.to_dict(with_owner=True, with_amenities=True), 200
        except Exception as e:
            return {'error': str(e)}, 404

    @jwt_required()
    @api.expect(place_model)
    def put(self, place_id):
        """Update an existing place (admin or owner only)"""
        try:
            identity = get_jwt_identity()
            user_id = identity.get('id') if isinstance(identity, dict) else identity
            is_admin = identity.get('is_admin', False) if isinstance(identity, dict) else False

            place = facade.get_place(place_id)
            if not place:
                return {'error': 'Place not found'}, 404

            # Vérifie autorisation
            if not is_admin and place.owner_id != user_id:
                return {'error': 'Unauthorized action'}, 403

            data = request.get_json()
            updated_place = facade.update_place(place_id, data)
            return updated_place.to_dict(with_owner=True, with_amenities=True), 200

        except Exception as e:
            return {'error': str(e)}, 400