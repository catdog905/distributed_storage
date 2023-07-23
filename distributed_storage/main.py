from redis.cluster import ClusterNode

from distributed_storage.environment_variables.ExposedGrpcPort import ExposedGrpcPort
from distributed_storage.environment_variables.InnerXmlRpcPort import InnerXmlRpcPort
from distributed_storage.environment_variables.OtherNodes import OtherNodes
from distributed_storage.environment_variables.redis_nodes_suffix import RedisNodesSuffix
from distributed_storage.storage.redis_storage import RedisStorage
from distributed_storage.storage.weakly_consistent_storage import WeaklyConsistentStorage
from distributed_storage.storage.outside_storage import OutsideStorage
from storage.dictionary_storage import DictionaryStorage
from distributed_storage.api.user_storage_api import StorageAPI
from distributed_storage.api.interconnect_storage_api import InterConnectStorageServer

if __name__ == '__main__':
    redis_nodes_suffix = str(RedisNodesSuffix())
    storage = RedisStorage(
        startup_nodes=[ClusterNode(host="redis-node-1" + redis_nodes_suffix, port=6379),
                       ClusterNode(host="redis-node-2" + redis_nodes_suffix, port=6379),
                       ])
    #storage = DictionaryStorage()
    outside_storages = [
        OutsideStorage(OtherNodes().value()[0], InnerXmlRpcPort()),
        OutsideStorage(OtherNodes().value()[1], InnerXmlRpcPort())]
    consistent_storage = WeaklyConsistentStorage(
        storage_nodes=[storage, outside_storages[0], outside_storages[1]]
    )
    InterConnectStorageServer(InnerXmlRpcPort(), storage, consistent_storage).run()
    StorageAPI(
        f'0.0.0.0:{ExposedGrpcPort().value()}',
        consistent_storage
    ).run()
    while True:
        pass
