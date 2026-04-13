"""
pytest examples - modern Python testing.
"""

# Functions to test
def add(a, b):
    return a + b

def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b

def is_palindrome(s):
    s = s.lower().replace(" ", "")
    return s == s[::-1]

def fibonacci(n):
    if n < 0:
        raise ValueError("n must be non-negative")
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

# Test classes (run with: pytest -v)
class TestAdd:
    def test_positive_numbers(self):
        assert add(2, 3) == 5

    def test_negative_numbers(self):
        assert add(-1, -2) == -3

    def test_mixed(self):
        assert add(-1, 1) == 0

    def test_floats(self):
        assert abs(add(0.1, 0.2) - 0.3) < 1e-10

class TestDivide:
    def test_basic(self):
        assert divide(10, 2) == 5.0

    def test_zero_division(self):
        import pytest
        with pytest.raises(ZeroDivisionError):
            divide(10, 0)

class TestPalindrome:
    def test_simple(self):
        assert is_palindrome("racecar") is True

    def test_not_palindrome(self):
        assert is_palindrome("hello") is False

    def test_with_spaces(self):
        assert is_palindrome("race car") is True

    def test_mixed_case(self):
        assert is_palindrome("Madam") is True

class TestFibonacci:
    def test_base_cases(self):
        assert fibonacci(0) == 0
        assert fibonacci(1) == 1

    def test_sequence(self):
        expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
        for i, val in enumerate(expected):
            assert fibonacci(i) == val

    def test_negative(self):
        import pytest
        with pytest.raises(ValueError):
            fibonacci(-1)

# Parametrized tests
import pytest

@pytest.mark.parametrize("a, b, expected", [
    (1, 1, 2),
    (0, 0, 0),
    (-1, 1, 0),
    (100, 200, 300),
])
def test_add_parametrized(a, b, expected):
    assert add(a, b) == expected

# Fixtures
@pytest.fixture
def sample_data():
    return [3, 1, 4, 1, 5, 9, 2, 6]

def test_sorted(sample_data):
    result = sorted(sample_data)
    assert result == [1, 1, 2, 3, 4, 5, 6, 9]

def test_max(sample_data):
    assert max(sample_data) == 9

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
