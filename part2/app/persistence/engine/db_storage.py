import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base

class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        user = os.getenv("HBNB_MYSQL_USER")
        pwd = os.getenv("HBNB_MYSQL_PWD")
        host = os.getenv("HBNB_MYSQL_HOST", "localhost")
        db = os.getenv("HBNB_MYSQL_DB")
        env = os.getenv("HBNB_ENV")

        # Create the engine to connect to the MySQL database
        self.__engine = create_engine(
            f"mysql+mysqldb://{user}:{pwd}@{host}/{db}", pool_pre_ping=True)

        # If running in test environment, drop all tables
        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def reload(self):
        """Creates all tables in the database and initializes the session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)

    def all(self, cls=None):
        """Returns a dictionary of all objects, optionally filtered by class"""
        obj_dict = {}
        if cls:
            objs = self.__session.query(cls).all()
            for obj in objs:
                obj_dict[f"{obj.__class__.__name__}.{obj.id}"] = obj
        else:
            for subclass in Base.__subclasses__():
                objs = self.__session.query(subclass).all()
                for obj in objs:
                    obj_dict[f"{obj.__class__.__name__}.{obj.id}"] = obj
        return obj_dict

    def get(self, cls, id):
        """Returns one object based on class and ID, or None if not found"""
        return self.__session.query(cls).filter_by(id=id).first()

    def add(self, obj):
        """Adds the object to the current database session and commits"""
        self.__session.add(obj)
        self.__session.commit()

    def delete(self, obj):
        """Deletes the object from the current database session and commits"""
        self.__session.delete(obj)
        self.__session.commit()

    def close(self):
        """Removes the current session"""
        self.__session.remove()
