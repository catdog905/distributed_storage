from threading import Thread
from xmlrpc.server import SimpleXMLRPCServer

from distributed_storage.environment_variables.EnvironmentVariable import EnvironmentVariable
from distributed_storage.storage.storage import Storage, NoSuchKeyInStoragePresent
from distributed_storage.storage.types.value import ValueFromXMLRPCDateTime


class ServerAlreadyStarted(Exception):
    pass


class XMLRPCStorageApi:
    def __init__(self, node_name, local_storage: Storage, distributed_storage: Storage):
        self.node_name = node_name
        self.local_storage = local_storage
        self.distributed_storage = distributed_storage

    def get_value(self, key: str):
        value = self.local_storage.get_value(key)
        print(f"got {key}:{value} in interconnect")
        return value

    def store_value(self, key: str, xmlValue: dict):
        value = ValueFromXMLRPCDateTime(xmlValue)
        try:
            existing_value = self.local_storage.get_value(key)
            print(f"stored {key}:{value} locally and in interconnect")
            if value.update_time < existing_value.update_time:
                Thread(target=self.distributed_storage.store_value, args=(key, value))
                return False
        except Exception:
            self.local_storage.store_value(key, value)
            print(f"stored {key}:{value} locally")
            return True


class InterConnectStorageServer:

    def __init__(self, xml_port: EnvironmentVariable, local_storage: Storage, distributed_storage: Storage):
        self.xml_port = xml_port
        self.local_storage = local_storage
        self.distributed_storage = distributed_storage
        self.running_thread = None
        self.server = None

    def run(self):
        if self.running_thread is not None:
            raise ServerAlreadyStarted()
        self.server = SimpleXMLRPCServer(('0.0.0.0', self.xml_port.value()), logRequests=False)
        self.server.register_introspection_functions()
        self.server.register_instance(XMLRPCStorageApi(self.xml_port, self.local_storage, self.distributed_storage))
        self.running_thread = Thread(target=lambda server: server.serve_forever(), args=(self.server,)).start()
