import time
from concurrent.futures import ThreadPoolExecutor

import grpc
from data_transfer_api_pb2 import (
    GetValueResponse,
    Value as StubValue,
    StoreValueResponse
)
import data_transfer_api_pb2_grpc as service

from google.protobuf.timestamp_pb2 import Timestamp as StubTimestamp
from datetime import datetime

from distributed_storage.update_time import CurrentUpdateTime
from distributed_storage.value import StubValueFromValue, Value

SERVER_ADDR = '0.0.0.0:1234'

storage = dict()


class StorageAPI(service.KeyValueServiceServicer):
    def GetValue(self, request, context):
        key = request.key
        print(key)
        if key not in storage:
            return GetValueResponse(key_found=False)
        return GetValueResponse(key_found=True, value=StubValueFromValue(value=storage[key]).stub())

    def StoreValue(self, request, context):
        key = request.key
        value = request.value
        storage[key] = Value(update_time=CurrentUpdateTime(), payload=value.payload)
        return StoreValueResponse(code=200, message=f"stored (k = {key}, v = {value})")


if __name__ == '__main__':
    try:
        server = grpc.server(ThreadPoolExecutor(max_workers=10))
        service.add_KeyValueServiceServicer_to_server(StorageAPI(), server)
        server.add_insecure_port(SERVER_ADDR)
        server.start()
        print(f"gRPC server is listening on {SERVER_ADDR}")
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(0)
        print("Shutting down...")
