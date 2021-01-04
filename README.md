# Example implementations of a simple networking protocol.

This repo houses a Python implementation of a wrapper for a simple socket protocol. It utilizes `SOCK_STREAM` sockets, and address type is inferred at initialization, of either `SOCK_STREAM` or `AF_UNIX`. Calls are blocking.

This repository is useful for reference and simple applications. I hope to update this with tests and other implementations in the future.

Should work for most message sizes.

Communication is one-way:

1. Server sends data length.
2. Client reads data length.
3. Server sends message (or messages.)
4. Client reads message (or messages.)

Specifically, the length of the data is formatted as a `signed long long int`, which should take 8 bytes.

## Example

### Server:

```
from simplest import SimplestServer
server = SimplestServer(('localhost', 6000))
# alternatively: server = SimplestServer('some_socket')
server.send(b'arbitrary data here')
```

### Client:

```
from simplest import SimplestServer
server = SimplestServer(('localhost', 6000))
# alternatively: server = SimplestServer('some_socket')
server.send(b'arbitrary data here')
```



## List of files

TODO

