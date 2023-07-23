from distributed_storage.storage.storage import Storage
from distributed_storage.storage.majority.major_response import MajorResponse
from distributed_storage.storage.types.value import Value


class MajorGetResponse:
    def major_get_response(self, key: str) -> Value:
        return MajorResponse(
            actors=self.storage_servers,
            target_function=lambda storage: storage.get_value(key),
            accept_threshold=0.5
        ).major_response()

    def __init__(self, storage_servers: list[Storage]):
        self.storage_servers = storage_servers
