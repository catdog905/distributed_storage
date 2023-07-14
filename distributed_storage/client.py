from threading import Thread

import grpc

import data_transfer_api_pb2 as service
import data_transfer_api_pb2_grpc as stub

from google.protobuf.timestamp_pb2 import Timestamp


def put(key):
    args = service.StoreValueRequest(key=key, value=service.Value(update_time=Timestamp().GetCurrentTime(), payload=b"value1"))
    response = stub.StoreValue(args)
    print(f"{response.code}:{response.message}")


def get(key):
    args = service.GetValueRequest(key=key)
    response = stub.GetValue(args)
    print(f'{response.key_found}, {response.value.update_time}, {response.value.payload}')


def delete_user(user_id):
    args = service.User(user_id=user_id)
    response = stub.DeleteUser(args)
    print(f"DeleteUser({user_id}) = {response.status}")


if __name__ == '__main__':
    with grpc.insecure_channel('localhost:1234') as channel:
        stub = stub.KeyValueServiceStub(channel)
        put("2")
        thread = Thread(target=get, args=("2",))
        thread.start()
        get("3")
