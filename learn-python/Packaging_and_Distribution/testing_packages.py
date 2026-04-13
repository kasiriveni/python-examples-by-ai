"""
Packaging and Distribution: pytest patterns, fixtures, and test organization.
"""
# NOTE: This file demonstrates pytest patterns without requiring pytest installed.
# Run with: python testing_packages.py (self-contained)
# Or: pytest testing_packages.py -v (requires pytest)

import sys
import traceback
from typing import Callable

# ═══════════════════════════════════════════
# 1. The code under test
# ═══════════════════════════════════════════
class InsufficientFundsError(Exception): pass

class BankAccount:
    def __init__(self, owner: str, balance: float = 0.0):
        if balance < 0:
            raise ValueError("Balance cannot be negative")
        self.owner = owner
        self._balance = balance
        self._transactions: list[tuple[str, float]] = []

    @property
    def balance(self) -> float:
        return self._balance

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self._balance += amount
        self._transactions.append(("deposit", amount))

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Withdrawal must be positive")
        if amount > self._balance:
            raise InsufficientFundsError(f"Cannot withdraw {amount}, balance is {self._balance}")
        self._balance -= amount
        self._transactions.append(("withdrawal", amount))

    def transfer_to(self, other: "BankAccount", amount: float) -> None:
        self.withdraw(amount)
        other.deposit(amount)

    @property
    def transaction_count(self) -> int:
        return len(self._transactions)

    def __repr__(self):
        return f"BankAccount({self.owner!r}, balance={self._balance:.2f})"

# ═══════════════════════════════════════════
# 2. Minimal test runner (no pytest needed)
# ═══════════════════════════════════════════
_tests: list[tuple[str, Callable]] = []
_failures: list[str] = []
_passes: int = 0

def test(fn: Callable | None = None, *, skip: bool = False):
    """Register a test function."""
    if fn is None:
        return lambda f: test(f, skip=skip)
    _tests.append((fn.__name__, fn, skip))
    return fn

def run_tests():
    global _passes, _failures
    _passes = 0
    _failures = []
    for name, fn, skip in _tests:
        if skip:
            print(f"  s {name}")
            continue
        try:
            fn()
            _passes += 1
            print(f"  ✓ {name}")
        except AssertionError as e:
            _failures.append((name, str(e)))
            print(f"  ✗ {name}: {e}")
        except Exception as e:
            _failures.append((name, f"{type(e).__name__}: {e}"))
            print(f"  ✗ {name}: {type(e).__name__}: {e}")
    print(f"\n  {_passes}/{len(_tests)} passed, {len(_failures)} failed")

def assert_raises(exc_type, fn, *args, **kwargs):
    try:
        fn(*args, **kwargs)
        raise AssertionError(f"Expected {exc_type.__name__} but nothing was raised")
    except exc_type:
        pass

# ═══════════════════════════════════════════
# 3. Tests
# ═══════════════════════════════════════════
@test
def test_initial_balance():
    acc = BankAccount("Alice", 100.0)
    assert acc.balance == 100.0
    assert acc.owner == "Alice"

@test
def test_deposit_increases_balance():
    acc = BankAccount("Bob")
    acc.deposit(50.0)
    acc.deposit(25.5)
    assert acc.balance == 75.5

@test
def test_withdraw_decreases_balance():
    acc = BankAccount("Carol", 200.0)
    acc.withdraw(75.0)
    assert acc.balance == 125.0

@test
def test_withdraw_exact_balance():
    acc = BankAccount("Dave", 100.0)
    acc.withdraw(100.0)
    assert acc.balance == 0.0

@test
def test_insufficient_funds_raises():
    acc = BankAccount("Eve", 50.0)
    assert_raises(InsufficientFundsError, acc.withdraw, 100.0)
    # Balance unchanged after failed withdrawal
    assert acc.balance == 50.0

@test
def test_negative_deposit_raises():
    acc = BankAccount("Frank")
    assert_raises(ValueError, acc.deposit, -10.0)

@test
def test_zero_deposit_raises():
    acc = BankAccount("Grace")
    assert_raises(ValueError, acc.deposit, 0)

@test
def test_negative_balance_raises():
    assert_raises(ValueError, BankAccount, "Harry", -1.0)

@test
def test_transfer_between_accounts():
    alice = BankAccount("Alice", 500.0)
    bob   = BankAccount("Bob",    100.0)
    alice.transfer_to(bob, 200.0)
    assert alice.balance == 300.0
    assert bob.balance   == 300.0

@test
def test_transfer_insufficient_funds():
    alice = BankAccount("Alice", 50.0)
    bob   = BankAccount("Bob",    0.0)
    assert_raises(InsufficientFundsError, alice.transfer_to, bob, 100.0)
    # Neither account should be modified
    assert alice.balance == 50.0
    assert bob.balance   == 0.0

@test
def test_transaction_count():
    acc = BankAccount("Test", 100.0)
    assert acc.transaction_count == 0
    acc.deposit(10.0)
    acc.withdraw(5.0)
    assert acc.transaction_count == 2

@test
def test_multiple_transactions():
    acc = BankAccount("Multi", 1000.0)
    for i in range(10):
        acc.deposit(i * 10)
    expected_balance = 1000.0 + sum(i * 10 for i in range(10))
    assert acc.balance == expected_balance

# ═══════════════════════════════════════════
# 4. Pytest fixture patterns
# ═══════════════════════════════════════════
PYTEST_FIXTURE_EXAMPLE = '''
# pytest fixture patterns (syntax reference — requires pytest)

import pytest
from myapp.bank import BankAccount, InsufficientFundsError

# ─── Fixtures ───
@pytest.fixture
def empty_account():
    """Fresh account with no balance."""
    return BankAccount("Test User")

@pytest.fixture
def funded_account():
    """Account seeded with $1000."""
    return BankAccount("Rich User", 1000.0)

@pytest.fixture(scope="module")
def db_connection():
    """Module-scoped fixture — created once per test module."""
    conn = create_test_db()
    yield conn           # test runs here
    conn.close()         # teardown

# ─── Parametrize ───
@pytest.mark.parametrize("amount,expected", [
    (100.0, 100.0),
    (0.01,  0.01),
    (9999.99, 9999.99),
])
def test_deposit_amounts(empty_account, amount, expected):
    empty_account.deposit(amount)
    assert empty_account.balance == pytest.approx(expected)

# ─── Exception testing ───
def test_overdraft(funded_account):
    with pytest.raises(InsufficientFundsError, match="Cannot withdraw"):
        funded_account.withdraw(9999.0)

# ─── Marks ───
@pytest.mark.slow
def test_high_volume_transactions(funded_account):
    for _ in range(10_000):
        funded_account.deposit(1.0)
    assert funded_account.balance > 1000.0

@pytest.mark.skip(reason="Feature not implemented yet")
def test_interest_calculation():
    pass

# ─── Conftest.py patterns ───
# conftest.py lives alongside tests; fixtures defined there are auto-discovered.
'''

if __name__ == "__main__":
    print("=== Running BankAccount Tests ===\n")
    run_tests()
    print("\n=== Pytest Fixture Reference ===")
    print(PYTEST_FIXTURE_EXAMPLE)
