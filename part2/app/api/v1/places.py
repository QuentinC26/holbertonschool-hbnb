<<<<<<< HEAD
from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace("places", description="Place operations")

place_model = api.model("Place", {
    "name": fields.String(required=True),
    "description": fields.String(required=True),
    "city": fields.String(required=True),
    "user_id": fields.String(required=True),
    "price_by_night": fields.Float(required=True),
    "latitude": fields.Float(required=True),
    "longitude": fields.Float(required=True),
    "amenity_ids": fields.List(fields.String, required=False)
})

@api.route("/")
class PlaceList(Resource):
    def get(self):
        return [p.serialize() for p in facade.list_places()]

    @api.expect(place_model)
    def post(self):
        try:
            data = api.payload
            place = facade.create_place(data)
            return place.serialize(), 201
        except ValueError as e:
            return {"error": str(e)}, 400


@api.route("/<string:place_id>")
class PlaceResource(Resource):
    def get(self, place_id):
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        return place.serialize()

    def put(self, place_id):
        data = api.payload
        place = facade.update_place(place_id, data)
        if not place:
            return {"error": "Place not found"}, 404
        return place.serialize()
=======
from flask_restx import Namespace, Resource, fields
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
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        try:
            data = request.get_json()
            place = facade.create_place(data)
            return place.to_dict(), 201
        except Exception as e:
            return {"error": str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        places = facade.get_all_places()
        return [p.to_dict(fields=['id', 'title', 'latitude', 'longitude']) for p in places], 200

@api.route('/<string:place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        place_dict = place.to_dict()
        place_dict['owner'] = place.owner.to_dict(fields=['id', 'first_name', 'last_name', 'email']) if place.owner else None
        place_dict['amenities'] = [a.to_dict(fields=['id', 'name']) for a in place.amenities]
        return place_dict, 200

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Place not found')
    def put(self, place_id):
        data = request.get_json()
        try:
            place = facade.update_place(place_id, data)
            if not place:
                return {"error": "Place not found"}, 404
            return {"message": "Place updated successfully"}, 200
        except Exception as e:
            return {"error": str(e)}, 400

>>>>>>> 7769b1a32a78878803832508b59414f405d48e9b
