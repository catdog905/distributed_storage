import pickle

from .dictionary_storage import NoSuchKeyInStoragePresent
from .storage import Storage
from redis.cluster import RedisCluster

from .types.value import Value


class RedisStorage(Storage):
    def contains(self, key) -> bool:
        return self.redis.exists(key)

    def get_value(self, key: str) -> Value:
        returned_value = self.redis.get(key)
        if returned_value is None:
            raise NoSuchKeyInStoragePresent(key)
        return pickle.loads(returned_value)

    def store_value(self, key: str, value: Value):
        self.redis.set(key, pickle.dumps(value))

    def __init__(self, startup_nodes):
        self.redis = RedisCluster(startup_nodes=startup_nodes)
