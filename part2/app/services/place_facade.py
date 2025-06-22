from models.place import Place
from models.user import User
from models.amenity import Amenity


class HBNBFacade:

    def create_place(self, data):
        # Valider les attributs requis
        required = [
            "name", "description", "city", "user_id",
            "price_by_night", "latitude", "longitude"
        ]

        for field in required:
            if field not in data:
                raise ValueError(f"Missing field: {field}")

        # Récupérer l'utilisateur propriétaire
        user = self.repo.get("User", data["user_id"])
        if not user:
            raise ValueError("Invalid user_id")

        # Récupérer les amenities s'ils sont fournis
        amenities = []
        for amenity_id in data.get("amenity_ids", []):
            amenity = self.repo.get("Amenity", amenity_id)
            if amenity:
                amenities.append(amenity)

        # Validation de base
        if float(data["price_by_night"]) < 0:
            raise ValueError("Price must be non-negative")
        if not (-90 <= float(data["latitude"]) <= 90):
            raise ValueError("Invalid latitude")
        if not (-180 <= float(data["longitude"]) <= 180):
            raise ValueError("Invalid longitude")

        place = Place(
            name=data["name"],
            description=data["description"],
            city=data["city"],
            user=user,
            price_by_night=float(data["price_by_night"]),
            latitude=float(data["latitude"]),
            longitude=float(data["longitude"]),
            amenities=amenities
        )
        self.repo.add("Place", place)
        return place

    def get_place(self, place_id):
        return self.repo.get("Place", place_id)

    def list_places(self):
        return self.repo.all("Place")

    def update_place(self, place_id, data):
        place = self.repo.get("Place", place_id)
        if not place:
            return None

        for key in [
            "name", "description", "city",
            "price_by_night", "latitude", "longitude"
        ]:
            if key in data:
                setattr(place, key, data[key])
        return place
