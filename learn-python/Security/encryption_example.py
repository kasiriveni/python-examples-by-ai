"""
Example of encrypting and decrypting data using Fernet symmetric encryption.
"""
from cryptography.fernet import Fernet

# Generate a key
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Encrypt data
data = b"Sensitive data"
encrypted_data = cipher_suite.encrypt(data)
print(f"Encrypted: {encrypted_data}")

# Decrypt data
decrypted_data = cipher_suite.decrypt(encrypted_data)
print(f"Decrypted: {decrypted_data.decode()}")
