# Core Python Concepts

## Core Themes
- Encryption, password hashing, and secure-secret handling.
- Input validation and safe comparisons.
- Common application-security building blocks in Python.

## Core Theme Examples
- Example 1: Bcrypt password hashing and secure verification.
- Example 2: Fernet symmetric encryption for sensitive data.
- Example 3: Constant-time signature comparison with hmac.

## Files and Concepts
- encryption_example.py: Fernet encryption, key generation, encrypt and decrypt operations
- input_validation_example.py: username validation, alphanumeric checks, length validation
- password_hashing_example.py: bcrypt hashing, password verification
- security_best_practices.py: secrets module, HMAC, HTML escaping, path-traversal prevention, constant-time comparison
- security_examples.py: SHA256 hashing, environment-variable handling

## Core Example
This example hashes a password-like value and compares signatures safely.

```python
import hashlib
import hmac

secret = b"token"
digest = hashlib.sha256(secret).hexdigest()
same = hmac.compare_digest(digest, hashlib.sha256(secret).hexdigest())

print(digest[:12])
print(same)
```
