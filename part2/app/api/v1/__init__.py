# Import namespaces from individual resource modules

from .users import api as users_api
from .places import api as places_api
from .amenities import api as amenities_api
from .reviews import api as reviews_api
from .auth import api as auth_api

# Expose namespaces for higher-level import

api = [
    users_api,
    places_api,
    amenities_api,
    reviews_api,
    auth_api
]