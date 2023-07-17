from abc import ABC, abstractmethod


class EnvironmentVariable(ABC):

    @abstractmethod
    def value(self):
        raise NotImplementedError
