"""
Testing Your Apps: pytest patterns and test organization.
"""
import pytest
from dataclasses import dataclass

# === Code to test ===
class Calculator:
    def add(self, a, b):
        return a + b

    def divide(self, a, b):
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return a / b

    def factorial(self, n):
        if n < 0:
            raise ValueError("Negative numbers not allowed")
        if n <= 1:
            return 1
        return n * self.factorial(n - 1)

@dataclass
class User:
    name: str
    email: str
    age: int

    def is_adult(self):
        return self.age >= 18

    def display_name(self):
        return self.name.title()

class UserService:
    def __init__(self):
        self.users = {}

    def create_user(self, name, email, age):
        if email in self.users:
            raise ValueError(f"User {email} already exists")
        user = User(name, email, age)
        self.users[email] = user
        return user

    def get_user(self, email):
        return self.users.get(email)

    def delete_user(self, email):
        if email not in self.users:
            raise KeyError(f"User {email} not found")
        del self.users[email]

# === Tests ===

# Basic tests
class TestCalculator:
    def setup_method(self):
        self.calc = Calculator()

    def test_add(self):
        assert self.calc.add(2, 3) == 5

    def test_add_negative(self):
        assert self.calc.add(-1, 1) == 0

    def test_divide(self):
        assert self.calc.divide(10, 2) == 5.0

    def test_divide_by_zero(self):
        with pytest.raises(ZeroDivisionError):
            self.calc.divide(10, 0)

    def test_factorial(self):
        assert self.calc.factorial(5) == 120

    def test_factorial_zero(self):
        assert self.calc.factorial(0) == 1

    def test_factorial_negative(self):
        with pytest.raises(ValueError):
            self.calc.factorial(-1)

# Parametrized tests
class TestCalculatorParametrized:
    @pytest.mark.parametrize("a, b, expected", [
        (1, 1, 2),
        (0, 0, 0),
        (-1, -1, -2),
        (100, 200, 300),
    ])
    def test_add(self, a, b, expected):
        calc = Calculator()
        assert calc.add(a, b) == expected

    @pytest.mark.parametrize("n, expected", [
        (0, 1), (1, 1), (5, 120), (10, 3628800),
    ])
    def test_factorial(self, n, expected):
        calc = Calculator()
        assert calc.factorial(n) == expected

# Fixtures
@pytest.fixture
def user_service():
    service = UserService()
    service.create_user("Alice", "alice@test.com", 25)
    service.create_user("Bob", "bob@test.com", 17)
    return service

class TestUserService:
    def test_create_user(self, user_service):
        user = user_service.create_user("Charlie", "charlie@test.com", 30)
        assert user.name == "Charlie"
        assert user.email == "charlie@test.com"

    def test_create_duplicate(self, user_service):
        with pytest.raises(ValueError, match="already exists"):
            user_service.create_user("Alice2", "alice@test.com", 20)

    def test_get_user(self, user_service):
        user = user_service.get_user("alice@test.com")
        assert user is not None
        assert user.name == "Alice"

    def test_get_nonexistent(self, user_service):
        assert user_service.get_user("unknown@test.com") is None

    def test_delete_user(self, user_service):
        user_service.delete_user("alice@test.com")
        assert user_service.get_user("alice@test.com") is None

    def test_is_adult(self, user_service):
        alice = user_service.get_user("alice@test.com")
        bob = user_service.get_user("bob@test.com")
        assert alice.is_adult() is True
        assert bob.is_adult() is False

if __name__ == "__main__":
    # Run with: pytest Testing_Your_Apps/pytest_patterns.py -v
    print("Run with pytest to execute tests")
    print("  pytest Testing_Your_Apps/pytest_patterns.py -v")
    print("  pytest Testing_Your_Apps/pytest_patterns.py -v --tb=short")
