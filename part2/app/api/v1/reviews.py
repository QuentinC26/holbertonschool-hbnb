from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import HBnBFacade

api = Namespace('reviews', description='Review operations')
facade = HBnBFacade()

review_model = api.model('Review', {
    'text': fields.String(required=True),
    'rating': fields.Integer(required=True),
    'user_id': fields.String(required=True),
    'place_id': fields.String(required=True)
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @jwt_required()
    def post(self):
        """Create a new review (authenticated only)"""
        data = request.get_json()
        data['user_id'] = get_jwt_identity()
        review = facade.create_review(data)
        return review.to_dict(), 201

    @jwt_required()
    def get(self):
        """Get all reviews (authenticated only)"""
        reviews = facade.get_all_reviews()
        return [r.to_dict() for r in reviews], 200

@api.route('/<string:review_id>')
class ReviewResource(Resource):
    @jwt_required()
    def get(self, review_id):
        """Get a single review (authenticated only)"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return review.to_dict(), 200

    @api.expect(review_model)
    @jwt_required()
    def put(self, review_id):
        """Update review (authenticated only)"""
        try:
            facade.update_review(review_id, request.get_json())
            return {'message': 'Review updated successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 400