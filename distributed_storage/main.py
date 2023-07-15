from distributed_storage.storage.dictionary_storage import DictionaryStorage
from distributed_storage.storage_api import StorageAPI
from distributed_storage.storage_servers.interconnect_storage_server import InterConnectStorageServer

if __name__ == '__main__':
    storage = DictionaryStorage()
    InterConnectStorageServer("node_1", storage).run()
    StorageAPI('0.0.0.0:1357', storage).run()
    while True:
        pass
