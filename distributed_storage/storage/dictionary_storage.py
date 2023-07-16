from .storage import Storage
from distributed_storage.storage.value import Value


class NoSuchKeyInStoragePresent(Exception):
    def __init__(self, key):
        self.key = key


class DictionaryStorage(Storage):

    def contains(self, key) -> bool:
        return key in self.storage

    def get_value(self, key: str) -> Value:
        if key not in self.storage:
            raise NoSuchKeyInStoragePresent(key)
        return self.storage[key]

    def store_value(self, key: str, value: Value):
        self.storage[key] = value

    def __init__(self):
        self.storage = dict()
