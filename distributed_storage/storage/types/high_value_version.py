from distributed_storage.storage.types.value import Value


class ValuesAreEmpty(Exception):
    def __str__(self):
        return "Values can not be empty"


class HighValueVersion:
    def high_value_version(self):
        return max(self.values, key=lambda x: x.update_time)

    def __init__(self, values: list[Value]):
        if len(values) == 0:
            raise ValuesAreEmpty()
        self.values = values
