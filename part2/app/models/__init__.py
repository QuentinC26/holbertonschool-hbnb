from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from models.base_model import BaseModel

# Stockage global (ex: DBStorage ou FileStorage)
from models.storage import DBStorage
storage = DBStorage()

# Permet d'importer directement : from models import User
__all__ = ['User', 'Place', 'Review', 'Amenity', 'BaseModel']
