from .user import User
from .place import Place
from .review import Review
from .amenity import Amenity
from .baseclass import BaseModel

# Permet d'importer directement : from models import User
__all__ = ['User', 'Place', 'Review', 'Amenity', 'BaseModel']
