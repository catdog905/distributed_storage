from distributed_storage.environment_variables.ExposedGrpcPort import ExposedGrpcPort
from distributed_storage.environment_variables.InnerXmlRpcPort import InnerXmlRpcPort
from distributed_storage.environment_variables.OtherNodesPorts import OtherNodesPorts
from distributed_storage.environment_variables.redis_nodes_suffix import RedisNodesSuffix
from distributed_storage.storage.redis_storage import RedisStorage
from distributed_storage.storage_servers.outside_storage_server import OutsideStorageServer
from storage_api import StorageAPI
from storage_servers.interconnect_storage_server import InterConnectStorageServer
from redis.cluster import ClusterNode

if __name__ == '__main__':
    redis_nodes_suffix = str(RedisNodesSuffix())
    print(redis_nodes_suffix)
    storage = RedisStorage(
        startup_nodes=[ClusterNode(host="redis-node-1"+redis_nodes_suffix, port=6379),
                       ClusterNode(host="redis-node-2"+redis_nodes_suffix, port=6379),
                       ClusterNode(host="redis-node-3"+redis_nodes_suffix, port=6379),
                       ClusterNode(host="redis-node-4"+redis_nodes_suffix, port=6379),
                       ClusterNode(host="redis-node-5"+redis_nodes_suffix, port=6379),
                       ClusterNode(host="redis-node-6"+redis_nodes_suffix, port=6379),
                       ])
    InterConnectStorageServer(InnerXmlRpcPort(), storage).run()
    StorageAPI(
        f'0.0.0.0:{ExposedGrpcPort().value()}',
        storage,
        [OutsideStorageServer(OtherNodesPorts().value()[0], InnerXmlRpcPort())]
    ).run()
    while True:
        pass
