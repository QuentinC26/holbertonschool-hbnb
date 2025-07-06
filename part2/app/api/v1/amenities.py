from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request

api = Namespace('admin', description='Admin operations')

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        amenity_data = api.payload
        new_amenity = facade.create_amenity(self, amenity_data)
        if not new_amenity:
            return {"Invalid input data", 400}
        else:
            return {'id': new_amenity.id, 'name': new_amenity.name}, 201

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenity_data = api.payload
        amenities = facade.get_all_amenities(self)
        return [{'id': amenities.id, 'name': amenities.name} for amenity in amenities], 200

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity_data = api.payload
        amenity = facade.get_amenity(self, amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return {'id': new_amenity.id, 'name': new_amenity.name}, 200

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        amenity_data = api.payload
        amenity = facade.update_amenity(self, amenity_id, amenity_data)
        if amenity is None:
            return {'error': 'Amenity not found'}, 404
        elif not amenity :
            return {'error': 'Invalid input data'}, 400
        else:
            amenity.name = amenity_data['name']
            return {'id': amenity.id, 'name': amenity.name}, 200

@api.route('/amenities/')
class AdminAmenityCreate(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        amenity_data = request.json
        new_amenity = facade.create_amenity(amenity_data)
        return {'message': 'Amenity created', 'amenity': new_amenity.to_dict()}, 201
