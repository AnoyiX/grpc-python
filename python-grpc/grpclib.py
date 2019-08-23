#!/usr/bin/python
# -*- coding: UTF-8 -*-

import importlib
import json
import time
import logging
import sys
import traceback
from concurrent import futures

import grpc

import service_pb2
import service_pb2_grpc


class Logger:

    def __init__(self):
        logger = logging.getLogger('console')
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        log_format = '%(asctime)s  %(levelname)s %(process)d --- [%(threadName)+15s] %(module)-20s : %(message)s'
        formatter = logging.Formatter(log_format, datefmt='%Y-%m-%d %H:%M:%S.000')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        self.logger = logger


class Server:

    def __init__(self, server, host, port):
        self.server = server
        self.host = host
        self.port = port
        self.addr = host + ':' + str(port)


class CommonService(service_pb2_grpc.CommonServiceServicer):

    def handle(self, request, context):
        request_str = request.request.decode(encoding='utf-8')
        grpc_request = json.loads(request_str)
        response = {'status': 0}
        module = importlib.import_module(grpc_request.get('clazz'))
        invoke = getattr(module, grpc_request.get('method'))
        args = grpc_request.get('args')
        try:
            response['result'] = invoke(*args)
        except Exception as e:
            exc_type, exc_value, exc_tb = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_tb)
            response['status'] = -1
            response['message'] = e.args
            response['excType'] = exc_type.__name__

        return service_pb2.Response(response=json.dumps(response).encode(encoding="utf-8"))


class GrpcClient:

    def handle(self):
        pass

    def connect(self, server):
        """
        get server stub
        :param server:
        :return:
        """
        return self.stubs.get(server)

    def load(self, servers):
        """
        load grpc server list
        :param servers: Server
        :return:
        """
        for server in servers:
            channel = grpc.insecure_channel(server.addr)
            stub = service_pb2_grpc.CommonServiceStub(channel)
            self.stubs[server.server] = stub

    def __init__(self):
        self.stubs = {}


class GrpcServer:

    def run(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=self.max_workers))
        service_pb2_grpc.add_CommonServiceServicer_to_server(CommonService(), server)
        server.add_insecure_port(self.address)
        server.start()
        log.info('grpc server running, listen on ' + self.address)
        try:
            while True:
                time.sleep(60 * 60 * 24)
        except KeyboardInterrupt:
            server.stop(0)

    def __init__(self, host='0.0.0.0', port=6565, max_workers=10):
        self.address = host + ':' + str(port)
        self.max_workers = max_workers


class GrpcException(Exception):

    def __init__(self, exc_type, message):
        self.exc_type = exc_type
        self.message = message


def grpc_service(server, serialize=3):
    """
    grpc service define
    :param server: server name
    :param serialize: serialize type, default 3 : json
    :return:
    """
    def decorator(func):
        def wrapper(*args):
            request = {
                'clazz': func.__module__,
                'method': func.__name__,
                'args': list(args)
            }
            request_json = json.dumps(request, ensure_ascii=False)
            response = grpc_client.connect(server).handle(
                service_pb2.Request(request=bytes(request_json.encode('utf-8')), serialize=serialize))
            response_json = json.loads(response.response)
            if response_json.get('status') == 0:
                return response_json.get('result')
            elif response_json.get('status') == -1:
                raise GrpcException(response_json.get('excType'), response_json.get('message'))
            else:
                raise Exception('unknown grpc exception')
        return wrapper
    return decorator


log = Logger().logger
grpc_client = GrpcClient()
