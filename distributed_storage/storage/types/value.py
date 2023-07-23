from .update_time import UpdateTime
from distributed_storage.proto.data_transfer_api_pb2 import (
    Value as StubValue
)


class Value:
    def __init__(self, update_time: UpdateTime, payload: bytes):
        self.update_time = update_time
        self.payload = payload

    def __eq__(self, other):
        if isinstance(other, Value):
            return self.update_time == other.update_time and self.payload == other.payload
        return False

    def __hash__(self):
        return hash(self.update_time) + hash(self.payload)

    def __repr__(self):
        return f"Value:{self.update_time} {self.payload}"


class ValueFromXMLRPCDateTime(Value):
    def __init__(self, xml_rpc_value: dict):
        super().__init__(xml_rpc_value['update_time'], xml_rpc_value['payload'].data)

    def __hash__(self):
        return super.__hash__(super)

    def __eq__(self, other):
        return super().__eq__(other)


class StubValueFromValue:
    def __init__(self, value: Value):
        self.value = value

    def stub(self):
        print(self.value.payload)
        return StubValue(payload=self.value.payload)
