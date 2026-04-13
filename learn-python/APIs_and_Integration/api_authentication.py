"""
API authentication examples.
"""
import hashlib
import hmac
import time
import json
import base64

# === API Key Authentication ===
print("=== API Key Auth ===")

class APIKeyAuth:
    def __init__(self):
        self._keys = {}

    def create_key(self, client_name):
        import secrets
        key = secrets.token_urlsafe(32)
        self._keys[key] = {"client": client_name, "created": time.time()}
        return key

    def verify(self, key):
        return key in self._keys

auth = APIKeyAuth()
key = auth.create_key("my-app")
print(f"API Key: {key[:20]}...")
print(f"Valid: {auth.verify(key)}")
print(f"Invalid: {auth.verify('fake-key')}")

# === Basic Auth ===
print("\n=== Basic Auth ===")

def create_basic_auth(username, password):
    credentials = f"{username}:{password}"
    encoded = base64.b64encode(credentials.encode()).decode()
    return f"Basic {encoded}"

def parse_basic_auth(header):
    if not header.startswith("Basic "):
        raise ValueError("Invalid Basic auth header")
    decoded = base64.b64decode(header[6:]).decode()
    username, password = decoded.split(":", 1)
    return username, password

header = create_basic_auth("admin", "secret123")
print(f"Header: {header}")
username, password = parse_basic_auth(header)
print(f"Parsed: user={username}, pass={'*' * len(password)}")

# === JWT-like Token ===
print("\n=== JWT-like Token ===")

class SimpleJWT:
    def __init__(self, secret):
        self._secret = secret.encode()

    def encode(self, payload):
        header = base64.urlsafe_b64encode(json.dumps({"alg": "HS256"}).encode()).decode()
        body = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode()
        signature = hmac.new(self._secret, f"{header}.{body}".encode(), hashlib.sha256).hexdigest()
        return f"{header}.{body}.{signature}"

    def decode(self, token):
        parts = token.split(".")
        if len(parts) != 3:
            raise ValueError("Invalid token")
        header, body, signature = parts
        expected = hmac.new(self._secret, f"{header}.{body}".encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(signature, expected):
            raise ValueError("Invalid signature")
        payload = json.loads(base64.urlsafe_b64decode(body))
        if "exp" in payload and payload["exp"] < time.time():
            raise ValueError("Token expired")
        return payload

jwt = SimpleJWT("my-secret-key")
token = jwt.encode({"user_id": 1, "role": "admin", "exp": time.time() + 3600})
print(f"Token: {token[:60]}...")

decoded = jwt.decode(token)
print(f"Decoded: {decoded}")

# === OAuth2-like flow ===
print("\n=== OAuth2 Flow (Simplified) ===")

class OAuth2Provider:
    def __init__(self):
        self._codes = {}
        self._tokens = {}

    def authorize(self, client_id, redirect_uri):
        import secrets
        code = secrets.token_urlsafe(16)
        self._codes[code] = {"client_id": client_id, "redirect_uri": redirect_uri}
        return f"{redirect_uri}?code={code}"

    def exchange_token(self, code, client_id, client_secret):
        if code not in self._codes:
            raise ValueError("Invalid authorization code")
        import secrets
        access_token = secrets.token_urlsafe(32)
        self._tokens[access_token] = {"client_id": client_id}
        del self._codes[code]
        return {"access_token": access_token, "token_type": "bearer"}

provider = OAuth2Provider()
redirect = provider.authorize("my-app", "https://myapp.com/callback")
print(f"Redirect: {redirect[:60]}...")

code = redirect.split("code=")[1]
tokens = provider.exchange_token(code, "my-app", "my-secret")
print(f"Access token: {tokens['access_token'][:20]}...")
