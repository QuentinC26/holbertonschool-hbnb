from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review
from app.persistence.repository import SQLAlchemyRepository

class HBnBFacade:
    def __init__(self):
        self.user_repository = SQLAlchemyRepository(User)  # Switched to SQLAlchemyRepository
        self.place_repository = SQLAlchemyRepository(Place)
        self.review_repository = SQLAlchemyRepository(Review)
        self.amenity_repository = SQLAlchemyRepository(Amenity)

    def create_user(self, user_data):
        from app import bcrypt
        user = User(**user_data)
        user.hash_password(user.password)
        user.verify_password(user.password)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_users(self, user_id, user_data):
        user = self.user_repo.update(user_id, user_data)
        if not user:
            return None

        for key in ["first_name", "last_name"]:
            if key in user_data:
                setattr(user, key, user_data[key])
        return user

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
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        # Placeholder for logic to update an amenity
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        if 'name' in amenity_data:
            amenity.name = amenity_data['name']
        else:
            return False
        return amenity

    def create_place(self, data):
        # Valider les attributs requis
        required = [
            "title", "description", "price", "latitude", "longitude", "owner_id"
        ]

        for field in required:
            if field not in data:
                raise ValueError(f"Missing field: {field}")

        # Récupérer l'utilisateur propriétaire
        user = self.user_repo.get(data["owner_id"])
        if not user:
            raise ValueError("Invalid owner_id")

        # Récupérer les amenities s'ils sont fournis
        amenities = []
        for amenity_id in data.get("amenities", []):
            amenity = self.amenity_repo.get(amenity_id)
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
            owner=user
        )
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_list_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, data):
        place = self.place_repo.get(place_id)
        if not place:
            return None

        for key in [
            "title", "description", "price",
            "latitude", "longitude"
        ]:
            if key in data:
                setattr(place, key, data[key])
        return place

    def create_review(self, review_data):
        user = self.user_repo.get(review_data["user_id"])
        place = self.place_repo.get(review_data["place_id"])

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
        review.save()
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
        return [review for review in self.review_repo.get_all() if review.place.id == place_id]

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            return None
        for key in ["text", "rating"]:
            if key in review_data:
                setattr(review, key, review_data[key])
        review.save()
        return review

    def delete_review(self, review_id):
        review = self.review_repo.delete(review_id)
        if not review:
            return None
        review.delete()
        return True
