import uuid


class Place:
    def __init__(
        self,
        name,
        description,
        city,
        user,
        price_by_night,
        latitude,
        longitude,
        amenities=None
    ):
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.city = city
        self.user = user  # Instance de User
        self.price_by_night = price_by_night
        self.latitude = latitude
        self.longitude = longitude
        self.amenities = amenities if amenities else []

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "city": self.city,
            "price_by_night": self.price_by_night,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner": {
                "id": self.user.id,
                "first_name": self.user.first_name,
                "last_name": self.user.last_name
            },
            "amenities": [a.serialize() for a in self.amenities]
        }
