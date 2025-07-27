from sqlalchemy import Column, String, Integer, ForeignKey
from models.base_model import BaseModel, Base

class Review(BaseModel, Base):
    __tablename__ = 'reviews'

    text = Column(String(1024), nullable=False)
    rating = Column(Integer, nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    place_id = Column(String(60), ForeignKey('places.id'), nullable=False)

    def __init__(self, text, rating, place, user):
        super().__init__()
        if not text:
            raise ValueError("Text requierment")
        if not (1 <= rating <= 5):
            raise ValueError("The note rating between 1 and 5")
        if not place or not hasattr(place, 'id'):
            raise ValueError("Place invalid")
        if not user or not hasattr(user, 'id'):
            raise ValueError("User invalid")

        self.text = text
        self.rating = rating
        self.place_id = place.id
        self.user_id = user.id
