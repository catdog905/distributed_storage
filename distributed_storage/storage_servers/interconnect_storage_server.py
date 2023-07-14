from threading import Thread
from xmlrpc.server import SimpleXMLRPCServer

from distributed_storage.storage.storage import Storage
from distributed_storage.value import Value


class ServerAlreadyStarted(Exception):
    pass


class XMLRPCStorageServer:
    def __init__(self, node_name, storage: Storage):
        self.node_name = node_name
        self.storage = storage

    def get_value(self, key: str) -> Value:
        self.storage.get_value(key)

    def store_value(self, key: str, value: Value):
        self.storage.store_value(key, value)


class InterConnectStorageServer:

    def __init__(self, node_name, storage):
        self.node_name = node_name
        self.storage = storage
        self.running_thread = None
        self.server = None

    def run(self):
        if self.running_thread is not None:
            raise ServerAlreadyStarted()
        self.server = SimpleXMLRPCServer(('0.0.0.0', 1234), logRequests=False)
        self.server.register_introspection_functions()
        self.server.register_instance(XMLRPCStorageServer(self.node_name, self.storage))
        self.running_thread = Thread(target=lambda server: server.serve_forever(), args=(self.server,))
