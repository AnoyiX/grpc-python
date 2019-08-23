from grpclib import *


@grpc_service(server='test')
def say(count, message):
    pass


@grpc_service(server='test')
def error():
    pass
