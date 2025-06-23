from app.models.BaseModel import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        if not name or len(name) > 50:
            raise ValueError("Nom requis ou trop long (max 50 caractères)")
        self.name = name
