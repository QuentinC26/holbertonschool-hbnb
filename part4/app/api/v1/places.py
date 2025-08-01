from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import HBnBFacade

api = Namespace('places', description='Place operations')
facade = HBnBFacade()

# === Modèle pour Swagger ===
place_model = api.model('Place', {
    'title': fields.String(required=True),
    'description': fields.String,
    'price': fields.Float(required=True),
    'latitude': fields.Float(required=True),
    'longitude': fields.Float(required=True),
    'owner_id': fields.String(required=True),
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
            current_user = get_jwt_identity()
            data = request.get_json()
            data['owner_id'] = current_user['id']  # Sécurisé depuis JWT

            place = facade.create_place(data)
            return place.to_dict(with_owner=True, with_amenities=True), 201
        except Exception as e:
            return {'error': str(e)}, 400

    def get(self):
        """Retrieve all places"""
        places = facade.get_all_places()
        return [p.to_dict() for p in places], 200

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
            current_user = get_jwt_identity()
            user_id = current_user.get('id')
            is_admin = current_user.get('is_admin', False)

            place = facade.get_place(place_id)
            if not place:
                return {'error': 'Place not found'}, 404

            # Vérifie si admin ou propriétaire
            if not is_admin and place.owner_id != user_id:
                return {'error': 'Unauthorized action'}, 403

            # Mise à jour des données
            data = request.get_json()
            updated_place = facade.update_place(place_id, data)
            return updated_place.to_dict(with_owner=True, with_amenities=True), 200

        except Exception as e:
            return {'error': str(e)}, 400
