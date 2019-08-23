from grpclib import *
from hello.test import *

servers = [Server('test', '127.0.0.1', 6565)]
grpc_client.load(servers)

response = say(1, 'hello grpc!')
print(response)

response = error()
print(response)
