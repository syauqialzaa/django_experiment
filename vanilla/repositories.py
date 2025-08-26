import hashlib

class BaseRepository:
    def __init__(self):
        self._data = {}
        self._counter = 1

    def all(self):
        return list(self._data.values())

    def get(self, item_id):
        return self._data.get(item_id)
    
    def save(self, item_data):
        item_id = self._counter
        item_data['id'] = item_id
        self._data[item_id] = item_data
        self._counter += 1
        return item_data

class UserRepository(BaseRepository):
    def find_by_username(self, username):
        for user in self.all():
            if user['username'] == username:
                return user
        return None

# Instantiate repositories
user_repo = UserRepository()
service_repo = BaseRepository()
appointment_repo = BaseRepository()