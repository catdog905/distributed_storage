from distributed_storage.storage.types.update_time import CurrentUpdateTime
from distributed_storage.storage.types.value import Value

value = Value(update_time=CurrentUpdateTime(), payload=b'hello')
print(hash(value))
