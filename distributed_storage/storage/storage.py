from distributed_storage.value import Value
from abc import ABC, abstractmethod


class Storage(ABC):

    @abstractmethod
    def get_value(self, key: str) -> Value:
        raise NotImplementedError

    @abstractmethod
    def store_value(self, key: str, value: Value):
        raise NotImplementedError