"""
Networking: TCP, UDP, HTTP clients, and socket programming.
"""
import socket
import threading
import time
import json
import urllib.request
import urllib.parse
import urllib.error
import http.server
from typing import Callable

# ═══════════════════════════════════════════
# 1. TCP Server and Client
# ═══════════════════════════════════════════
class EchoServer:
    """Threaded TCP echo server."""

    def __init__(self, host: str = "127.0.0.1", port: int = 0):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind((host, port))
        self._sock.listen(5)
        self.host, self.port = self._sock.getsockname()
        self._running = False

    def start(self) -> None:
        self._running = True
        threading.Thread(target=self._accept_loop, daemon=True).start()

    def stop(self) -> None:
        self._running = False
        self._sock.close()

    def _accept_loop(self) -> None:
        while self._running:
            try:
                conn, addr = self._sock.accept()
                threading.Thread(target=self._handle, args=(conn,), daemon=True).start()
            except OSError:
                break

    def _handle(self, conn: socket.socket) -> None:
        with conn:
            while True:
                data = conn.recv(4096)
                if not data: break
                conn.sendall(data)   # echo back

def tcp_client_send(host: str, port: int, messages: list[str]) -> list[str]:
    responses = []
    with socket.create_connection((host, port), timeout=5) as sock:
        for msg in messages:
            sock.sendall(msg.encode())
            responses.append(sock.recv(4096).decode())
    return responses

# ═══════════════════════════════════════════
# 2. UDP messaging
# ═══════════════════════════════════════════
class UDPServer:
    def __init__(self, host: str = "127.0.0.1", port: int = 0):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.bind((host, port))
        self._sock.settimeout(1.0)
        self.host, self.port = self._sock.getsockname()
        self.received: list[str] = []

    def receive_one(self) -> str | None:
        try:
            data, _ = self._sock.recvfrom(4096)
            msg = data.decode()
            self.received.append(msg)
            return msg
        except socket.timeout:
            return None

    def close(self): self._sock.close()

def udp_send(host: str, port: int, message: str) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(message.encode(), (host, port))

# ═══════════════════════════════════════════
# 3. HTTP client (stdlib urllib)
# ═══════════════════════════════════════════
def http_get(url: str, headers: dict | None = None, timeout: float = 10) -> dict:
    req = urllib.request.Request(url, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return {"status": resp.status, "body": resp.read().decode("utf-8", errors="replace")}
    except urllib.error.HTTPError as e:
        return {"status": e.code, "error": str(e)}
    except urllib.error.URLError as e:
        return {"status": 0, "error": str(e.reason)}

def http_post_json(url: str, payload: dict, timeout: float = 10) -> dict:
    body = json.dumps(payload).encode()
    req = urllib.request.Request(
        url, data=body,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return {"status": resp.status, "body": json.loads(resp.read().decode())}
    except urllib.error.HTTPError as e:
        return {"status": e.code, "error": str(e)}
    except urllib.error.URLError as e:
        return {"status": 0, "error": str(e.reason)}

def build_url(base: str, path: str = "", **params) -> str:
    url = base.rstrip("/") + ("/" + path.lstrip("/") if path else "")
    if params:
        url += "?" + urllib.parse.urlencode(params)
    return url

# ═══════════════════════════════════════════
# 4. Mini HTTP server
# ═══════════════════════════════════════════
class JSONHandler(http.server.BaseHTTPRequestHandler):
    routes: dict[tuple, Callable] = {}
    def log_message(self, *_): pass

    def do_GET(self):
        handler = self.routes.get(("GET", self.path))
        if handler:
            body = json.dumps(handler()).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_error(404)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body   = json.loads(self.rfile.read(length)) if length else {}
        handler = self.routes.get(("POST", self.path))
        if handler:
            response = json.dumps(handler(body)).encode()
            self.send_response(201)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(response)
        else:
            self.send_error(404)

def start_test_server() -> http.server.HTTPServer:
    server = http.server.HTTPServer(("127.0.0.1", 0), JSONHandler)
    JSONHandler.routes[("GET",  "/health")] = lambda: {"status": "ok"}
    JSONHandler.routes[("GET",  "/users")]  = lambda: [{"id": 1, "name": "Alice"}]
    JSONHandler.routes[("POST", "/echo")]   = lambda body: {"echoed": body}
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server

# ═══════════════════════════════════════════
# 5. Socket utilities
# ═══════════════════════════════════════════
def is_port_open(host: str, port: int, timeout: float = 1.0) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout): return True
    except (socket.timeout, ConnectionRefusedError, OSError): return False

def local_ip() -> str:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]

def hostname() -> str: return socket.gethostname()

def resolve(host: str) -> list[str]:
    try:
        info = socket.getaddrinfo(host, None, socket.AF_INET)
        return list({entry[4][0] for entry in info})
    except socket.gaierror as e:
        return [f"Error: {e}"]

# ═══════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════
if __name__ == "__main__":
    print("=== TCP Echo Server ===")
    srv = EchoServer(); srv.start()
    for r in tcp_client_send(srv.host, srv.port, ["Hello!", "Python networking"]):
        print(f"  Echo: {r!r}")
    srv.stop()

    print("\n=== UDP Messaging ===")
    udp_srv = UDPServer()
    udp_send(udp_srv.host, udp_srv.port, "Hello UDP!")
    time.sleep(0.05)
    msg = udp_srv.receive_one()
    print(f"  Received: {msg!r}")
    udp_srv.close()

    print("\n=== Mini HTTP Server ===")
    http_srv = start_test_server()
    base = f"http://127.0.0.1:{http_srv.server_address[1]}"
    for path, method, payload in [
        ("/health", "GET",  None),
        ("/users",  "GET",  None),
        ("/echo",   "POST", {"msg": "test"}),
    ]:
        if method == "GET":
            resp = http_get(f"{base}{path}")
        else:
            resp = http_post_json(f"{base}{path}", payload)
        print(f"  {method} {path} → {resp['status']} {str(resp.get('body',''))[:60]}")
    http_srv.shutdown()

    print("\n=== URL Builder ===")
    print(f"  {build_url('https://api.example.com', 'search', q='python', page=2)}")

    print("\n=== Socket Info ===")
    print(f"  Hostname: {hostname()}")
    print(f"  Local IP: {local_ip()}")
    print(f"  Port 9999 open on localhost: {is_port_open('127.0.0.1', 9999)}")
    print(f"  Resolve 'localhost': {resolve('localhost')}")
