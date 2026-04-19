import hashlib

# Create a SHA-256 hash object
hash_obj = hashlib.sha256()

# Update with data (must be bytes)
hash_obj.update(b"Hello World")

# Get the hexadecimal digest
print(hash_obj.hexdigest())
# Output: a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e
