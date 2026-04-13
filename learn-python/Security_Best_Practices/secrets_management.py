"""
Security Best Practices: Secrets management and environment variable security.
"""
import os
import re
import hashlib
import hmac
import base64
import secrets
from pathlib import Path
from typing import Any

# ═══════════════════════════════════════════
# 1. Safe environment variable loading
# ═══════════════════════════════════════════
class EnvConfig:
    """
    Type-safe, validated config from environment variables.
    Never hardcode secrets in source code.
    """

    def __init__(self, env: dict[str, str] | None = None):
        self._env = env or os.environ

    def get(self, key: str, default: str | None = None) -> str | None:
        return self._env.get(key, default)

    def require(self, key: str) -> str:
        value = self._env.get(key)
        if not value:
            raise EnvironmentError(f"Required environment variable '{key}' is not set")
        return value

    def get_int(self, key: str, default: int | None = None) -> int | None:
        value = self._env.get(key)
        if value is None:
            return default
        try:
            return int(value)
        except ValueError:
            raise ValueError(f"Environment variable '{key}' must be an integer, got: {value!r}")

    def get_bool(self, key: str, default: bool = False) -> bool:
        value = self._env.get(key, "").lower()
        if not value:
            return default
        if value in ("1", "true", "yes", "on"):
            return True
        if value in ("0", "false", "no", "off"):
            return False
        raise ValueError(f"'{key}' must be a boolean value, got: {value!r}")

    def get_list(self, key: str, separator: str = ",") -> list[str]:
        value = self._env.get(key, "")
        if not value:
            return []
        return [item.strip() for item in value.split(separator) if item.strip()]

    def get_url(self, key: str, default: str | None = None) -> str | None:
        value = self._env.get(key, default)
        if value and not re.match(r'^(https?|postgresql|redis|mongodb)://', value):
            raise ValueError(f"'{key}' must be a valid URL, got: {value!r}")
        return value

    def snapshot(self) -> dict[str, str]:
        """Return a copy of relevant config (NEVER log secrets)."""
        safe_keys = {"APP_NAME", "APP_ENV", "LOG_LEVEL", "HOST", "PORT", "DEBUG"}
        return {k: v for k, v in self._env.items() if k in safe_keys}

# ═══════════════════════════════════════════
# 2. .env file parser (without python-dotenv)
# ═══════════════════════════════════════════
def load_dotenv(path: str | Path = ".env") -> dict[str, str]:
    """Parse a .env file into a dict. Does NOT modify os.environ."""
    result: dict[str, str] = {}
    path = Path(path)
    if not path.exists():
        return result

    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        # Remove inline comments
        line = re.sub(r"\s+#.*$", "", line)
        if "=" in line:
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            result[key] = value

    return result

# ═══════════════════════════════════════════
# 3. Secret detection (scan for leaked secrets)
# ═══════════════════════════════════════════
SECRET_PATTERNS = [
    (r'(?i)(api[_\-]?key|apikey)\s*[:=]\s*["\']?([A-Za-z0-9_\-]{20,})["\']?', "API Key"),
    (r'(?i)(secret[_\-]?key|secret)\s*[:=]\s*["\']?([A-Za-z0-9_\-]{20,})["\']?', "Secret Key"),
    (r'(?i)(password|passwd|pwd)\s*[:=]\s*["\']?([^\s"\']{8,})["\']?', "Password"),
    (r'(?i)Bearer\s+([A-Za-z0-9_\-\.]{20,})', "Bearer Token"),
    (r'(?i)(aws[_\-]?access[_\-]?key[_\-]?id)\s*[:=]\s*([A-Z0-9]{20})', "AWS Key ID"),
    (r'sk-[A-Za-z0-9]{48}', "OpenAI API Key"),
    (r'ghp_[A-Za-z0-9]{36}', "GitHub Token"),
    (r'-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----', "Private Key"),
]

def scan_for_secrets(text: str) -> list[dict[str, str]]:
    """Scan text for potentially leaked secrets."""
    findings = []
    for pattern, secret_type in SECRET_PATTERNS:
        matches = re.finditer(pattern, text)
        for m in matches:
            findings.append({
                "type": secret_type,
                "match": m.group(0)[:40] + ("..." if len(m.group(0)) > 40 else ""),
                "position": str(m.start()),
            })
    return findings

def scan_file(path: str | Path) -> list[dict[str, str]]:
    try:
        content = Path(path).read_text(errors="ignore")
        return scan_for_secrets(content)
    except OSError:
        return []

# ═══════════════════════════════════════════
# 4. Secure token generation
# ═══════════════════════════════════════════
def generate_secret_key(length: int = 50) -> str:
    """Generate a cryptographically secure secret key."""
    return secrets.token_urlsafe(length)

def generate_api_key(prefix: str = "sk") -> str:
    return f"{prefix}_{secrets.token_hex(24)}"

def generate_otp(digits: int = 6) -> str:
    return str(secrets.randbelow(10**digits)).zfill(digits)

# ═══════════════════════════════════════════
# 5. Constant-time comparison (prevent timing attacks)
# ═══════════════════════════════════════════
def safe_compare(a: str, b: str) -> bool:
    """Constant-time string comparison (prevents timing attacks)."""
    return hmac.compare_digest(
        a.encode("utf-8"),
        b.encode("utf-8"),
    )

# ═══════════════════════════════════════════
# 6. Secrets redaction for logging
# ═══════════════════════════════════════════
SENSITIVE_KEYS = frozenset({
    "password", "passwd", "secret", "token", "api_key", "apikey",
    "auth", "credential", "private_key", "secret_key", "access_key",
})

def redact(data: Any, replacement: str = "***REDACTED***") -> Any:
    """Recursively redact sensitive keys from dicts."""
    if isinstance(data, dict):
        return {
            k: replacement if k.lower() in SENSITIVE_KEYS else redact(v, replacement)
            for k, v in data.items()
        }
    if isinstance(data, list):
        return [redact(item, replacement) for item in data]
    return data

if __name__ == "__main__":
    print("=== EnvConfig ===")
    fake_env = {
        "APP_NAME": "MyAPI",
        "APP_ENV": "production",
        "PORT": "8000",
        "DEBUG": "false",
        "ALLOWED_HOSTS": "example.com, api.example.com",
        "DATABASE_URL": "postgresql://localhost/mydb",
        "LOG_LEVEL": "info",
    }
    config = EnvConfig(fake_env)
    print(f"APP_NAME: {config.get('APP_NAME')}")
    print(f"PORT:     {config.get_int('PORT')}")
    print(f"DEBUG:    {config.get_bool('DEBUG')}")
    print(f"HOSTS:    {config.get_list('ALLOWED_HOSTS')}")
    print(f"DB URL:   {config.get_url('DATABASE_URL')}")
    print(f"Safe snapshot: {config.snapshot()}")

    print("\n=== Secret Scanning ===")
    sample_code = """
    api_key = "sk-abcdef1234567890abcdef1234567890abcdef1234567890"
    password = "super_secret_password_here"
    auth_header = "Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1c2VyIn0.abc123xyz"
    """
    findings = scan_for_secrets(sample_code)
    for f in findings:
        print(f"  FOUND [{f['type']}]: {f['match']}")

    print("\n=== Secure Token Generation ===")
    print(f"Secret key: {generate_secret_key()}")
    print(f"API key:    {generate_api_key()}")
    print(f"OTP (6):    {generate_otp(6)}")

    print("\n=== Constant-time Compare ===")
    print(f"safe compare (equal):   {safe_compare('token123', 'token123')}")
    print(f"safe compare (unequal): {safe_compare('token123', 'token456')}")

    print("\n=== Redaction ===")
    payload = {
        "user": "alice",
        "password": "hunter2",
        "api_key": "sk-supersecret",
        "preferences": {"theme": "dark", "token": "auth_token_xyz"},
    }
    print(f"Original: {payload}")
    print(f"Redacted: {redact(payload)}")
