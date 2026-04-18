# Core Python Concepts

## Core Themes
- Cryptographic patterns and safer secret management.
- Input validation, XSS and SQL-injection prevention.
- Rate limiting and OWASP-oriented defensive patterns.

## Core Theme Examples
- Example 1: PBKDF2 key derivation with random salts.
- Example 2: Parameterized SQL and HTML escaping for XSS prevention.
- Example 3: Token-bucket and sliding-window rate limiters.

## Files and Concepts
- cryptography_patterns.py: hashing, PBKDF2 with salts, HMAC authenticators, OTP-style tokens
- input_validation.py: email, URL, identifier validation, HTML escaping, parameterized SQL thinking
- owasp_prevention.py: SQL-injection prevention, XSS sanitization, CSRF tokens, rate limiting
- rate_limiting.py: fixed-window, sliding-window, token-bucket, leaky-bucket limiters
- secrets_management.py: env-based secret loading, dotenv parsing, secret-pattern detection

## Core Example
This example validates input and enforces a simple rate limit.

```python
from collections import defaultdict

requests = defaultdict(int)

def allow(user, username):
	if not username.isalnum():
		return False
	requests[user] += 1
	return requests[user] <= 3

print(allow("alice", "Alice1"))
```
