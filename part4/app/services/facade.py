from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

from app.repository.user_repository import UserRepository
from app.repository.place_repository import PlaceRepository
from app.repository.review_repository import ReviewRepository
from app.repository.amenity_repository import AmenityRepository

from app.utils.validation import validate_price, validate_latitude, validate_longitude

class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()

    # Users
    def create_user(self, user_data):
        required_fields = ['first_name', 'last_name', 'email', 'password']
        for field in required_fields:
            if not user_data.get(field):
                raise ValueError(f"Le champ '{field}' est requis.")

        user = User(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email'],
            password=user_data['password'],  # va appeler le setter → hash
            is_admin=user_data.get('is_admin', False)
        )

        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_email(email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, data):
        user = self.get_user(user_id)
        if not user:
            return None
        user.update(data)
        self.user_repo.update()
        return user

    def delete_user(self, user_id):
        user = self.get_user(user_id)
        if not user:
            return False
        self.user_repo.delete(user)
        return True

    # Amenities
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, data):
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None
        amenity.update(data)
        self.amenity_repo.update()
        return amenity

    def delete_amenity(self, amenity_id):
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return False
        self.amenity_repo.delete(amenity)
        return True

    # Reviews
    def create_review(self, review_data):
        user = self.get_user(review_data.get("user_id"))
        place = self.place_repo.get(review_data.get("place_id"))

        if not user or not place:
            raise ValueError("User or Place not found")

        rating = review_data.get("rating")
        if rating is None or not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")

        review = Review(**review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")
        return [r for r in self.get_all_reviews() if r.place_id == place_id]

    def update_review(self, review_id, data):
        review = self.get_review(review_id)
        if not review:
            return None
        review.update(data)
        self.review_repo.update()
        return review

    def delete_review(self, review_id):
        review = self.get_review(review_id)
        if not review:
            return False
        self.review_repo.delete(review)
        return True

    # Places
    def create_place(self, place_data):
        validate_price(place_data.get('price'))
        validate_latitude(place_data.get('latitude'))
        validate_longitude(place_data.get('longitude'))

        place = Place(**place_data)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, data):
        place = self.get_place(place_id)
        if not place:
            return None

        if 'price' in data:
            validate_price(data['price'])
        if 'latitude' in data:
            validate_latitude(data['latitude'])
        if 'longitude' in data:
            validate_longitude(data['longitude'])

        place.update(data)
        self.place_repo.update()
        return place

    def delete_place(self, place_id):
        place = self.get_place(place_id)
        if not place:
            return False
        self.place_repo.delete(place)
        return True
