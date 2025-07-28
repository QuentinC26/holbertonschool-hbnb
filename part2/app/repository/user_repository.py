# app/repository/user_repository.py

from app.models.user import User
from app.models.engine.db_storage import db



class UserRepository:
    def __init__(self, session=db.session):
        self.session = session

    def add(self, user):
        self.session.add(user)
        self.session.commit()

    def get(self, user_id):
        return self.session.query(User).filter_by(id=user_id).first()

    def get_all(self):
        return self.session.query(User).all()

    def get_by_email(self, email):
        return self.session.query(User).filter_by(email=email).first()

    def update(self):
        self.session.commit()

    def delete(self, user):
        self.session.delete(user)
        self.session.commit()
