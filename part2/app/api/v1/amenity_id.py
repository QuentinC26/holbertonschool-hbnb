from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request

api = Namespace('admin', description='Admin operations')

@api.route('/amenities/<amenity_id>')
class AdminAmenityModify(Resource):
    @jwt_required()
    def put(self, amenity_id):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        data = request.json
        updated_amenity = facade.update_amenity(amenity_id, data)
        return {'message': 'Amenity updated', 'amenity': updated_amenity.to_dict()}, 200
