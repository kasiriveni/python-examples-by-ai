"""
Security Best Practices: OWASP Top 10 prevention examples.
"""
import html
import re
import hashlib
import secrets
import hmac
from urllib.parse import urlparse

# === 1. SQL Injection Prevention ===
print("=== SQL Injection Prevention ===")

# BAD: String formatting (vulnerable)
def bad_query(user_input):
    return f"SELECT * FROM users WHERE name = '{user_input}'"

# GOOD: Parameterized queries
def good_query(user_input):
    """Use parameterized queries (shown as template)."""
    query = "SELECT * FROM users WHERE name = ?"
    params = (user_input,)
    return query, params

malicious = "'; DROP TABLE users; --"
print(f"BAD:  {bad_query(malicious)}")
print(f"GOOD: {good_query(malicious)}")

# === 2. XSS Prevention ===
print("\n=== XSS Prevention ===")

def sanitize_html(user_input):
    return html.escape(user_input)

xss_attempt = '<script>alert("XSS")</script>'
print(f"Input:     {xss_attempt}")
print(f"Sanitized: {sanitize_html(xss_attempt)}")

# === 3. Password Hashing ===
print("\n=== Password Hashing ===")

def hash_password(password):
    salt = secrets.token_hex(16)
    hash_val = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100_000)
    return f"{salt}${hash_val.hex()}"

def verify_password(password, stored):
    salt, hash_val = stored.split('$')
    new_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100_000)
    return hmac.compare_digest(new_hash.hex(), hash_val)

stored = hash_password("mypassword123")
print(f"Stored: {stored[:40]}...")
print(f"Verify correct:   {verify_password('mypassword123', stored)}")
print(f"Verify incorrect: {verify_password('wrongpassword', stored)}")

# === 4. Input Validation ===
print("\n=== Input Validation ===")

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_url(url, allowed_schemes=('https',)):
    parsed = urlparse(url)
    return parsed.scheme in allowed_schemes and bool(parsed.netloc)

emails = ["valid@example.com", "bad@", "injection@evil.com<script>"]
for e in emails:
    print(f"  {e:35s} valid={validate_email(e)}")

urls = ["https://example.com", "http://evil.com", "javascript:alert(1)"]
for u in urls:
    print(f"  {u:35s} valid={validate_url(u)}")

# === 5. CSRF Token ===
print("\n=== CSRF Token ===")

def generate_csrf_token():
    return secrets.token_urlsafe(32)

def validate_csrf(session_token, form_token):
    return hmac.compare_digest(session_token, form_token)

token = generate_csrf_token()
print(f"Token: {token[:20]}...")
print(f"Valid:   {validate_csrf(token, token)}")
print(f"Invalid: {validate_csrf(token, 'fake-token')}")

# === 6. Rate Limiting ===
print("\n=== Simple Rate Limiter ===")

from collections import defaultdict
import time

class RateLimiter:
    def __init__(self, max_requests, window_seconds):
        self.max_requests = max_requests
        self.window = window_seconds
        self.requests = defaultdict(list)

    def is_allowed(self, client_id):
        now = time.time()
        # Clean old requests
        self.requests[client_id] = [
            t for t in self.requests[client_id] if now - t < self.window
        ]
        if len(self.requests[client_id]) >= self.max_requests:
            return False
        self.requests[client_id].append(now)
        return True

limiter = RateLimiter(max_requests=3, window_seconds=1)
for i in range(5):
    allowed = limiter.is_allowed("user1")
    print(f"  Request {i+1}: {'allowed' if allowed else 'BLOCKED'}")
