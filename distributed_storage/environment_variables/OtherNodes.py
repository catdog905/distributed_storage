import os

from distributed_storage.environment_variables.EnvironmentVariable import EnvironmentVariable


class OtherNodes(EnvironmentVariable):
    def value(self) -> list:
        return os.getenv('OTHER_NODES').split(",")
