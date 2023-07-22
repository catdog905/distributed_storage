import os

from distributed_storage.environment_variables.EnvironmentVariable import EnvironmentVariable


class RedisNodesSuffix(EnvironmentVariable):
    def value(self):
        return os.getenv('REDIS_SUFFIX')
