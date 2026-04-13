"""
Magic/dunder methods in Python.
"""

class Money:
    """Demonstrates various dunder methods."""

    def __init__(self, amount, currency="USD"):
        self.amount = round(amount, 2)
        self.currency = currency

    # String representations
    def __str__(self):
        return f"${self.amount:.2f} {self.currency}"

    def __repr__(self):
        return f"Money({self.amount}, '{self.currency}')"

    # Arithmetic
    def __add__(self, other):
        if isinstance(other, Money):
            if self.currency != other.currency:
                raise ValueError("Cannot add different currencies")
            return Money(self.amount + other.amount, self.currency)
        return Money(self.amount + other, self.currency)

    def __radd__(self, other):
        return self.__add__(Money(other, self.currency))

    def __sub__(self, other):
        if isinstance(other, Money):
            return Money(self.amount - other.amount, self.currency)
        return Money(self.amount - other, self.currency)

    def __mul__(self, factor):
        return Money(self.amount * factor, self.currency)

    def __rmul__(self, factor):
        return self.__mul__(factor)

    def __neg__(self):
        return Money(-self.amount, self.currency)

    # Comparison
    def __eq__(self, other):
        return self.amount == other.amount and self.currency == other.currency

    def __lt__(self, other):
        return self.amount < other.amount

    def __le__(self, other):
        return self.amount <= other.amount

    def __gt__(self, other):
        return self.amount > other.amount

    # Hashing (required if __eq__ is defined)
    def __hash__(self):
        return hash((self.amount, self.currency))

    # Boolean
    def __bool__(self):
        return self.amount != 0

    # Format
    def __format__(self, spec):
        if spec == "short":
            return f"${self.amount:.0f}"
        return str(self)

    # Context manager
    def __enter__(self):
        print(f"Starting transaction: {self}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"Transaction complete: {self}")
        return False


class InfiniteCounter:
    """Demonstrates __iter__ and __next__."""
    def __init__(self, start=0):
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        value = self.current
        self.current += 1
        return value


if __name__ == "__main__":
    m1 = Money(100)
    m2 = Money(50)

    print(f"m1 = {m1}")
    print(f"m1 + m2 = {m1 + m2}")
    print(f"m1 * 3 = {m1 * 3}")
    print(f"m1 > m2: {m1 > m2}")
    print(f"format short: {m1:short}")
    print(f"repr: {repr(m1)}")
    print(f"bool(Money(0)): {bool(Money(0))}")

    # Context manager
    with Money(500) as budget:
        print(f"  Working with {budget}")

    # Iterator
    counter = InfiniteCounter(10)
    for i, val in enumerate(counter):
        if i >= 5:
            break
        print(f"  Counter: {val}")
