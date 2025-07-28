from flask_restx import Namespace, Resource, fields
from flask import request
from app.services.facade import HBnBFacade

api = Namespace('amenities', description='Amenity operations')
facade = HBnBFacade()

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True)
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    def post(self):
        """Create a new amenity"""
        try:
            amenity = facade.create_amenity(request.get_json())
            return amenity.to_dict(), 201
        except Exception as e:
            return {'error': str(e)}, 400

    def get(self):
        """Retrieve all amenities"""
        amenities = [a.to_dict() for a in facade.get_all_amenities()]
        return amenities, 200

@api.route('/<string:amenity_id>')
class AmenityResource(Resource):
    def get(self, amenity_id):
        """Retrieve a single amenity"""
        try:
            amenity = facade.get_amenity(amenity_id)
            return amenity.to_dict(), 200
        except Exception as e:
            return {'error': str(e)}, 404

    @api.expect(amenity_model)
    def put(self, amenity_id):
        """Update an existing amenity"""
        try:
            amenity = facade.update_amenity(amenity_id, request.get_json())
            return amenity.to_dict(), 200
        except Exception as e:
            return {'error': str(e)}, 400
