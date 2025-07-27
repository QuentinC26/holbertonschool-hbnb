from app.models.user import User
from app.persistence.repository import InMemoryRepository
from repository.place_repository import PlaceRepository
from repository.review_repository import ReviewRepository
from repository.amenity_repository import AmenityRepository

place_repo = PlaceRepository()
review_repo = ReviewRepository()
amenity_repo = AmenityRepository()

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

    def put_update_users(self, user_id):
        return self.user_repo.put(user_id)

    
    def create_amenity(self, amenity_data):
        # Placeholder for logic to create an amenity
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        # Placeholder for logic to retrieve an amenity by ID
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        # Placeholder for logic to retrieve all amenities
        return self.all_amenity_repo.get(amenity)

    def update_amenity(self, amenity_id, amenity_data):
        # Placeholder for logic to update an amenity
        amenity = amenity.get_by_id(amenity_id)
        if not review:
            return None
        for key, value in amenity_data.items():
            setattr(review, key, value)
        amenity.save()
        return amenity



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

    # Place
    def create_place(data): return place_repo.create(data)
    def get_place(id): return place_repo.get(id)
    def get_all_places(): return place_repo.get_all()
    def update_place(place, data): return place_repo.update(place, data)
    def delete_place(place): return place_repo.delete(place)

    # Review
    def create_review(data): return review_repo.create(data)
    def get_review(id): return review_repo.get(id)
    def get_all_reviews(): return review_repo.get_all()
    def update_review(review, data): return review_repo.update(review, data)
    def delete_review(review): return review_repo.delete(review)

    # Amenity
    def create_amenity(data): return amenity_repo.create(data)
    def get_amenity(id): return amenity_repo.get(id)
    def get_all_amenities(): return amenity_repo.get_all()
    def update_amenity(amenity, data): return amenity_repo.update(amenity, data)
    def delete_amenity(amenity): return amenity_repo.delete(amenity)
