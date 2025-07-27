from app.models.baseclass import BaseModel
from sqlalchemy.orm import relationship

class Amenity(BaseModel):
    from app import db
    __tablename__ = 'amenities'

    id = db.Column(db.String, primary_key = True, nullable=False)
    name = db.Column(db.String(50), nullable=False)

    def __init__(self, name):
        super().__init__()
        if not name or len(name) > 50:
            raise ValueError("Nom requis ou trop long (max 50 caractères)")
        self.name = name
