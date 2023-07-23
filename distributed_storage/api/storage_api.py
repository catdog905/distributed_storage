from concurrent.futures import ThreadPoolExecutor
from threading import Thread

import grpc
from distributed_storage.proto.data_transfer_api_pb2 import (
    GetValueResponse,
    StoreValueResponse
)
import distributed_storage.proto.data_transfer_api_pb2_grpc as service

from distributed_storage.storage.storage import Storage
from distributed_storage.storage_servers.interconnect_storage_server import ServerAlreadyStarted
from distributed_storage.storage.types.update_time import CurrentUpdateTime
from distributed_storage.storage.types.value import StubValueFromValue, Value
from distributed_storage.storage_servers.outside_storage import OutsideStorage

SERVER_ADDR = '0.0.0.0:1234'


class KeyValueService(service.KeyValueServiceServicer):
    def GetValue(self, request, context):
        key = request.key
        return GetValueResponse(key_found=True, value=StubValueFromValue(value=self.storage.get_value(key)).stub())

    def StoreValue(self, request, context):
        key = request.key
        value = request.value
        self.storage.store_value(key, Value(update_time=CurrentUpdateTime(), payload=value.payload))
        return StoreValueResponse(code=200, message=f"stored (k = {key}, v = {value})")

    def __init__(self, storage: Storage, slave_nodes: list[OutsideStorage]):
        self.storage = storage
        self.slave_nodes = slave_nodes


class StorageAPI:

    def __init__(self, server_addr, storage: Storage, slave_nodes: list[OutsideStorage]):
        self.server_addr = server_addr
        self.storage = storage
        self.server = None
        self.running_thread = None
        self.slave_nodes = slave_nodes

    def run(self):
        if self.server is not None:
            raise ServerAlreadyStarted()
        self.server = grpc.server(ThreadPoolExecutor(max_workers=10))
        service.add_KeyValueServiceServicer_to_server(KeyValueService(self.storage, self.slave_nodes), self.server)
        self.server.add_insecure_port(self.server_addr)
        self.server.start()
        self.running_thread = Thread(target=lambda server: server.wait_for_termination(), args=(self.server, )).start()