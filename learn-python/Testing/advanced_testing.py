"""
Testing: pytest advanced patterns — parametrize, fixtures, mocking, property-based.
"""
# This file is a reference guide + self-contained runner.
# Run with: pytest testing_advanced.py -v
# Or:       python testing_advanced.py  (uses the built-in mini-runner)

import sys
import math
import random
import time
from typing import Callable, Any

# ═══════════════════════════════════════════
# Code under test
# ═══════════════════════════════════════════
def is_prime(n: int) -> bool:
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    return all(n % d != 0 for d in range(3, int(n**0.5)+1, 2))

def roman_to_int(s: str) -> int:
    values = {"I":1,"V":5,"X":10,"L":50,"C":100,"D":500,"M":1000}
    result, prev = 0, 0
    for ch in reversed(s):
        v = values[ch]
        result += v if v >= prev else -v
        prev = v
    return result

def int_to_roman(n: int) -> str:
    vals = [(1000,"M"),(900,"CM"),(500,"D"),(400,"CD"),(100,"C"),
            (90,"XC"),(50,"L"),(40,"XL"),(10,"X"),(9,"IX"),
            (5,"V"),(4,"IV"),(1,"I")]
    result = ""
    for value, symbol in vals:
        while n >= value:
            result += symbol; n -= value
    return result

def fizzbuzz(n: int) -> list[str]:
    return [
        "FizzBuzz" if i%15==0 else "Fizz" if i%3==0 else "Buzz" if i%5==0 else str(i)
        for i in range(1, n+1)
    ]

class Stack:
    def __init__(self): self._data: list = []
    def push(self, v): self._data.append(v)
    def pop(self): return self._data.pop()
    def peek(self): return self._data[-1]
    def is_empty(self): return not self._data
    def __len__(self): return len(self._data)

# ═══════════════════════════════════════════
# Mini test runner
# ═══════════════════════════════════════════
_tests: list[tuple[str, Callable]] = []
_passed = 0; _failed = 0

def test(fn: Callable | None = None):
    if fn is None: return lambda f: test(f)
    _tests.append((fn.__name__, fn)); return fn

def assert_equal(a, b, msg=""):
    if a != b: raise AssertionError(f"{a!r} != {b!r}" + (f" — {msg}" if msg else ""))

def assert_raises(exc, fn, *args, **kwargs):
    try: fn(*args, **kwargs)
    except exc: return
    raise AssertionError(f"Expected {exc.__name__} but nothing was raised")

def run_tests():
    global _passed, _failed
    for name, fn in _tests:
        try:
            fn()
            _passed += 1; print(f"  ✓ {name}")
        except AssertionError as e:
            _failed += 1; print(f"  ✗ {name}: {e}")
        except Exception as e:
            _failed += 1; print(f"  ✗ {name}: {type(e).__name__}: {e}")
    print(f"\n  {_passed}/{len(_tests)} passed, {_failed} failed")

# ═══════════════════════════════════════════
# Tests — is_prime
# ═══════════════════════════════════════════
PRIME_CASES = [(2,True),(3,True),(4,False),(5,True),(9,False),(11,True),(97,True),(100,False)]

@test
def test_is_prime_known():
    for n, expected in PRIME_CASES:
        assert is_prime(n) == expected, f"is_prime({n})"

@test
def test_primes_below_20():
    expected = [2,3,5,7,11,13,17,19]
    actual = [n for n in range(20) if is_prime(n)]
    assert_equal(actual, expected)

@test
def test_is_prime_large():
    assert is_prime(104729)   # known prime
    assert not is_prime(104728)

# ═══════════════════════════════════════════
# Tests — Roman numerals
# ═══════════════════════════════════════════
ROMAN_CASES = [(1,"I"),(4,"IV"),(9,"IX"),(14,"XIV"),(40,"XL"),
               (90,"XC"),(400,"CD"),(900,"CM"),(1994,"MCMXCIV"),(2024,"MMXXIV")]

@test
def test_int_to_roman():
    for n, expected in ROMAN_CASES:
        assert_equal(int_to_roman(n), expected, f"int_to_roman({n})")

@test
def test_roman_to_int():
    for n, roman in ROMAN_CASES:
        assert_equal(roman_to_int(roman), n, f"roman_to_int({roman!r})")

@test
def test_roman_roundtrip():
    for n in range(1, 4000):
        assert_equal(roman_to_int(int_to_roman(n)), n, f"roundtrip({n})")

# ═══════════════════════════════════════════
# Tests — FizzBuzz
# ═══════════════════════════════════════════
@test
def test_fizzbuzz_first_15():
    result = fizzbuzz(15)
    assert_equal(result[0],  "1")
    assert_equal(result[2],  "Fizz")
    assert_equal(result[4],  "Buzz")
    assert_equal(result[14], "FizzBuzz")

@test
def test_fizzbuzz_count():
    result = fizzbuzz(100)
    fizz_count = sum(1 for r in result if r == "Fizz")
    buzz_count = sum(1 for r in result if r == "Buzz")
    fb_count   = sum(1 for r in result if r == "FizzBuzz")
    assert_equal(fizz_count, 27)
    assert_equal(buzz_count, 14)
    assert_equal(fb_count,   6)

# ═══════════════════════════════════════════
# Tests — Stack
# ═══════════════════════════════════════════
@test
def test_stack_push_pop():
    s = Stack()
    s.push(1); s.push(2); s.push(3)
    assert_equal(len(s), 3)
    assert_equal(s.pop(), 3)
    assert_equal(len(s), 2)

@test
def test_stack_peek_doesnt_remove():
    s = Stack()
    s.push(42)
    assert_equal(s.peek(), 42)
    assert_equal(len(s), 1)

@test
def test_stack_empty_pop_raises():
    s = Stack()
    assert_raises(IndexError, s.pop)

@test
def test_stack_lifo_ordering():
    s = Stack()
    items = list(range(10))
    for i in items: s.push(i)
    reversed_items = [s.pop() for _ in range(10)]
    assert_equal(reversed_items, list(reversed(items)))

# ═══════════════════════════════════════════
# Property-based style tests (simple)
# ═══════════════════════════════════════════
@test
def test_roman_property_format():
    """All ints 1-3999 produce valid Roman numeral strings."""
    valid_chars = set("IVXLCDM")
    for n in range(1, 4000):
        r = int_to_roman(n)
        assert r, f"Empty roman for {n}"
        assert all(c in valid_chars for c in r), f"Invalid chars in {r!r}"

@test
def test_fizzbuzz_property_divisibility():
    """Check FizzBuzz divisibility invariants for 1..300."""
    result = fizzbuzz(300)
    for i, r in enumerate(result, 1):
        is_fizz = (i % 3 == 0)
        is_buzz = (i % 5 == 0)
        if is_fizz and is_buzz: assert r == "FizzBuzz", f"i={i}"
        elif is_fizz:            assert r == "Fizz",     f"i={i}"
        elif is_buzz:            assert r == "Buzz",     f"i={i}"
        else:                    assert r == str(i),     f"i={i}"

# ═══════════════════════════════════════════
# Pytest reference (syntax only)
# ═══════════════════════════════════════════
PYTEST_REFERENCE = '''
# pytest advanced patterns (reference only)

import pytest

# ── Parametrize ──────────────────────────
@pytest.mark.parametrize("n,expected", [
    (2, True), (4, False), (97, True),
])
def test_is_prime_param(n, expected):
    assert is_prime(n) == expected

# ── Fixtures ─────────────────────────────
@pytest.fixture
def empty_stack():
    return Stack()

@pytest.fixture
def populated_stack(empty_stack):
    for i in range(5):
        empty_stack.push(i)
    return empty_stack       # fixture composition

# ── tmp_path (built-in fixture) ──────────
def test_file_creation(tmp_path):
    f = tmp_path / "data.txt"
    f.write_text("hello")
    assert f.read_text() == "hello"

# ── monkeypatch ──────────────────────────
def test_env_var(monkeypatch):
    monkeypatch.setenv("MY_KEY", "secret")
    import os
    assert os.environ["MY_KEY"] == "secret"

# ── Mock ─────────────────────────────────
from unittest.mock import patch, MagicMock

def test_requests_mock():
    with patch("requests.get") as mock_get:
        mock_get.return_value = MagicMock(status_code=200, json=lambda: {"key":"val"})
        # call code that uses requests.get...
        response = mock_get("https://api.example.com")
        assert response.status_code == 200

# ── Hypothesis (property-based) ─────────
# pip install hypothesis
from hypothesis import given, strategies as st

@given(st.integers(1, 3999))
def test_roman_hypothesis(n):
    assert roman_to_int(int_to_roman(n)) == n
'''

if __name__ == "__main__":
    print("=== Running tests ===\n")
    run_tests()
    print("\n=== Pytest Reference ===")
    print(PYTEST_REFERENCE[:400], "...\n")
