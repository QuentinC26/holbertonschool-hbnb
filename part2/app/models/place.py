from app.models.base_model import BaseModel
from app.models.user import User
from app.models.amenity import Amenity
from extensions import db


class Place(BaseModel):
    def __init__(
            self, title, description, price, latitude, longitude, owner: User, amenities=None):
        super().__init__()
        if not title or len(title) > 100:
            raise ValueError("Titre requis ou trop long (max 100 caractères)")
        if price <= 0:
            raise ValueError("Prix invalide")
        if not (-90.0 <= latitude <= 90.0):
            raise ValueError("Latitude invalide")
        if not (-180.0 <= longitude <= 180.0):
            raise ValueError("Longitude invalide")
        if not isinstance(owner, User):
            raise ValueError("Propriétaire invalide")

        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []
        self.amenities = []

        __tablename__ = 'places'

        title = db.Column(db.String(128), nullable=False)
        description = db.Column(db.String(1024), nullable=True)
        price = db.Column(db.Float, nullable=False)
        latitude = db.Column(db.Float, nullable=True)
        longitude = db.Column(db.Float, nullable=True)

    def add_review(self, review):
        self.reviews.append(review)

    def add_amenity(self, amenity: Amenity):
        self.amenities.append(amenity)
