from app.models.engine.db_storage import DBStorage

# Initialize the global storage object used across the app
storage = DBStorage()
storage.reload()
