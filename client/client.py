from grpclib import *
from hello.test import *

servers = [Server('test', '127.0.0.1', 6565)]
grpc_client.load(servers)

for i in range(0, 10):
    response = say(i, 'hello grpc!')
    print(response)
