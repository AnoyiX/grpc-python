python-grpc An Common Service RPC library
------
Based on `grpcio`，we define the common grpc service and function. By reflection & syntactic sugar，server side can provide rpc service easily, also client can declare rpc interface easily.

Project Path Description
------
- `client`: grpc client demo
- `server`: grpc server demo
- `python-grpc`: python-grpc core module

Tutorials
------

install python-grpc
```
pip3 install python-grpc
```

**Server Side**

run grpc server in path `server`
```
python3 server.py
```

**Client Side**

test grpc client in path `client`
```
python3 client.py
```

Common Service Define `service.proto`
--------
```
syntax = "proto3";

// Define Common Service
service CommonService {
    // common rpc function
    rpc handle ( Request ) returns ( Response ) {}
}

// Request Type
message Request {
    int32 serialize = 1;
    bytes request = 2;
}

// Response Type
message Response {
    bytes response = 1;
}
```