import re
from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship
from .base_model import BaseModel, Base
from werkzeug.security import check_password_hash, generate_password_hash

class User(BaseModel, Base):
    __tablename__ = 'users'

    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(128), nullable=False, unique=True)
    is_admin = Column(Boolean, nullable=False, default=False)
    _password = Column("password", String(512), nullable=False)

    places = relationship("Place", backref="owner", cascade="all, delete")
    reviews = relationship("Review", backref="user", cascade="all, delete")

    def __init__(self, first_name, last_name, email, password, is_admin=False, **kwargs):
        super().__init__(**kwargs)
        if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Email invalide")
        if len(first_name) > 50 or len(last_name) > 50:
            raise ValueError("Nom trop long (max 50 caractères)")

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password  # setter hash
        self.is_admin = is_admin

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = generate_password_hash(value)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
    return {
        'id': str(self.id),
        'first_name': self.first_name,
        'last_name': self.last_name,
        'email': self.email,
        'is_admin': self.is_admin,
        'created_at': self.created_at.isoformat() if self.created_at else None,
        'updated_at': self.updated_at.isoformat() if self.updated_at else None
    }