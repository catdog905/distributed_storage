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

```bash
poetry run python distributed_storage/client.py
```