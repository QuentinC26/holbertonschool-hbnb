from persistence.repository import InMemoryRepository


class HBNBFacade:
    def __init__(self):
        self.repo = InMemoryRepository()

    def create_user(self, user):
        self.repo.add("User", user)

    def get_user(self, user_id):
        return self.repo.get("User", user_id)

    def list_users(self):
        return self.repo.all("User")
