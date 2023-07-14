from distributed_storage.value import Value


class OutsideStorageServer:

    def get_value(self, key: str) -> Value:
        raise NotImplementedError

    def store_value(self, key: str, value: Value):
        raise NotImplementedError

    def run(self):
        parser = ArgumentParser()
        parser.add_argument('node_id', type=int)
        args = parser.parse_args()
        with SimpleXMLRPCServer(('0.0.0.0', PORT), logRequests=False) as server:
            server.register_introspection_functions()
            server.register_instance(Node(args.node_id))
            try:
                server.serve_forever()
            except KeyboardInterrupt:
                print("Shutting down...")
