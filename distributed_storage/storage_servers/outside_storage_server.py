from xmlrpc.client import ServerProxy

from distributed_storage.environment_variables.InnerXmlRpcPort import InnerXmlRpcPort
from distributed_storage.storage.value import Value


class OutsideStorageServer:

    def get_value(self, key: str) -> Value:
        with ServerProxy(self.uri) as node:
            return node.get_value(key)

    def store_value(self, key: str, value: Value):
        with ServerProxy(self.uri) as node:
            print(value)
            node.store_value(key, value)

    def __init__(self, node_id, port: InnerXmlRpcPort):
        self.node_id = node_id
        self.port = port
        self.uri = f'http://distributed_storage_node_{self.node_id}:{self.port.value()}'
