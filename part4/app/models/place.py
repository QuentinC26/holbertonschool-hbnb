from app.models.baseclass import BaseModel
from app.models.user import User
from app.models.amenity import Amenity


class Place(BaseModel):
    from app import db
    _tablename__ = 'places'

    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False, unique=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    owner_id = db.Column(db.String(60), db.ForeignKey('users.id'), nullable=False)

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
        self.reviews = []
        self.amenities = []

    def add_review(self, review):
        self.reviews.append(review)

    def add_amenity(self, amenity: Amenity):
        self.amenities.append(amenity)
