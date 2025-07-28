from flask_restx import Namespace, Resource, fields
from flask import request
from app.services.facade import HBnBFacade

api = Namespace('places', description='Place operations')
facade = HBnBFacade()

place_model = api.model('Place', {
    'title': fields.String(required=True),
    'description': fields.String,
    'price': fields.Float(required=True),
    'latitude': fields.Float(required=True),
    'longitude': fields.Float(required=True),
    'owner_id': fields.String(required=True),
    'amenities': fields.List(fields.String, required=True)
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    def post(self):
        """Create a new place"""
        try:
            place = facade.create_place(request.get_json())
            return place.to_dict(with_owner=True, with_amenities=True), 201
        except Exception as e:
            return {'error': str(e)}, 400

    def get(self):
        """Retrieve all places"""
        places = facade.get_all_places()
        return [p.to_dict() for p in places], 200

@api.route('/<string:place_id>')
class PlaceResource(Resource):
    def get(self, place_id):
        """Retrieve a single place with relationships"""
        try:
            place = facade.get_place(place_id)
            return place.to_dict(with_owner=True, with_amenities=True), 200
        except Exception as e:
            return {'error': str(e)}, 404

    @api.expect(place_model)
    def put(self, place_id):
        """Update an existing place"""
        try:
            facade.update_place(place_id, request.get_json())
            return {'message': 'Place updated successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 400
