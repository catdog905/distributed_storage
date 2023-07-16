
from abc import ABC, abstractmethod

from .value import Value


class Storage(ABC):

    @abstractmethod
    def contains(self, key) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_value(self, key: str) -> Value:
        raise NotImplementedError

    @abstractmethod
    def store_value(self, key: str, value: Value):
        raise NotImplementedError
