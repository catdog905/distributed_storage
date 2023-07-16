from xmlrpc.client import ServerProxy

from distributed_storage.storage.value import Value


class OutsideStorageServer:

    def get_value(self, key: str) -> Value:
        with ServerProxy(f'http://localhost:{self.port}') as node:
            return node.get_value(key)

    def store_value(self, key: str, value: Value):
        with ServerProxy(f'http://localhost:{self.port}') as node:
            print(value)
            node.store_value(key, value)

    def __init__(self, port):
        self.port = port
