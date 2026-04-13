"""
Example of secure password hashing using bcrypt.
"""
from bcrypt import hashpw, gensalt, checkpw

def hash_password(password):
    return hashpw(password.encode(), gensalt())

def verify_password(password, hashed):
    return checkpw(password.encode(), hashed)

if __name__ == "__main__":
    password = "securepassword123"
    hashed = hash_password(password)
    print(f"Hashed password: {hashed}")

    is_valid = verify_password(password, hashed)
    print(f"Password valid: {is_valid}")
