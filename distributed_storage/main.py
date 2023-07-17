from argparse import ArgumentParser

import os
from distributed_storage.storage_servers.outside_storage_server import OutsideStorageServer
from storage.dictionary_storage import DictionaryStorage
from storage_api import StorageAPI
from storage_servers.interconnect_storage_server import InterConnectStorageServer

if __name__ == '__main__':
    parser = ArgumentParser()
    # parser.add_argument('rpc_port', type=int)
    # parser.add_argument('xml_port', type=int)
    parser.add_argument('other_node_id', type=int)
    args = parser.parse_args()
    storage = DictionaryStorage()

    xmlrpc_port = int(os.getenv('XMLRPC_PORT', 1234))
    grpc_port = int(os.getenv('GRPC_PORT', 1234))

    print(f'rpc_port={grpc_port}, xml_port={xmlrpc_port}, other_node_id={args.other_node_id}')
    InterConnectStorageServer(xmlrpc_port, storage).run()
    StorageAPI(f'0.0.0.0:{grpc_port}', storage, [OutsideStorageServer(args.other_node_id, xmlrpc_port)]).run()
    while True:
        pass
