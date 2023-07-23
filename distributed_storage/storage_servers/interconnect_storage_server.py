from threading import Thread
from xmlrpc.server import SimpleXMLRPCServer

from distributed_storage.environment_variables.EnvironmentVariable import EnvironmentVariable
from distributed_storage.storage.storage import Storage
from distributed_storage.storage.types.value import ValueFromXMLRPCDateTime


class ServerAlreadyStarted(Exception):
    pass


class XMLRPCStorageServer:
    def __init__(self, node_name, storage: Storage):
        self.node_name = node_name
        self.storage = storage

    def get_value(self, key: str):
        return self.storage.get_value(key)

    def store_value(self, key: str, value: dict):
        self.storage.store_value(key, ValueFromXMLRPCDateTime(value))

        print(f"Request to store key={key}; value={value} from another node; type_value={type(value['payload'].data)}")
        return True


class InterConnectStorageServer:

    def __init__(self, xml_port: EnvironmentVariable, storage: Storage):
        self.xml_port = xml_port
        self.storage = storage
        self.running_thread = None
        self.server = None

    def run(self):
        if self.running_thread is not None:
            raise ServerAlreadyStarted()
        self.server = SimpleXMLRPCServer(('0.0.0.0', self.xml_port.value()), logRequests=False)
        self.server.register_introspection_functions()
        self.server.register_instance(XMLRPCStorageServer(self.xml_port, self.storage))
        self.running_thread = Thread(target=lambda server: server.serve_forever(), args=(self.server,)).start()
