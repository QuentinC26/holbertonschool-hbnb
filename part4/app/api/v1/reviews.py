from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True),
    'rating': fields.Integer(required=True),
    'place_id': fields.String(required=True)
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @jwt_required()
    def post(self):
        review_data = api.payload
        current_user = get_jwt_identity()
        user_id = current_user['id']
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        place = facade.get_place(review_data["place_id"])
        if not place:
            return {'error': 'Place not found'}, 404
        review = facade.get_all_reviews()
        try:
            if user_id == place.owner.id:
                return {'error': "You cannot review your own place."}, 400
            existing_review = facade.get_review_by_user_and_place(user_id, review_data["place_id"])
            if existing_review:
                return {'error': "You have already reviewed this place."}, 400
            new_review = facade.create_review(review_data)
            return {"id": new_review.id, "text": new_review.text, "rating": new_review.rating, "user_id": user.id if user.id else None, 'place_id': place.id if place.id else None}, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    def get(self):
        reviews = facade.get_all_reviews()
        return [{'id': review.id, 'text': review.text, 'rating': review.rating} for review in reviews], 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    def get(self, review_id):
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return {'id': review.id, 'text': review.text, 'rating': review.rating, "user_id": review.user.id if review.user.id else None, 'place_id': review.place.id if review.place.id else None}, 200

    @api.expect(review_model)
    @jwt_required()
    def put(self, review_id):
        current_user = get_jwt_identity()
        user_id = current_user['id']
        review = facade.get_review(review_id)
        review_data = api.payload
        if not review_data:
            return {'error': 'Review not found'}, 404
        if review.user.id != user_id:
                return {'error': "Unauthorized action."}, 403
        try:
            updated_review = facade.update_review(review_id, review_data)
            return {'message': 'Review updated successfully'}, 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @jwt_required()
    def delete(self, review_id):
        current_user = get_jwt_identity()
        user_id = current_user['id']
        review = facade.get_review(review_id)
        review_data = api.payload
        if not review:
            return {'error': 'Review not found'}, 404
        if review.user.id != user_id:
            return {'error': "Unauthorized action."}, 403
        deleted = facade.delete_review(review_id)
        return {'message': 'Review deleted successfully'}, 200

