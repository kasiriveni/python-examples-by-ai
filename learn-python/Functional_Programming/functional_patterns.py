"""
Functional Programming: Advanced functional patterns.
"""
from functools import reduce, partial, wraps
from itertools import chain, starmap, accumulate
from operator import add, mul, itemgetter

# === Pure functions ===
print("=== Pure Functions ===")

# Pure: same input -> same output, no side effects
def add(a, b):
    return a + b

def multiply_list(numbers, factor):
    return [n * factor for n in numbers]

print(f"add(3, 4) = {add(3, 4)}")
print(f"multiply_list([1,2,3], 5) = {multiply_list([1, 2, 3], 5)}")

# === Higher-order functions ===
print("\n=== Higher-Order Functions ===")

def apply_operation(func, a, b):
    return func(a, b)

print(f"apply_operation(add, 3, 4) = {apply_operation(add, 3, 4)}")
print(f"apply_operation(mul, 3, 4) = {apply_operation(mul, 3, 4)}")

# Function composition
def compose(*functions):
    def composed(x):
        result = x
        for f in reversed(functions):
            result = f(result)
        return result
    return composed

double = lambda x: x * 2
increment = lambda x: x + 1
square = lambda x: x ** 2

transform = compose(square, increment, double)  # square(increment(double(x)))
print(f"compose(square, inc, double)(3) = {transform(3)}")  # square(inc(6)) = square(7) = 49

# Pipe (left-to-right composition)
def pipe(*functions):
    def piped(x):
        result = x
        for f in functions:
            result = f(result)
        return result
    return piped

transform2 = pipe(double, increment, square)  # double(3)=6, inc=7, square=49
print(f"pipe(double, inc, square)(3) = {transform2(3)}")

# === Map, Filter, Reduce ===
print("\n=== Map/Filter/Reduce ===")

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Map
squared = list(map(lambda x: x**2, numbers))
print(f"Map (square): {squared}")

# Filter
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(f"Filter (even): {evens}")

# Reduce
total = reduce(add, numbers)
product = reduce(mul, numbers)
print(f"Reduce (sum): {total}")
print(f"Reduce (product): {product}")

# Accumulate (running totals)
running = list(accumulate(numbers, add))
print(f"Accumulate (sum): {running}")

# === Currying ===
print("\n=== Currying ===")

def curry(func):
    """Auto-curry a function."""
    import inspect
    sig = inspect.signature(func)
    n_params = len(sig.parameters)

    @wraps(func)
    def curried(*args):
        if len(args) >= n_params:
            return func(*args)
        return lambda *more: curried(*args, *more)
    return curried

@curry
def add3(a, b, c):
    return a + b + c

print(f"add3(1, 2, 3) = {add3(1, 2, 3)}")
print(f"add3(1)(2)(3) = {add3(1)(2)(3)}")
add_10 = add3(10)
print(f"add3(10)(5)(3) = {add_10(5)(3)}")

# === Immutable data transformations ===
print("\n=== Immutable Transforms ===")

def update_dict(d, **kwargs):
    """Return new dict with updates (immutable)."""
    return {**d, **kwargs}

def remove_key(d, key):
    """Return new dict without key (immutable)."""
    return {k: v for k, v in d.items() if k != key}

original = {"name": "Alice", "age": 30, "city": "NYC"}
updated = update_dict(original, age=31, email="alice@test.com")
without_city = remove_key(original, "city")

print(f"Original: {original}")
print(f"Updated:  {updated}")
print(f"Without city: {without_city}")

# === Monadic-style chaining ===
print("\n=== Maybe Monad (Optional Chaining) ===")

class Maybe:
    def __init__(self, value):
        self._value = value

    @staticmethod
    def of(value):
        return Maybe(value)

    def map(self, func):
        if self._value is None:
            return Maybe(None)
        try:
            return Maybe(func(self._value))
        except Exception:
            return Maybe(None)

    def flat_map(self, func):
        if self._value is None:
            return Maybe(None)
        return func(self._value)

    def get_or_else(self, default):
        return self._value if self._value is not None else default

    def __repr__(self):
        return f"Maybe({self._value})"

result = (Maybe.of({"user": {"name": "Alice", "age": 30}})
          .map(lambda d: d.get("user"))
          .map(lambda u: u.get("name"))
          .map(str.upper)
          .get_or_else("Unknown"))
print(f"Chained: {result}")

result2 = (Maybe.of(None)
           .map(lambda d: d.get("user"))
           .get_or_else("Unknown"))
print(f"None chain: {result2}")
