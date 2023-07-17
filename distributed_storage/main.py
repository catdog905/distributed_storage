from argparse import ArgumentParser

import os

from distributed_storage.environment_variables.ExposedGrpcPort import ExposedGrpcPort
from distributed_storage.environment_variables.InnerXmlRpcPort import InnerXmlRpcPort
from distributed_storage.environment_variables.OtherNodesPorts import OtherNodesPorts
from distributed_storage.storage_servers.outside_storage_server import OutsideStorageServer
from storage.dictionary_storage import DictionaryStorage
from storage_api import StorageAPI
from storage_servers.interconnect_storage_server import InterConnectStorageServer

if __name__ == '__main__':
    storage = DictionaryStorage()
    InterConnectStorageServer(InnerXmlRpcPort(), storage).run()
    StorageAPI(
        f'0.0.0.0:{ExposedGrpcPort().value()}',
        storage,
        [OutsideStorageServer(OtherNodesPorts().value()[0], InnerXmlRpcPort())]
    ).run()
    while True:
        pass
