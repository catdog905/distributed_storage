from distributed_storage.environment_variables.ExposedGrpcPort import ExposedGrpcPort
from distributed_storage.environment_variables.InnerXmlRpcPort import InnerXmlRpcPort
from distributed_storage.environment_variables.OtherNodesPorts import OtherNodesPorts
from distributed_storage.storage.low_consistent_master_storage import LowConsistentStorage
from distributed_storage.storage_servers.outside_storage import OutsideStorage
from storage.dictionary_storage import DictionaryStorage
from distributed_storage.api.storage_api import StorageAPI
from storage_servers.interconnect_storage_server import InterConnectStorageServer

if __name__ == '__main__':
    storage = DictionaryStorage()
    consistent_storage = LowConsistentStorage(
        storage, [OutsideStorage(OtherNodesPorts().value()[0], InnerXmlRpcPort())]
    )
    InterConnectStorageServer(InnerXmlRpcPort(), storage).run()
    StorageAPI(
        f'0.0.0.0:{ExposedGrpcPort().value()}',
        consistent_storage,
        [OutsideStorage(OtherNodesPorts().value()[0], InnerXmlRpcPort())]
    ).run()
    while True:
        pass
