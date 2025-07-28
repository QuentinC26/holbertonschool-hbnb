import re
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from .base_model import BaseModel, Base

class User(BaseModel, Base):
    __tablename__ = 'users'

    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(128), nullable=False, unique=True)
    is_admin = Column(String(5), default='False')
    password = Column(String(128), nullable=False)

    places = relationship("Place", backref="owner", cascade="all, delete")
    reviews = relationship("Review", backref="user", cascade="all, delete")

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()
        if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Email invalide")
        if len(first_name) > 50 or len(last_name) > 50:
            raise ValueError("Nom trop long (max 50 caractères)")

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_admin = str(is_admin)
