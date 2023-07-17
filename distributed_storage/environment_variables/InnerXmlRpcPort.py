import os

from distributed_storage.environment_variables.EnvironmentVariable import EnvironmentVariable


class InnerXmlRpcPort(EnvironmentVariable):
    def value(self):
        return int(os.getenv('XMLRPC_PORT'))
