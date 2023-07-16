from threading import Thread

import grpc

import data_transfer_api_pb2 as service
import data_transfer_api_pb2_grpc as stub

from google.protobuf.timestamp_pb2 import Timestamp

from distributed_storage.storage.update_time import StubTimestampFromUpdateTime, CurrentUpdateTime


def put(key):
    args = service.StoreValueRequest(key=key,
                                     value=service.Value(payload=b"value1"))
    response = stub.StoreValue(args)
    print(f"{response.code}:{response.message}")


def get(key):
    args = service.GetValueRequest(key=key)
    response = stub.GetValue(args)
    return response.value.payload


if __name__ == '__main__':
    with grpc.insecure_channel('localhost:1234') as channel:
        stub = stub.KeyValueServiceStub(channel)
        put("2")
        print(get("2"))
