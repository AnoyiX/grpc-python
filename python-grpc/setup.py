from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='python-grpc',
    version='0.0.6',
    description='common grpc service',
    author='Anoyi',
    author_email='545544032@qq.com',
    url='https://github.com/ChinaSilence/python-grpc',
    py_modules=['grpclib', 'service_pb2', 'service_pb2_grpc'],
    install_requires=['grpcio>=1.23.0', 'protobuf>=3.9.1'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
