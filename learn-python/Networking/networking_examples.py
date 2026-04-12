# Networking: sockets and HTTP requests (requests)
import socket

# simple TCP client example (connects to example.com:80)
try:
    s = socket.socket()
    s.settimeout(2)
    s.connect(('example.com', 80))
    s.sendall(b'GET / HTTP/1.0\r\nHost: example.com\r\n\r\n')
    data = s.recv(1024)
    print(data.splitlines()[0])
    s.close()
except Exception as e:
    print('socket error', e)

# HTTP via requests (requires requests package)
# import requests
# r = requests.get('https://api.github.com')
# print(r.status_code)
