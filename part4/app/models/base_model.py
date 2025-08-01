import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BaseModel:
    id = Column(String(60), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def save(self):
        self.updated_at = datetime.utcnow()

    def update(self, data: dict):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()

    def to_dict(self):
        d = self.__dict__.copy()
        d.pop('_sa_instance_state', None)
        return d
