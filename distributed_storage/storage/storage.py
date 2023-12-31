from abc import ABC, abstractmethod

from distributed_storage.storage.types.value import Value


class NoSuchKeyInStoragePresent(Exception):
    def __init__(self, key):
        self.key = key


class Storage(ABC):

    @abstractmethod
    def get_value(self, key: str) -> Value:
        raise NotImplementedError

    @abstractmethod
    def store_value(self, key: str, value: Value):
        raise NotImplementedError
