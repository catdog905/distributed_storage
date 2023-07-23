## How to run the project
Currently, docker compose does not works properly yet (problems with nodes visibility)

So, you can try this storage, started two storage processes:

```bash
poetry run python distributed_storage/main.py 1234 12345 22345
```

```bash
poetry run python distributed_storage/main.py 2234 22345 12345
```

Before the storage start you need to install all dependencies:
```bash
poetry install
```

Maybe you will be asked to install the following libraries (by this time I don't know why it is possible only by pip)
```bash
RUN pip install grpcio
RUN pip install protobuf
```

Check `Dockerfile`. It works

# Using
You can use `client.py` in order to use the storage


# Synchronization
We need to synchronize databases -> consistency check.

Scenarios:
- our service api fail to accept request from user. -> no problem. user should resubmit
- one slave down while saving/getting request from master/sending response to master
Problems:
  - server have already saved the value
  - other slaves have already saved the value
  - all slaves correctly saved the value, but there was problems with network etc
Solution:
  - Don`t give up police. If the node does not respond it will recover. Just wait for it and block user.
  - When conflict appears choose a latest and become master
  - Commit by getting approve from the more than half devices and get a value asked more than a half of devices