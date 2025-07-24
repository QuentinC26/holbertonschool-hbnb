import re
from datetime import datetime
from app.models.base_model import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, password, is_admin=False):
        __tablename__ = 'users'

        first_name = db.Column(db.String(50), nullable=False)
        last_name = db.Column(db.String(50), nullable=False)
        email = db.Column(db.String(120), nullable=False, unique=True)
        password = db.Column(db.String(128), nullable=False)
        is_admin = db.Column(db.Boolean, default=False)

    def hash_password(self, password):
        from app import bcrypt
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        from app import bcrypt
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)
