from distributed_storage.storage.majority.major_get_response import MajorGetResponse
from distributed_storage.storage.majority.major_store_response import MajorStoreResponse
from distributed_storage.storage.storage import Storage
from distributed_storage.storage.types.value import Value
from distributed_storage.storage.outside_storage import OutsideStorage


class ValueWasNotStoredProperly(Exception):
    pass


class WeaklyConsistentStorage(Storage):

    def get_value(self, key: str) -> Value:
        return MajorGetResponse(self.storage_nodes).major_get_response(key)

    def store_value(self, key: str, value: Value):
        status = MajorStoreResponse(self.storage_nodes).major_store_response(key, value)
        print(f"this is status = {status}")
        if not status:
            raise ValueWasNotStoredProperly()

    def __init__(self, storage_nodes: list[OutsideStorage]):
        self.storage_nodes = storage_nodes
