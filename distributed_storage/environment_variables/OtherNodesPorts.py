import os

from distributed_storage.environment_variables.EnvironmentVariable import EnvironmentVariable


class OtherNodesPorts(EnvironmentVariable):
    def value(self) -> list:
        return [os.getenv('OTHER_NODE_PORT', 1234)]
