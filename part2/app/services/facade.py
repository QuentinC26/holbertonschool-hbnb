from app.models.user import User
from app.persistence.repository import InMemoryRepository

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def put(self, user_id):
        return self.user_repo.put(user_id)

    def create_review(self, review_data):
        user = User.get_by_id(review_data["user_id"])
        place = Place.get_by_id(review_data["place_id"])

        if not user or not place:
            raise ValueError("User or Place not found")

        rating = review_data.get("rating")
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")

        review = Review(**review_data)
        review.save()
        return review

    def get_review(self, review_id):
        return Review.get_by_id(review_id)

    def get_all_reviews(self):
        return Review.all()

    def get_reviews_by_place(self, place_id):
        place = Place.get_by_id(place_id)
        if not place:
            raise ValueError("Place not found")
        return [r for r in Review.all() if r.place_id == place_id]

    def update_review(self, review_id, review_data):
        review = Review.get_by_id(review_id)
        if not review:
            return None
        for key, value in review_data.items():
            setattr(review, key, value)
        review.save()
        return review

    def delete_review(self, review_id):
        review = Review.get_by_id(review_id)
        if not review:
            return None
        review.delete()
        return True
