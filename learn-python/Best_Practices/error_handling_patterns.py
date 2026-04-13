"""
Best practices: Error handling patterns.
"""
import logging

logger = logging.getLogger(__name__)

# === 1. Be specific with exceptions ===
# Bad
def bad_error_handling(data):
    try:
        return data["key"]["nested"]
    except Exception:
        return None

# Good
def good_error_handling(data):
    try:
        return data["key"]["nested"]
    except (KeyError, TypeError) as e:
        logger.warning(f"Data access failed: {e}")
        return None

# === 2. Custom exception hierarchy ===
class AppError(Exception):
    """Base application error."""
    pass

class NotFoundError(AppError):
    def __init__(self, resource, id):
        self.resource = resource
        self.id = id
        super().__init__(f"{resource} {id} not found")

class ValidationError(AppError):
    def __init__(self, errors):
        self.errors = errors
        super().__init__(f"Validation failed: {errors}")

class AuthError(AppError):
    pass

# === 3. Context-specific error wrapping ===
def get_user(user_id):
    try:
        # Simulate database lookup
        users = {1: "Alice", 2: "Bob"}
        return users[user_id]
    except KeyError:
        raise NotFoundError("User", user_id) from None

# === 4. Error recovery patterns ===
def with_retry(func, max_retries=3, exceptions=(Exception,)):
    """Retry a function on failure."""
    for attempt in range(1, max_retries + 1):
        try:
            return func()
        except exceptions as e:
            if attempt == max_retries:
                raise
            logger.warning(f"Attempt {attempt} failed: {e}")
    return None

# === 5. Result pattern (no exceptions for expected failures) ===
from dataclasses import dataclass
from typing import TypeVar, Generic, Optional

T = TypeVar('T')

@dataclass
class Result(Generic[T]):
    value: Optional[T] = None
    error: Optional[str] = None

    @property
    def is_ok(self):
        return self.error is None

    @classmethod
    def ok(cls, value):
        return cls(value=value)

    @classmethod
    def fail(cls, error):
        return cls(error=error)

def parse_int(s: str) -> Result[int]:
    try:
        return Result.ok(int(s))
    except ValueError:
        return Result.fail(f"Cannot parse '{s}' as integer")

# === 6. Cleanup with finally ===
def process_file(filepath):
    resource = None
    try:
        resource = open(filepath)
        return resource.read()
    except FileNotFoundError:
        return None
    finally:
        if resource:
            resource.close()

# === Demo ===
if __name__ == "__main__":
    # Custom exceptions
    try:
        get_user(99)
    except NotFoundError as e:
        print(f"Error: {e}")
        print(f"Resource: {e.resource}, ID: {e.id}")

    # Result pattern
    for value in ["42", "abc", "0"]:
        result = parse_int(value)
        if result.is_ok:
            print(f"Parsed '{value}' -> {result.value}")
        else:
            print(f"Failed: {result.error}")

    # Validation errors
    try:
        errors = {"email": "invalid format", "age": "must be positive"}
        raise ValidationError(errors)
    except ValidationError as e:
        print(f"\nValidation: {e.errors}")
