import re
from datetime import datetime
from app.models.BaseModel import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Email invalide")
        if len(first_name) > 50 or len(last_name) > 50:
            raise ValueError("Nom trop long (max 50 caractères)")

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
