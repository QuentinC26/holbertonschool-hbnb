from .user import User
from .place import Place
from .review import Review
from .amenity import Amenity
from .base_model import BaseModel

# Stockage global (ex: DBStorage ou FileStorage)
from models.storage import DBStorage
storage = DBStorage()

# Permet d'importer directement : from models import User
__all__ = ['User', 'Place', 'Review', 'Amenity', 'BaseModel']
