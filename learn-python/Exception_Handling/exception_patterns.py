"""
Exception Handling: Custom exceptions, exception hierarchies, chaining, and patterns.
"""
from __future__ import annotations
import logging
import traceback
from dataclasses import dataclass
from typing import Any

# ═══════════════════════════════════════════
# 1. Custom exception hierarchy
# ═══════════════════════════════════════════
class AppError(Exception):
    """Base exception for all application errors."""
    code: int = 500
    message: str = "An internal error occurred"

    def __init__(self, message: str | None = None, **context):
        self.message = message or self.__class__.message
        self.context = context
        super().__init__(self.message)

    def __str__(self):
        ctx = f" | {self.context}" if self.context else ""
        return f"[{self.__class__.__name__}:{self.code}] {self.message}{ctx}"

class ValidationError(AppError):
    code = 400; message = "Validation failed"

class AuthenticationError(AppError):
    code = 401; message = "Authentication required"

class AuthorizationError(AppError):
    code = 403; message = "Access denied"

class NotFoundError(AppError):
    code = 404; message = "Resource not found"

class ConflictError(AppError):
    code = 409; message = "Resource conflict"

class RateLimitError(AppError):
    code = 429; message = "Too many requests"

class ServiceUnavailableError(AppError):
    code = 503; message = "Service unavailable"

# Sub-hierarchies
class DatabaseError(AppError):
    code = 503; message = "Database error"

class ConnectionError(DatabaseError):
    message = "Cannot connect to database"

class QueryError(DatabaseError):
    message = "Query execution failed"

class FieldValidationError(ValidationError):
    def __init__(self, field: str, value: Any, reason: str):
        super().__init__(f"Field '{field}': {reason}", field=field, value=value)
        self.field = field; self.value = value; self.reason = reason

# ═══════════════════════════════════════════
# 2. Exception chaining
# ═══════════════════════════════════════════
def fetch_from_db(query: str):
    try:
        if not query.strip():
            raise ValueError("Empty query")
        if "DROP" in query.upper():
            raise PermissionError("DDL not allowed")
        raise RuntimeError("Connection timed out")  # simulate
    except RuntimeError as e:
        raise QueryError(str(e), query=query) from e   # explicit chaining
    except PermissionError as e:
        raise AuthorizationError(str(e), query=query) from e

def fetch_wrapper(query: str):
    try:
        return fetch_from_db(query)
    except DatabaseError as e:
        raise ServiceUnavailableError(f"DB layer failed: {e}", upstream=str(e)) from e

# ═══════════════════════════════════════════
# 3. try/except/else/finally
# ═══════════════════════════════════════════
def parse_int(s: str) -> int | None:
    try:
        result = int(s)
    except ValueError:
        return None           # swallow and return None
    else:
        return result         # runs only if no exception
    finally:
        pass                  # always runs (cleanup here)

def divide_safe(a: float, b: float) -> float:
    try:
        return a / b
    except ZeroDivisionError as e:
        raise ValidationError("Division by zero", numerator=a) from e

# ═══════════════════════════════════════════
# 4. ExceptionGroup (Python 3.11+)
# ═══════════════════════════════════════════
def validate_all(data: dict) -> None:
    """Collect all validation errors, raise as ExceptionGroup."""
    errors = []
    if not data.get("name"):
        errors.append(FieldValidationError("name", data.get("name"), "required"))
    if not isinstance(data.get("age"), int) or data.get("age", -1) < 0:
        errors.append(FieldValidationError("age", data.get("age"), "must be non-negative int"))
    email = data.get("email", "")
    if "@" not in str(email):
        errors.append(FieldValidationError("email", email, "invalid format"))
    if errors:
        raise ExceptionGroup("Validation failed", errors)

def demo_exception_group():
    print("\n=== ExceptionGroup (Python 3.11+) ===")
    cases = [
        {"name": "Alice", "age": 30, "email": "alice@example.com"},
        {"name": "",      "age": -1,  "email": "bad-email"},
        {"name": "Bob",   "age": 25,  "email": "bob"},
    ]
    for data in cases:
        try:
            validate_all(data)
            print(f"  {data.get('name', '?')}: valid")
        except* FieldValidationError as eg:
            errors = [f"{e.field}: {e.reason}" for e in eg.exceptions]
            print(f"  {data.get('name', '?')}: errors = {errors}")

# ═══════════════════════════════════════════
# 5. Context managers for error handling
# ═══════════════════════════════════════════
import contextlib

@contextlib.contextmanager
def suppress_and_log(*exceptions, logger: logging.Logger | None = None):
    """Suppress specific exceptions and log them."""
    try:
        yield
    except exceptions as e:
        msg = f"Suppressed {type(e).__name__}: {e}"
        if logger:
            logger.warning(msg)
        else:
            print(f"  [SUPPRESSED] {msg}")

@contextlib.contextmanager
def convert_errors(error_map: dict[type, type]):
    """Convert one exception type to another."""
    try:
        yield
    except tuple(error_map.keys()) as e:
        target_type = error_map.get(type(e), AppError)
        raise target_map(str(e)) from e if (error_map := {type(e): target_type}) else e

# ═══════════════════════════════════════════
# 6. Retry with exponential backoff
# ═══════════════════════════════════════════
import time
import random as _rand

def retry_with_backoff(
    fn,
    *args,
    max_attempts: int = 3,
    base_delay: float = 0.1,
    max_delay: float = 2.0,
    backoff_factor: float = 2.0,
    retryable: tuple[type, ...] = (Exception,),
    **kwargs
):
    delay = base_delay
    last_exc = None
    for attempt in range(1, max_attempts + 1):
        try:
            return fn(*args, **kwargs)
        except retryable as e:
            last_exc = e
            if attempt == max_attempts:
                raise
            jitter = _rand.uniform(0, delay * 0.1)
            wait = min(delay + jitter, max_delay)
            print(f"  Attempt {attempt} failed ({e}), retrying in {wait:.2f}s")
            time.sleep(wait)
            delay = min(delay * backoff_factor, max_delay)
    raise last_exc

# ═══════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════
if __name__ == "__main__":
    print("=== Custom exception hierarchy ===")
    exceptions = [
        ValidationError("Email is invalid", email="bad"),
        FieldValidationError("age", -1, "must be positive"),
        NotFoundError("User not found", user_id=42),
        AuthorizationError(role="viewer"),
    ]
    for e in exceptions:
        print(f"  {e}")

    print("\n=== Exception chaining ===")
    for query in ["SELECT * FROM users", ""]:
        try:
            if not query:
                raise ValidationError("Empty query")
            fetch_wrapper(query)
        except AppError as e:
            print(f"  {e}")
            if e.__cause__:
                print(f"    caused by: {type(e.__cause__).__name__}: {e.__cause__}")

    print("\n=== try/else/finally ===")
    for s in ["42", "abc", "3.14"]:
        result = parse_int(s)
        print(f"  parse_int({s!r}) = {result!r}")

    print("\n=== divide_safe ===")
    for a, b in [(10, 3), (5, 0)]:
        try:
            print(f"  {a}/{b} = {divide_safe(a, b):.3f}")
        except ValidationError as e:
            print(f"  Error: {e}")

    demo_exception_group()

    print("\n=== suppress_and_log ===")
    with suppress_and_log(ValueError, ZeroDivisionError):
        x = 1 / 0
    print("  (continued after suppressed ZeroDivisionError)")
    with suppress_and_log(ValueError):
        int("not-a-number")
    print("  (continued after suppressed ValueError)")

    print("\n=== retry_with_backoff ===")
    calls = [0]
    def flaky_service():
        calls[0] += 1
        if calls[0] < 3:
            raise ConnectionError(f"Attempt {calls[0]} failed")
        return "OK"
    result = retry_with_backoff(flaky_service, max_attempts=3, base_delay=0.01)
    print(f"  Result after {calls[0]} attempts: {result!r}")
