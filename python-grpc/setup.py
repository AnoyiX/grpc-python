from setuptools import setup

setup(
    name='python-grpc',
    version='0.0.2',
    description='common grpc service',
    author='Anoyi',
    author_email='545544032@qq.com',
    url='https://github.com/ChinaSilence/python-grpc',
    py_modules=['grpclib', 'service_pb2', 'service_pb2_grpc'],
    install_requires=['grpcio>=1.23.0']
)
