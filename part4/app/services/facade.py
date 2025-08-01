from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review
from app.persistence.repository import SQLAlchemyRepository
from app.persistence.UserRepository import UserRepository
from app.persistence.AmenityRepository import AmenityRepository
from app.persistence.PlaceRepository import PlaceRepository
from app.persistence.ReviewRepository import ReviewRepository

class HBnBFacade:
    def __init__(self):
        self.user_repository = UserRepository()
        self.place_repository = PlaceRepository()
        self.review_repository = ReviewRepository()
        self.amenity_repository = AmenityRepository()

    def create_user(self, user_data):
        from app import bcrypt
        user = User(**user_data)
        user.hash_password(user_data["password"])
        user.verify_password(user_data["password"])
        self.user_repository.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repository.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repository.get_user_by_email(email)

    def get_all_users(self):
        return self.user_repository.get_all()

    def update_users(self, user_id, user_data):
        user = self.user_repository.update(user_id, user_data)
        if not user:
            return None

        for key in ["first_name", "last_name"]:
            if key in user_data:
                setattr(user, key, user_data[key])
        return user

    def create_amenity(self, amenity_data):
        # Placeholder for logic to create an amenity
        amenity = Amenity(**amenity_data)
        self.amenity_repository.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        # Placeholder for logic to retrieve an amenity by ID
        return self.amenity_repository.get(amenity_id)

    def get_all_amenities(self):
        # Placeholder for logic to retrieve all amenities
        return self.amenity_repository.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        # Placeholder for logic to update an amenity
        amenity = self.amenity_repository.update(amenity_id, amenity_data)
        if not amenity:
            return None
        if 'name' in amenity_data:
            amenity.name = amenity_data['name']
            return amenity
        else:
            return False

    def create_place(self, data):
        # Valider les attributs requis
        required = [
            "title", "description", "price", "latitude", "longitude", "owner_id"
        ]
        
        for field in required:
            if field not in data:
                raise ValueError(f"Missing field: {field}")

        # Récupérer l'utilisateur propriétaire
        user = self.user_repository.get(data["owner_id"])
        if not user:
            raise ValueError("Invalid owner_id")

        amenities = []

        # Récupérer les amenities s'ils sont fournis
        for amenity_id in data.get("amenities", []):
            amenity = self.amenity_repository.get(amenity_id)
            if amenity:
                amenities.append(amenity)

        # Validation de base
        if float(data["price"]) < 0:
            raise ValueError("Price must be non-negative")
        if not (-90 <= float(data["latitude"]) <= 90):
            raise ValueError("Invalid latitude")
        if not (-180 <= float(data["longitude"]) <= 180):
            raise ValueError("Invalid longitude")

        place = Place(
            title=data["title"],
            description=data["description"],
            price=float(data["price"]),
            latitude=float(data["latitude"]),
            longitude=float(data["longitude"]),
            owner=user,
            amenities=amenities
        )
        self.place_repository.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repository.get(place_id)

    def get_list_places(self):
        return self.place_repository.get_all()

    def update_place(self, place_id, data):
        place = self.place_repository.get(place_id)
        if not place:
            return None

        for key in [
            "title", "description", "price",
            "latitude", "longitude"
        ]:
            if key in data:
                setattr(place, key, data[key])
        
        self.place_repository.commit()
        return place

    def create_review(self, review_data):
        user = self.user_repository.get(review_data["user_id"])
        place = self.place_repository.get(review_data["place_id"])

        if not user or not place:
            raise ValueError("User or Place not found")

        rating = review_data.get("rating")
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")

        review = Review(
                text=review_data["text"],
                user=user,
                place=place,
                rating=review_data["rating"]
                )
        self.review_repository.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repository.get(review_id)

    def get_all_reviews(self):
        return self.review_repository.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.place_repository.get(place_id)
        if not place:
            raise ValueError("Place not found")
        return [review for review in self.review_repository.get_all() if review.place.id == place_id]

    def update_review(self, review_id, review_data):
        review = self.review_repository.get(review_id)
        if not review:
            return None
        for key in ["text", "rating"]:
            if key in review_data:
                setattr(review, key, review_data[key])
        self.review_repository.commit()
        return review

    def delete_review(self, review_id):
        review = self.review_repository.delete(review_id)
        if not review:
            return None
        review.delete()
        return True

    def get_review_by_user_and_place(self, user_id, place_id):
        return next(
            (review for review in self.review_repository.get_all()
             if review.user.id == user_id and review.place.id == place_id),
            None
        )