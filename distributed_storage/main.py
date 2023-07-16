from argparse import ArgumentParser

from distributed_storage.storage_servers.outside_storage_server import OutsideStorageServer
from storage.dictionary_storage import DictionaryStorage
from storage_api import StorageAPI
from storage_servers.interconnect_storage_server import InterConnectStorageServer

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('rpc_port', type=int)
    parser.add_argument('xml_port', type=int)
    parser.add_argument('other_node_port', type=int)
    args = parser.parse_args()
    storage = DictionaryStorage()
    print(f'rpc_port={args.rpc_port}, xml_port={args.xml_port}, other_node_port={args.other_node_port}')
    InterConnectStorageServer(args.xml_port, storage).run()
    StorageAPI(f'0.0.0.0:{args.rpc_port}', storage, [OutsideStorageServer(args.other_node_port)]).run()
    while True:
        pass
