"""
Socket programming basics in Python.
"""
import socket
import threading
import json

def echo_server(host='127.0.0.1', port=0):
    """Simple echo server that returns received messages."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)
    actual_port = server_socket.getsockname()[1]
    print(f"Server listening on {host}:{actual_port}")

    def handle_client(conn, addr):
        print(f"  Connected: {addr}")
        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                message = data.decode()
                print(f"  Received: {message}")
                conn.sendall(f"Echo: {message}".encode())
        finally:
            conn.close()
            print(f"  Disconnected: {addr}")

    return server_socket, actual_port

def echo_client(host, port, messages):
    """Send messages and receive echoes."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        for msg in messages:
            s.sendall(msg.encode())
            response = s.recv(1024).decode()
            print(f"  Sent: {msg} -> Got: {response}")

# UDP example
def udp_demo():
    """Simple UDP send/receive."""
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(('127.0.0.1', 0))
    port = server.getsockname()[1]

    # Send from client
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.sendto(b"Hello UDP!", ('127.0.0.1', port))

    # Receive on server
    data, addr = server.recvfrom(1024)
    print(f"  UDP received: {data.decode()} from {addr}")

    client.close()
    server.close()

# Socket info
def show_socket_info():
    """Display socket and network info."""
    hostname = socket.gethostname()
    print(f"Hostname: {hostname}")

    try:
        ip = socket.gethostbyname(hostname)
        print(f"IP Address: {ip}")
    except socket.gaierror:
        print("Could not resolve hostname")

    # DNS lookup
    try:
        addrs = socket.getaddrinfo("python.org", 443)
        print(f"python.org addresses: {len(addrs)} found")
        for addr in addrs[:2]:
            print(f"  {addr[4]}")
    except socket.gaierror:
        print("DNS lookup failed (no internet)")

if __name__ == "__main__":
    show_socket_info()

    print("\n--- TCP Echo Demo ---")
    server_socket, port = echo_server()

    def accept_one(server_socket):
        conn, addr = server_socket.accept()
        data = conn.recv(1024)
        conn.sendall(f"Echo: {data.decode()}".encode())
        conn.close()
        server_socket.close()

    t = threading.Thread(target=accept_one, args=(server_socket,))
    t.start()
    echo_client('127.0.0.1', port, ["Hello!"])
    t.join()

    print("\n--- UDP Demo ---")
    udp_demo()
