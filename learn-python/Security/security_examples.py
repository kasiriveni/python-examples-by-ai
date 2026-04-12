# Security examples: hashing and reading secrets from env
import os
import hashlib

password = 's3cr3t'
h = hashlib.sha256(password.encode()).hexdigest()
print('SHA256:', h)

# Read secret from environment (set with: set MY_SECRET=... on Windows)
print('MY_SECRET:', os.getenv('MY_SECRET'))
