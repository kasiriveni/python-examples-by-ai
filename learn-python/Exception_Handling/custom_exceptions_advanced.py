"""
Custom exceptions in Python.
"""

# Basic custom exception
class AppError(Exception):
    """Base exception for the application."""
    pass

class ValidationError(AppError):
    """Raised when validation fails."""
    def __init__(self, field, message):
        self.field = field
        self.message = message
        super().__init__(f"Validation error on '{field}': {message}")

class NotFoundError(AppError):
    """Raised when a resource is not found."""
    def __init__(self, resource_type, resource_id):
        self.resource_type = resource_type
        self.resource_id = resource_id
        super().__init__(f"{resource_type} with id '{resource_id}' not found")

class AuthenticationError(AppError):
    """Raised when authentication fails."""
    pass

class RateLimitError(AppError):
    """Raised when rate limit is exceeded."""
    def __init__(self, retry_after):
        self.retry_after = retry_after
        super().__init__(f"Rate limit exceeded. Retry after {retry_after}s")

# Using custom exceptions
def validate_user(name, age):
    if not name or not name.strip():
        raise ValidationError("name", "Name cannot be empty")
    if not isinstance(age, int) or age < 0 or age > 150:
        raise ValidationError("age", f"Invalid age: {age}")
    return True

def find_user(user_id):
    users = {1: "Alice", 2: "Bob"}
    if user_id not in users:
        raise NotFoundError("User", user_id)
    return users[user_id]

# Exception hierarchy handling
if __name__ == "__main__":
    # Test validation
    try:
        validate_user("", 25)
    except ValidationError as e:
        print(f"Caught: {e}")
        print(f"Field: {e.field}")

    # Test not found
    try:
        find_user(99)
    except NotFoundError as e:
        print(f"Caught: {e}")
        print(f"Resource: {e.resource_type} #{e.resource_id}")

    # Catch base class
    try:
        raise RateLimitError(retry_after=30)
    except AppError as e:
        print(f"App error: {e}")
        if isinstance(e, RateLimitError):
            print(f"Wait {e.retry_after}s")
