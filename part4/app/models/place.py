from app.models.baseclass import BaseModel
from app.models.user import User
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from .place_amenities import place_amenity


class Place(BaseModel):
    from app import db
    __tablename__ = 'places'

    id = db.Column(db.String, primary_key = True, nullable=False)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False, unique=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    owner_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    owner = relationship("User", backref="places")
    amenities = relationship("Amenity", secondary=place_amenity, back_populates="places")

    def __init__(self, title, description, price, latitude, longitude, owner: User, amenities=None):
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
        self.amenities = amenities if amenities is not None else []

    def add_review(self, review):
        self.reviews.append(review)

    def add_amenity(self, amenity):
        self.amenities.append(amenity)
