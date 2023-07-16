from .update_time import UpdateTime, StubTimestampFromUpdateTime
from distributed_storage.data_transfer_api_pb2 import (
    Value as StubValue
)


class Value:
    def __init__(self, update_time: UpdateTime, payload: bytes):
        self.update_time = update_time
        self.payload = payload


class ValueFromXMLRPCDateTime(Value):
    def __init__(self, xml_rpc_value: dict):
        super().__init__(xml_rpc_value['update_time'], xml_rpc_value['payload'].data)


class StubValueFromValue:
    def __init__(self, value: Value):
        self.value = value

    def stub(self):
        print(self.value.payload)
        return StubValue(payload=self.value.payload)
