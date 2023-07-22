from abc import ABC, abstractmethod


class EnvironmentVariable(ABC):

    @abstractmethod
    def value(self):
        raise NotImplementedError

    def __str__(self):
        return str(self.value())

    def __repr__(self):
        return str(self.value())
