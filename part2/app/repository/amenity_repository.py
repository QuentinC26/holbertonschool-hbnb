from app.models.amenity import Amenity
from app.models.engine.db_storage import db  # Assuming 'db' is the SQLAlchemy instance

class AmenityRepository:
    def __init__(self, session=db.session):
        self.session = session

    def add(self, amenity):
        self.session.add(amenity)
        self.session.commit()

    def get(self, amenity_id):
        return self.session.query(Amenity).filter_by(id=amenity_id).first()

    def get_all(self):
        return self.session.query(Amenity).all()

    def update(self):
        self.session.commit()

    def delete(self, amenity):
        self.session.delete(amenity)
        self.session.commit()
