"""
Security Best Practices: Input validation and injection prevention.
"""
import re
import html
import urllib.parse
from typing import Any

# ═══════════════════════════════════════════
# 1. Input sanitization
# ═══════════════════════════════════════════
class InputValidator:
    """Validate and sanitize user input at system boundaries."""

    # Email
    _EMAIL_RE = re.compile(
        r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$'
    )

    # URL (basic, no unicode)
    _URL_RE = re.compile(
        r'^https?://[a-zA-Z0-9\-.]+(:[0-9]+)?(/[^\s]*)?$'
    )

    # Alphanumeric identifier
    _IDENT_RE = re.compile(r'^[a-zA-Z0-9_\-]{1,64}$')

    @staticmethod
    def email(value: str) -> str:
        if not isinstance(value, str):
            raise ValueError("Email must be a string")
        value = value.strip().lower()
        if len(value) > 254:
            raise ValueError("Email too long")
        if not InputValidator._EMAIL_RE.match(value):
            raise ValueError(f"Invalid email: {value!r}")
        return value

    @staticmethod
    def url(value: str, allowed_schemes=("https",)) -> str:
        if not isinstance(value, str):
            raise ValueError("URL must be a string")
        value = value.strip()
        if not InputValidator._URL_RE.match(value):
            raise ValueError(f"Invalid URL: {value!r}")
        scheme = urllib.parse.urlparse(value).scheme
        if scheme not in allowed_schemes:
            raise ValueError(f"URL scheme '{scheme}' not allowed")
        return value

    @staticmethod
    def identifier(value: str) -> str:
        if not isinstance(value, str):
            raise ValueError("Identifier must be a string")
        if not InputValidator._IDENT_RE.match(value):
            raise ValueError(f"Invalid identifier: {value!r}")
        return value

    @staticmethod
    def integer(value: Any, min_val: int | None = None, max_val: int | None = None) -> int:
        try:
            n = int(value)
        except (TypeError, ValueError):
            raise ValueError(f"Invalid integer: {value!r}")
        if min_val is not None and n < min_val:
            raise ValueError(f"{n} < minimum {min_val}")
        if max_val is not None and n > max_val:
            raise ValueError(f"{n} > maximum {max_val}")
        return n

    @staticmethod
    def enum(value: str, allowed: set[str]) -> str:
        if value not in allowed:
            raise ValueError(f"{value!r} not in {allowed}")
        return value

    @staticmethod
    def max_length(value: str, max_len: int) -> str:
        if len(value) > max_len:
            raise ValueError(f"Value too long: {len(value)} > {max_len}")
        return value

# ═══════════════════════════════════════════
# 2. XSS Prevention
# ═══════════════════════════════════════════
def escape_html(text: str) -> str:
    """HTML-escape user content before rendering."""
    return html.escape(str(text), quote=True)

def escape_url_param(value: str) -> str:
    """URL-encode a query string value."""
    return urllib.parse.quote(str(value), safe="")

def safe_html_attributes(attr_dict: dict[str, str]) -> str:
    """Build HTML attributes safely."""
    parts = []
    for k, v in attr_dict.items():
        # Whitelist attribute names
        if not re.match(r'^[a-zA-Z][a-zA-Z0-9\-]{0,30}$', k):
            continue  # skip dangerous attribute names
        # Prevent javascript: in href/src/action
        if k.lower() in ("href", "src", "action"):
            if re.match(r'^\s*javascript:', v, re.IGNORECASE):
                v = "#"
        parts.append(f'{k}="{escape_html(v)}"')
    return " ".join(parts)

# ═══════════════════════════════════════════
# 3. SQL injection prevention patterns
# ═══════════════════════════════════════════
import sqlite3

class SafeQueryBuilder:
    """Demonstrates parameterized query patterns."""

    def __init__(self):
        self.conn = sqlite3.connect(":memory:")
        self.conn.execute("""
            CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT, role TEXT)
        """)
        for row in [("Alice", "alice@test.com", "admin"),
                    ("Bob", "bob@test.com", "user"),
                    ("Charlie", "charlie@test.com", "user")]:
            self.conn.execute("INSERT INTO users (name,email,role) VALUES (?,?,?)", row)
        self.conn.commit()

    def get_user_safe(self, user_id: int) -> list:
        """SAFE: parameterized query."""
        user_id = InputValidator.integer(user_id, min_val=1)
        return self.conn.execute(
            "SELECT id, name, email FROM users WHERE id = ?", (user_id,)
        ).fetchall()

    def search_users_safe(self, name_like: str, role: str = "user") -> list:
        """SAFE: parameterized with LIKE."""
        name_like = InputValidator.max_length(name_like.strip(), 50)
        role = InputValidator.enum(role, {"admin", "user", "moderator"})
        # Use ? for values, whitelist for column names
        return self.conn.execute(
            "SELECT id, name FROM users WHERE name LIKE ? AND role = ?",
            (f"%{name_like}%", role)
        ).fetchall()

    def get_user_UNSAFE_example(self, user_id: str) -> str:
        """UNSAFE example — NEVER DO THIS."""
        return f"SELECT * FROM users WHERE id = {user_id}"  # SQL injection possible!

# ═══════════════════════════════════════════
# 4. Path traversal prevention
# ═══════════════════════════════════════════
from pathlib import Path

def safe_file_path(base_dir: str | Path, user_input: str) -> Path:
    """Prevent path traversal attacks."""
    base = Path(base_dir).resolve()
    requested = (base / user_input).resolve()
    if not str(requested).startswith(str(base)):
        raise PermissionError(f"Access denied: path traversal detected")
    return requested

# ═══════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════
if __name__ == "__main__":
    v = InputValidator()

    print("=== Email Validation ===")
    test_emails = ["alice@example.com", "ALICE@EXAMPLE.COM",
                   "not-an-email", "a@b.c", "@missing.com"]
    for e in test_emails:
        try:
            print(f"  {e!r:30s} → {v.email(e)!r}")
        except ValueError as err:
            print(f"  {e!r:30s} → ERROR: {err}")

    print("\n=== Integer Validation ===")
    for val in ["42", "  10 ", "abc", 3.14, "-5", "9999"]:
        try:
            print(f"  {val!r:10s} → {v.integer(val, 0, 100)}")
        except ValueError as err:
            print(f"  {val!r:10s} → ERROR: {err}")

    print("\n=== XSS Prevention ===")
    payloads = [
        '<script>alert("xss")</script>',
        '"><img src=x onerror=alert(1)>',
        'Normal text with <b>bold</b>',
        "It's a <test>",
    ]
    for p in payloads:
        print(f"  Input:   {p}")
        print(f"  Escaped: {escape_html(p)}\n")

    print("=== HTML Attributes ===")
    attrs = {"href": "javascript:alert(1)", "class": "btn", "onclick": "steal()"}
    print(f"  Safe attrs: {safe_html_attributes(attrs)}")

    print("\n=== SQL Injection Prevention ===")
    db = SafeQueryBuilder()
    print(f"  User 1: {db.get_user_safe(1)}")
    print(f"  Search 'alice': {db.search_users_safe('alice', role='admin')}")

    # Show what SQL injection looks like (string format — don't do this)
    malicious = "1 OR 1=1; DROP TABLE users;--"
    unsafe_query = db.get_user_UNSAFE_example(malicious)
    print(f"\n  UNSAFE query built: {unsafe_query!r}")
    print("  ↑ This would be catastrophic in a real DB!")

    print("\n=== Path Traversal Prevention ===")
    base = "/var/www/uploads"
    for user_path in ["image.png", "../../../etc/passwd", "subdir/file.txt"]:
        try:
            result = safe_file_path(base, user_path)
            print(f"  {user_path!r:30s} → {result}")
        except PermissionError as err:
            print(f"  {user_path!r:30s} → BLOCKED: {err}")
