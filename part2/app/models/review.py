from app.models.base_model import BaseModel
from app.models.user import User
from app.models.place import Place


class Review(BaseModel):
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
