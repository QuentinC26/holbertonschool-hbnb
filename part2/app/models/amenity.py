from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from .base_model import BaseModel, Base

class Amenity(BaseModel, Base):
    __tablename__ = 'amenities'

    name = Column(String(128), nullable=False)
    places = relationship("Place", secondary='place_amenity', viewonly=True)

    def __init__(self, name):
        super().__init__()
        if not name or len(name.strip()) == 0:
            raise ValueError("Nom de l'équipement requis")
        self.name = name
