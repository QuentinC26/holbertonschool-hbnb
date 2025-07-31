from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import HBnBFacade

api = Namespace('amenities', description='Amenity operations')
facade = HBnBFacade()

# Modèle pour Swagger
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True)
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @jwt_required()
    def post(self):
        """Create a new amenity (Admin only)"""
        current_user = get_jwt_identity()
        if not current_user.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403

        data = request.get_json()
        try:
            amenity = facade.create_amenity(data)
            return amenity.to_dict(), 201
        except Exception as e:
            return {'error': str(e)}, 400

    def get(self):
        """Retrieve all amenities (Public)"""
        try:
            amenities = [a.to_dict() for a in facade.get_all_amenities()]
            return amenities, 200
        except Exception as e:
            return {'error': str(e)}, 500


@api.route('/<string:amenity_id>')
class AmenityResource(Resource):
    def get(self, amenity_id):
        """Retrieve a single amenity (Public)"""
        try:
            amenity = facade.get_amenity(amenity_id)
            if not amenity:
                return {'error': 'Amenity not found'}, 404
            return amenity.to_dict(), 200
        except Exception as e:
            return {'error': str(e)}, 404

    @api.expect(amenity_model)
    @jwt_required()
    def put(self, amenity_id):
        """Update an amenity (Admin only)"""
        current_user = get_jwt_identity()
        if not current_user.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403

        data = request.get_json()
        try:
            updated_amenity = facade.update_amenity(amenity_id, data)
            return updated_amenity.to_dict(), 200
        except Exception as e:
            return {'error': str(e)}, 400
