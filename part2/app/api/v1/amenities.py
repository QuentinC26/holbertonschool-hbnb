from flask_restx import Namespace, Resource, fields
from app.services import facade

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
        new_amenity = create_amenity(self, amenity_data)
        if not new_amenity:
            return {"Invalid input data", 400}
        else:
            return dict(new_amenity), 201

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenity = get_all_amenities(self)
        return list(amenity), 200

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = get_amenity(self, amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return amenity, 200

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        amenity = facade. update_amenity(self, amenity_id, amenity_data)
        if amenity is None:
            return {'error': 'Amenity not found'}, 404
        else:
            amenity_data = api.payload
            return amenity, 200
