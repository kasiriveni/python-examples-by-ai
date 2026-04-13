"""
Security Best Practices: Cryptography patterns using only stdlib.
"""
import hashlib
import hmac
import os
import base64
import struct
import time
from typing import Tuple

# ═══════════════════════════════════════════
# 1. Hashing
# ═══════════════════════════════════════════
def hash_password(password: str, algorithm: str = "sha256") -> str:
    """
    Hash a string.
    NOTE: For real passwords use bcrypt/argon2 via passlib.
          This demonstrates the stdlib hash API only.
    """
    h = hashlib.new(algorithm)
    h.update(password.encode("utf-8"))
    return h.hexdigest()

def hash_file(path: str, algorithm: str = "sha256", chunk_size: int = 65536) -> str:
    """Hash a file's contents in chunks (memory-efficient)."""
    h = hashlib.new(algorithm)
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            h.update(chunk)
    return h.hexdigest()

def salted_hash(value: str, salt: bytes | None = None) -> Tuple[str, str]:
    """Hash with a random salt. Returns (hex_hash, hex_salt)."""
    if salt is None:
        salt = os.urandom(32)
    dk = hashlib.pbkdf2_hmac("sha256", value.encode(), salt, iterations=260_000)
    return base64.urlsafe_b64encode(dk).decode(), base64.urlsafe_b64encode(salt).decode()

def verify_salted_hash(value: str, hex_hash: str, hex_salt: str) -> bool:
    """Constant-time verification of a salted hash."""
    salt = base64.urlsafe_b64decode(hex_salt)
    computed, _ = salted_hash(value, salt)
    return hmac.compare_digest(computed, hex_hash)

# ═══════════════════════════════════════════
# 2. HMAC authentication
# ═══════════════════════════════════════════
class HMACAuthenticator:
    """Sign and verify messages with HMAC-SHA256."""

    def __init__(self, secret_key: bytes):
        if len(secret_key) < 32:
            raise ValueError("Secret key must be at least 32 bytes")
        self._key = secret_key

    def sign(self, message: bytes) -> bytes:
        return hmac.new(self._key, message, hashlib.sha256).digest()

    def sign_b64(self, message: bytes) -> str:
        return base64.urlsafe_b64encode(self.sign(message)).decode()

    def verify(self, message: bytes, signature: bytes) -> bool:
        expected = self.sign(message)
        return hmac.compare_digest(expected, signature)

    def create_token(self, payload: dict) -> str:
        """Simple signed token: base64(payload).signature"""
        import json
        payload_bytes = base64.urlsafe_b64encode(
            json.dumps(payload).encode()
        )
        sig = self.sign_b64(payload_bytes).encode()
        return f"{payload_bytes.decode()}.{sig.decode()}"

    def verify_token(self, token: str) -> dict | None:
        """Verify and decode a token. Returns None on failure."""
        import json
        try:
            payload_b64, sig = token.rsplit(".", 1)
            payload_bytes = payload_b64.encode()
            expected_sig = self.sign_b64(payload_bytes)
            if not hmac.compare_digest(expected_sig, sig):
                return None
            return json.loads(base64.urlsafe_b64decode(payload_bytes))
        except Exception:
            return None

# ═══════════════════════════════════════════
# 3. Simple OTP (TOTP-like, HMAC-based)
# ═══════════════════════════════════════════
class TOTPLike:
    """
    Very simplified TOTP-like implementation.
    Real TOTP: use pyotp library (RFC 6238).
    """

    def __init__(self, secret: bytes, step_seconds: int = 30, digits: int = 6):
        self.secret = secret
        self.step_seconds = step_seconds
        self.digits = digits

    def _time_step(self, offset: int = 0) -> int:
        return int(time.time() / self.step_seconds) + offset

    def generate(self, offset: int = 0) -> str:
        t = struct.pack(">Q", self._time_step(offset))
        h = hmac.new(self.secret, t, hashlib.sha1).digest()
        offset_byte = h[-1] & 0x0F
        code = struct.unpack(">I", h[offset_byte:offset_byte+4])[0] & 0x7FFFFFFF
        return str(code % (10 ** self.digits)).zfill(self.digits)

    def verify(self, token: str, window: int = 1) -> bool:
        """Accept codes from previous/current/next window."""
        for offset in range(-window, window + 1):
            if hmac.compare_digest(self.generate(offset), token):
                return True
        return False

# ═══════════════════════════════════════════
# 4. XOR cipher (educational — NOT secure)
# ═══════════════════════════════════════════
def xor_cipher(data: bytes, key: bytes) -> bytes:
    """XOR cipher — educational only. NOT cryptographically secure."""
    key_cycle = (key[i % len(key)] for i in range(len(data)))
    return bytes(a ^ b for a, b in zip(data, key_cycle))

# ═══════════════════════════════════════════
# 5. Secure random
# ═══════════════════════════════════════════
def random_bytes(n: int) -> bytes:
    return os.urandom(n)

def random_token(n_bytes: int = 32) -> str:
    return base64.urlsafe_b64encode(os.urandom(n_bytes)).rstrip(b"=").decode()

def random_hex(n_bytes: int = 16) -> str:
    return os.urandom(n_bytes).hex()

def random_pin(digits: int = 6) -> str:
    """Cryptographically random numeric PIN."""
    n = int.from_bytes(os.urandom(4), "big") % (10 ** digits)
    return str(n).zfill(digits)

# ═══════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════
if __name__ == "__main__":
    print("=== Hashing ===")
    for algo in ["md5", "sha1", "sha256", "sha3_256", "blake2b"]:
        h = hash_password("MySecret123!", algo)
        print(f"  {algo:12s}: {h[:32]}...")

    print("\n=== Salted Hash (PBKDF2) ===")
    hashed, salt = salted_hash("correct-horse-battery-staple")
    print(f"  Hash: {hashed[:30]}...")
    print(f"  Salt: {salt[:20]}...")
    print(f"  Verify correct:   {verify_salted_hash('correct-horse-battery-staple', hashed, salt)}")
    print(f"  Verify incorrect: {verify_salted_hash('wrong-password', hashed, salt)}")

    print("\n=== HMAC Authenticator ===")
    key = os.urandom(32)
    auth = HMACAuthenticator(key)
    msg = b"Transfer $100 to Alice"
    sig = auth.sign(msg)
    print(f"  Signature: {sig.hex()[:32]}...")
    print(f"  Verify (ok):       {auth.verify(msg, sig)}")
    print(f"  Verify (tampered): {auth.verify(b'Transfer $999 to Alice', sig)}")

    token = auth.create_token({"user": "alice", "role": "admin", "exp": 9999999999})
    print(f"\n  Token: {token[:60]}...")
    payload = auth.verify_token(token)
    print(f"  Decoded: {payload}")
    print(f"  Tampered: {auth.verify_token(token[:-4] + 'XXXX')}")

    print("\n=== TOTP-like OTP ===")
    otp = TOTPLike(secret=os.urandom(20))
    code = otp.generate()
    print(f"  Current code: {code}")
    print(f"  Verify (correct): {otp.verify(code)}")
    print(f"  Verify (wrong):   {otp.verify('000000')}")

    print("\n=== Secure Random ===")
    print(f"  Token:   {random_token()}")
    print(f"  Hex:     {random_hex()}")
    print(f"  PIN:     {random_pin(6)}")
    print(f"  4 bytes: {random_bytes(4).hex()}")
