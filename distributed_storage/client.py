import grpc

import distributed_storage.proto.data_transfer_api_pb2 as service
import distributed_storage.proto.data_transfer_api_pb2_grpc as stub


def put(key):
    args = service.StoreValueRequest(key=key,
                                     value=service.Value(payload=b"value1"))
    response = stub.StoreValue(args)
    print(f"{response.code}:{response.message}")


def get(key):
    args = service.GetValueRequest(key=key)
    response = stub.GetValue(args)
    return response.value.payload


if __name__ == '__main__':
    with grpc.insecure_channel('localhost:1234') as channel:
        stub = stub.KeyValueServiceStub(channel)
        #put("6")
        print(get("6"))
