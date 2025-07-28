from app.models.baseclass import BaseModel
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app.models.place import Place
from .place_amenities import place_amenity

class Amenity(BaseModel):
    from app import db
    __tablename__ = 'amenities'

    id = db.Column(db.String, primary_key = True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    places = relationship("Place", secondary=place_amenity, back_populates="amenities")

    def __init__(self, name):
        super().__init__()
        if not name or len(name) > 50:
            raise ValueError("Nom requis ou trop long (max 50 caractères)")
        self.name = name
