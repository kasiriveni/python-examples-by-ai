"""
Security best practices in Python.
"""
import secrets
import hashlib
import hmac
import os
import html
import re

# === Secure random generation ===
print("=== Secure Random ===")
# Use secrets module instead of random for security
token = secrets.token_hex(32)
url_token = secrets.token_urlsafe(32)
random_bytes = secrets.token_bytes(16)
print(f"Token: {token}")
print(f"URL-safe: {url_token}")
print(f"Random int (0-99): {secrets.randbelow(100)}")

# Secure password generation
alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%"
password = ''.join(secrets.choice(alphabet) for _ in range(16))
print(f"Generated password: {password}")

# === HMAC for message authentication ===
print("\n=== HMAC ===")
key = secrets.token_bytes(32)
message = b"Important message"
mac = hmac.new(key, message, hashlib.sha256).hexdigest()
print(f"HMAC: {mac}")

# Verify (timing-safe comparison)
received_mac = mac
is_valid = hmac.compare_digest(mac, received_mac)
print(f"Valid: {is_valid}")

# === Input sanitization ===
print("\n=== Input Sanitization ===")

# HTML escaping (prevent XSS)
user_input = '<script>alert("XSS")</script>'
safe_output = html.escape(user_input)
print(f"Escaped HTML: {safe_output}")

# SQL injection prevention (use parameterized queries)
def safe_query_example():
    """Always use parameterized queries, never string formatting."""
    # WRONG: f"SELECT * FROM users WHERE name = '{user_input}'"
    # RIGHT: cursor.execute("SELECT * FROM users WHERE name = ?", (user_input,))
    print("  Always use parameterized queries for SQL!")

safe_query_example()

# Path traversal prevention
def safe_file_path(base_dir, filename):
    """Prevent directory traversal attacks."""
    # Resolve the full path
    base = os.path.realpath(base_dir)
    filepath = os.path.realpath(os.path.join(base_dir, filename))
    # Ensure it's within the base directory
    if not filepath.startswith(base):
        raise ValueError("Path traversal detected!")
    return filepath

try:
    safe_file_path("/app/data", "../../../etc/passwd")
except ValueError as e:
    print(f"  Blocked: {e}")

# === Environment variable management ===
print("\n=== Environment Variables ===")
# Never hardcode secrets - use environment variables
api_key = os.environ.get("API_KEY", "not_set")
print(f"API_KEY from env: {'***' if api_key != 'not_set' else 'not_set'}")

# === Constant-time comparison ===
print("\n=== Constant Time Comparison ===")
# Always use hmac.compare_digest for comparing secrets
secret1 = b"my_secret_token"
secret2 = b"my_secret_token"
secret3 = b"wrong_token"
print(f"Match: {hmac.compare_digest(secret1, secret2)}")
print(f"No match: {hmac.compare_digest(secret1, secret3)}")

# === Input validation ===
print("\n=== Input Validation ===")

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_integer(value, min_val=None, max_val=None):
    try:
        n = int(value)
        if min_val is not None and n < min_val:
            return False
        if max_val is not None and n > max_val:
            return False
        return True
    except (ValueError, TypeError):
        return False

print(f"Valid email: {validate_email('user@example.com')}")
print(f"Invalid email: {validate_email('not-an-email')}")
print(f"Valid int: {validate_integer('42', 0, 100)}")
print(f"Invalid int: {validate_integer('abc')}")

# === Hashing passwords ===
print("\n=== Password Hashing (hashlib) ===")
def hash_password_pbkdf2(password, salt=None):
    if salt is None:
        salt = os.urandom(16)
    key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100_000)
    return salt + key

def verify_password_pbkdf2(password, stored):
    salt = stored[:16]
    expected = hash_password_pbkdf2(password, salt)
    return hmac.compare_digest(stored, expected)

stored = hash_password_pbkdf2("my_secure_password")
print(f"Password hash length: {len(stored)} bytes")
print(f"Verify correct: {verify_password_pbkdf2('my_secure_password', stored)}")
print(f"Verify wrong: {verify_password_pbkdf2('wrong_password', stored)}")
