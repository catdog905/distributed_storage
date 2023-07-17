import os

from distributed_storage.environment_variables.EnvironmentVariable import EnvironmentVariable


class ExposedGrpcPort(EnvironmentVariable):
    def value(self):
        return int(os.getenv('GRPC_PORT'))
