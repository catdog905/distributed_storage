from distributed_storage.storage.storage import Storage
from distributed_storage.storage.types.update_time import CurrentUpdateTime
from distributed_storage.storage.types.value import Value
from distributed_storage.storage_servers.majority.major_get_response import MajorGetResponse
from distributed_storage.storage_servers.majority.major_store_response import MajorStoreResponse
from distributed_storage.storage_servers.outside_storage import OutsideStorage


class LowConsistentStorage(Storage):

    def get_value(self, key: str) -> Value:
        return MajorGetResponse(self.other_nodes).major_get_response(key)

    def store_value(self, key: str, value: Value):
        self.origin.store_value(key, Value(update_time=CurrentUpdateTime(), payload=value.payload))
        status = MajorStoreResponse(self.other_nodes).major_store_response(key, value)
        print(f"this is status = {status}")

    def __init__(self, origin: Storage, other_nodes: list[OutsideStorage]):
        self.origin = origin
        self.other_nodes = other_nodes
