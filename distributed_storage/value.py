from distributed_storage.update_time import UpdateTime, StubTimestampFromUpdateTime
from data_transfer_api_pb2 import (
    GetValueResponse,
    Value as StubValue,
    StoreValueResponse
)


class Value:
    def __init__(self, update_time: UpdateTime, payload: bytes):
        self.update_time = update_time
        self.payload = payload


class StubValueFromValue:
    def __init__(self, value: Value):
        self.value = value

    def stub(self):
        return StubValue(update_time=StubTimestampFromUpdateTime(self.value.update_time).stub(),
                         payload=self.value.payload)
