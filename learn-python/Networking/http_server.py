"""
Networking: HTTP server from scratch.
"""
import socket
import json
from datetime import datetime
from urllib.parse import urlparse, parse_qs

# === Simple HTTP Server ===
class SimpleHTTPServer:
    """Minimal HTTP server for educational purposes."""

    def __init__(self, host="127.0.0.1", port=8080):
        self.host = host
        self.port = port
        self.routes = {}

    def route(self, path, methods=None):
        """Decorator to register routes."""
        methods = methods or ["GET"]
        def decorator(func):
            self.routes[path] = {"handler": func, "methods": methods}
            return func
        return decorator

    def parse_request(self, data):
        """Parse raw HTTP request."""
        lines = data.decode().split("\r\n")
        method, path, version = lines[0].split(" ", 2)

        headers = {}
        body_start = 0
        for i, line in enumerate(lines[1:], 1):
            if line == "":
                body_start = i + 1
                break
            key, _, value = line.partition(": ")
            headers[key.lower()] = value

        body = "\r\n".join(lines[body_start:]) if body_start else ""
        parsed_url = urlparse(path)

        return {
            "method": method,
            "path": parsed_url.path,
            "query": parse_qs(parsed_url.query),
            "headers": headers,
            "body": body,
            "version": version,
        }

    def build_response(self, status_code, body, content_type="text/html"):
        """Build HTTP response."""
        status_messages = {200: "OK", 201: "Created", 404: "Not Found",
                          405: "Method Not Allowed", 500: "Internal Server Error"}
        status = f"{status_code} {status_messages.get(status_code, 'Unknown')}"

        if isinstance(body, dict):
            body = json.dumps(body)
            content_type = "application/json"

        response = f"HTTP/1.1 {status}\r\n"
        response += f"Content-Type: {content_type}\r\n"
        response += f"Content-Length: {len(body)}\r\n"
        response += f"Date: {datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')}\r\n"
        response += f"Connection: close\r\n"
        response += f"\r\n{body}"
        return response.encode()

    def handle_request(self, data):
        """Process request and return response."""
        try:
            request = self.parse_request(data)
            route = self.routes.get(request["path"])

            if not route:
                return self.build_response(404, {"error": "Not Found"})

            if request["method"] not in route["methods"]:
                return self.build_response(405, {"error": "Method Not Allowed"})

            result = route["handler"](request)
            return self.build_response(200, result)

        except Exception as e:
            return self.build_response(500, {"error": str(e)})

    def start(self):
        """Start the server (call to actually run)."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind((self.host, self.port))
            server.listen(5)
            print(f"Server running on http://{self.host}:{self.port}")

            while True:
                client, addr = server.accept()
                with client:
                    data = client.recv(4096)
                    if data:
                        response = self.handle_request(data)
                        client.sendall(response)

# === Demo (without actually starting) ===
if __name__ == "__main__":
    server = SimpleHTTPServer()

    @server.route("/")
    def home(request):
        return {"message": "Welcome to the HTTP server!", "time": str(datetime.now())}

    @server.route("/api/data", methods=["GET", "POST"])
    def api_data(request):
        if request["method"] == "POST":
            return {"created": request["body"]}
        return {"data": [1, 2, 3], "query": request["query"]}

    # Test the request parsing
    print("=== HTTP Request Parsing ===")
    raw_request = b"GET /api/data?page=1&limit=10 HTTP/1.1\r\nHost: localhost\r\nAccept: application/json\r\n\r\n"
    parsed = server.parse_request(raw_request)
    print(f"Method: {parsed['method']}")
    print(f"Path: {parsed['path']}")
    print(f"Query: {parsed['query']}")
    print(f"Headers: {parsed['headers']}")

    # Test response building
    print("\n=== HTTP Response ===")
    response = server.handle_request(raw_request)
    print(response.decode()[:300])

    print("\n=== Route Test ===")
    home_req = b"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n"
    resp = server.handle_request(home_req)
    print(resp.decode()[:200])

    print("\n# To run server: uncomment server.start() and visit http://localhost:8080")