from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base

place_amenity = Table(
    'place_amenity', Base.metadata,
    Column('place_id', String(60), ForeignKey('places.id'), primary_key=True),
    Column('amenity_id', String(60), ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel, Base):
    __tablename__ = 'places'

    title = Column(String(100), nullable=False)
    description = Column(String(1024))
    price = Column(Integer, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    owner_id = Column(String(60), ForeignKey('users.id'), nullable=False)

    reviews = relationship("Review", backref="place", cascade="all, delete")
    amenities = relationship("Amenity", secondary=place_amenity, viewonly=False)

    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        if not title or len(title) > 100:
            raise ValueError("Titre requis ou trop long (max 100 caractères)")
        if price <= 0:
            raise ValueError("Prix invalide")
        if not (-90.0 <= latitude <= 90.0):
            raise ValueError("Latitude invalide")
        if not (-180.0 <= longitude <= 180.0):
            raise ValueError("Longitude invalide")
        if not owner or not hasattr(owner, 'id'):
            raise ValueError("Propriétaire invalide")

        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner.id
