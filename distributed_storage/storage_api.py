import time
from concurrent.futures import ThreadPoolExecutor
from threading import Thread

import grpc
from data_transfer_api_pb2 import (
    GetValueResponse,
    Value as StubValue,
    StoreValueResponse
)
import data_transfer_api_pb2_grpc as service

from google.protobuf.timestamp_pb2 import Timestamp as StubTimestamp
from datetime import datetime

from distributed_storage.storage.storage import Storage
from distributed_storage.storage_servers.interconnect_storage_server import ServerAlreadyStarted
from distributed_storage.update_time import CurrentUpdateTime
from distributed_storage.value import StubValueFromValue, Value

SERVER_ADDR = '0.0.0.0:1234'


class KeyValueService(service.KeyValueServiceServicer):
    def GetValue(self, request, context):
        key = request.key
        if not self.storage.contains(key):
            return GetValueResponse(key_found=False)
        return GetValueResponse(key_found=True, value=StubValueFromValue(value=self.storage.get_value(key)).stub())

    def StoreValue(self, request, context):
        key = request.key
        value = request.value
        self.storage.store_value(key, Value(update_time=CurrentUpdateTime(), payload=value.payload))
        return StoreValueResponse(code=200, message=f"stored (k = {key}, v = {value})")

    def __init__(self, storage):
        self.storage = storage


class StorageAPI:

    def __init__(self, server_addr, storage: Storage):
        self.server_addr = server_addr
        self.storage = storage
        self.server = None
        self.running_thread = None

    def run(self):
        if self.server is not None:
            raise ServerAlreadyStarted()
        self.server = grpc.server(ThreadPoolExecutor(max_workers=10))
        service.add_KeyValueServiceServicer_to_server(KeyValueService(self.storage), self.server)
        self.server.add_insecure_port(self.server_addr)
        self.server.start()
        self.running_thread = Thread(target=lambda server: server.wait_for_termination(), args=(self.server, )).start()
