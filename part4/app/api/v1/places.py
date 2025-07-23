from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from app.services import facade

api = Namespace('places', description='Place operations')

# Related models
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String,
    'name': fields.String
})

user_model = api.model('PlaceUser', {
    'id': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String
})

# Adding the review model
review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'owner': fields.Nested(user_model, description='Owner of the place'),
    'amenities': fields.List(fields.Nested(amenity_model), description='List of amenities'),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews')
})


@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        data = request.get_json()
        amenities = data.pop('amenities', None)
        current_user = get_jwt_identity()["id"]
        data["owner_id"] = current_user
        try:
            place = facade.create_place(data)
            return {'id': place.id, 'title': place.title, 'description': place.description, 'price': place.price, 'latitude': place.latitude, 'longitude': place.longitude, 'owner_id': place.owner.id if place.owner else None}, 201
        except Exception as e:
            return {"error": str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        places = facade.get_list_places()
        return [{'id': place.id, 'title': place.title, 'description': place.description, 'price': place.price, 'latitude': place.latitude, 'longitude': place.longitude, 'owner_id': place.owner.id if place.owner else None} for place in places], 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        return {'id': place.id, 
                'title': place.title,
                'description': place.description,
                'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'owner': {
                    "id": place.owner.id, 
                    "first_name": place.owner.first_name,
                    "last_name": place.owner.last_name,
                    "email": place.owner.email
                    }   
                    if place.owner else None, 
                'amenities': [
                    {
                        'id': amenity.id, 
                        'name': amenity.name
                    } 
                    for amenity in place.amenities
                    ]}, 200

    @api.response(200, 'Place updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Place not found')
    @jwt_required()
    def put(self, place_id):
        data = request.get_json()
        current_user = get_jwt_identity()
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 403
        if not place.owner or place.owner.id != current_user["id"]:
            return {'error': 'Unauthorized action'}, 403
        try:
            updated_place = facade.update_place(place_id, data)
            return {"message": "Place updated successfully"}, 200
        except Exception as e:
            return {"error": str(e)}, 400
