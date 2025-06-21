class InMemoryRepository:
    def __init__(self):
        self.storage = {
            "User": {},
            "Place": {},
            "Review": {},
            "Amenity": {}
        }

    def add(self, entity_type, obj):
        if not hasattr(obj, "id"):
            raise ValueError("Object must have an id")
        self.storage[entity_type][obj.id] = obj

    def get(self, entity_type, obj_id):
        return self.storage[entity_type].get(obj_id)

    def all(self, entity_type):
        return list(self.storage[entity_type].values())

    def delete(self, entity_type, obj_id):
        if obj_id in self.storage[entity_type]:
            del self.storage[entity_type][obj_id]
