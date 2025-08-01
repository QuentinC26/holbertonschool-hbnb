from app.models.baseclass import BaseModel
from app.models.user import User
from app.models.place import Place
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey


class Review(BaseModel):
    from app import db
    __tablename__ = 'reviews'

    id = db.Column(db.String, primary_key = True, nullable=False)
    text = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    user = relationship("User", backref="reviews")
    place_id = db.Column(db.String, db.ForeignKey('places.id'), nullable=False)
    place = relationship("Place", backref="reviews")

    def __init__(self, text, rating, place: Place, user: User):
        super().__init__()
        if not text:
            raise ValueError("Le texte de l'avis est requis")
        if not (1 <= rating <= 5):
            raise ValueError("La note doit être entre 1 et 5")
        if not isinstance(place, Place):
            raise ValueError("Place invalide")
        if not isinstance(user, User):
            raise ValueError("Utilisateur invalide")

        self.text = text
        self.rating = rating
        self.place = place
        self.user = user
