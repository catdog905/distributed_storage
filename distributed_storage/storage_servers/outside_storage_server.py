from xmlrpc.client import ServerProxy

from distributed_storage.value import Value


class OutsideStorageServer:

    def get_value(self, key: str) -> Value:
        with ServerProxy(f'http://node_{self.node_name}:{self.port}') as node:
            return node.get_value(key)

    def store_value(self, key: str, value: Value):
        with ServerProxy(f'http://node_{self.node_name}:{self.port}') as node:
            node.store_value(key, value)

    def __init__(self, node_name, port):
        self.node_name = node_name
        self.port = port
