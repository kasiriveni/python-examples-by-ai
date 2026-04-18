# Core Python Concepts

## Core Themes
- Socket programming and client-server communication.
- HTTP request and response handling.
- TCP, UDP, and multithreaded server patterns.

## Core Theme Examples
- Example 1: Create client-server connections using socket pairs.
- Example 2: Parse HTTP headers and send response lines.
- Example 3: Build multithreaded servers for concurrent client handling.

## Files and Concepts
- http_client.py: URL parsing, HTTP request building, timeout handling
- http_server.py: HTTP request parsing, route registration, response building
- networking_examples.py: TCP sockets, UDP sockets, requests-based networking basics
- socket_programming.py: socket connections, echo server, threaded clients
- tcp_udp_http.py: TCP and UDP servers, multithreaded handlers, HTTP protocol basics

## Core Example
This example creates a local TCP socket and shows the server address.

```python
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 0))
server.listen(1)

host, port = server.getsockname()
print(host, port)
server.close()
```
