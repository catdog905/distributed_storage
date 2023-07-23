import unittest
from unittest.mock import MagicMock

from distributed_storage.storage_api import KeyValueService, StorageAPI
from distributed_storage.data_transfer_api_pb2 import (
    GetValueRequest,
    StoreValueRequest,
    Value
)


class TestKeyValueService(unittest.TestCase):
    def setUp(self):
        self.storage = MagicMock()
        self.slave_nodes = [MagicMock(), MagicMock()]
        self.key_value_service = KeyValueService(self.storage, self.slave_nodes)

    def test_get_value_key_found(self):
        key = 'test_key'
        payload = b'dfsdf'
        value = Value()
        value.payload = payload
        self.storage.contains.return_value = True
        self.storage.get_value.return_value = value
        request = GetValueRequest()
        request.key = key
        result = self.key_value_service.GetValue(request=request, context=None)
        self.assertTrue(result.key_found)
        self.assertEqual(result.value, value)

    def test_get_value_key_not_found(self):
        key = 'test_key'
        self.storage.contains.return_value = False
        request = GetValueRequest()
        request.key = key
        result = self.key_value_service.GetValue(request=request, context=None)
        self.assertFalse(result.key_found)

    def test_store_value(self):
        key = 'test_key'
        payload = b'sdfdsf'
        value = Value(payload=payload)

        request = StoreValueRequest(key=key, value=value)

        self.key_value_service.StoreValue(request=request, context=None)

        args, kwargs = self.storage.store_value.call_args
        self.assertEqual(args[0], key)
        self.assertEqual(args[1].payload, value.payload)

        self.storage.store_value.assert_called_once_with(
            key, unittest.mock.ANY
        )

        for slave_node in self.slave_nodes:
            args, kwargs = self.storage.store_value.call_args
            self.assertEqual(args[0], key)
            self.assertEqual(args[1].payload, value.payload)

            slave_node.store_value.assert_called_once_with(
                key, unittest.mock.ANY
            )


class TestStorageAPI(unittest.TestCase):

    def setUp(self):
        self.server_addr = '0.0.0.0:1234'
        self.storage = MagicMock()
        self.slave_nodes = [MagicMock(), MagicMock()]
        self.storage_api = StorageAPI(self.server_addr, self.storage, self.slave_nodes)

    def test_run(self):

        with unittest.mock.patch('grpc.server'):
            with unittest.mock.patch('threading.Thread.start', new=MagicMock()) as mock_thread:
                self.storage_api.run()
                self.storage_api.server.add_insecure_port.assert_called_once_with(self.server_addr)
                self.storage_api.server.start.assert_called_once()
                mock_thread.assert_called_once()


if __name__ == '__main__':
    unittest.main()
