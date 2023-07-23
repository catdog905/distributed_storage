from distributed_storage.storage.storage import Storage
from distributed_storage.storage.types.value import Value
from distributed_storage.storage_servers.majority.major_response import MajorResponse


class MajorStoreResponse:
    def major_store_response(self, key: str, value: Value):
        return MajorResponse(
            actors=self.storage_servers,
            target_function=lambda storage: True if storage.store_value(key, value) is None else False,
            accept_threshold=0.5
        ).major_response()

    def __init__(self, storage_servers: list[Storage]):
        self.storage_servers = storage_servers
