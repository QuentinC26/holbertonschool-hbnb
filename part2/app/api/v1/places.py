from flask_restx import Namespace, Resource, fields
from services.place_facade import HBNBFacade

api = Namespace("places", description="Place operations")
facade = HBNBFacade()

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
