import uuid
from .baseclass import BaseModel
import re
from datetime import datetime
from sqlalchemy.orm import relationship

class User(BaseModel):
    from app import bcrypt, db
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_admin = is_admin

    def hash_password(self, password):
        from app import bcrypt
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        from app import bcrypt
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)
