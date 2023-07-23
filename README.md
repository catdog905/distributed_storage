## How to run the project:

```bash
docker-compose up --build
```

To remove the cache:
```bash
docker-compose down  --volumes
```

# Using
You can use `client.py` in order to use the storage


# Synchronization
We need to synchronize databases -> consistency check.

## Problems:
  - server have already saved the value
  - other slaves have already saved the value
  - all slaves correctly saved the value, but there was problems with network etc

## Solution:
  - Don`t give up police. If the node does not respond it will recover. Just wait for it and block user.
  - When conflict appears choose a latest and become master
  - Commit by getting approve from the more than half devices and get a value asked more than a half of devices
