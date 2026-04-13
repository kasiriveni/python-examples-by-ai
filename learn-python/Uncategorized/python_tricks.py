"""
Uncategorized: Useful Python tricks and idioms.
"""
from contextlib import suppress
import operator

# === 1. Useful built-in functions ===
print("=== Built-in Functions ===")

# any/all
numbers = [1, 2, 3, 4, 5]
print(f"Any > 4: {any(x > 4 for x in numbers)}")
print(f"All > 0: {all(x > 0 for x in numbers)}")

# zip with fill
from itertools import zip_longest
a = [1, 2, 3]
b = ['a', 'b']
print(f"zip_longest: {list(zip_longest(a, b, fillvalue='?'))}")

# sorted with key
students = [("Alice", 90), ("Bob", 75), ("Charlie", 85)]
by_score = sorted(students, key=operator.itemgetter(1), reverse=True)
print(f"By score: {by_score}")

# filter with None removes falsy values
data = [0, 1, None, '', 'hello', [], [1], False, True]
truthy = list(filter(None, data))
print(f"Truthy values: {truthy}")

# === 2. Dictionary tricks ===
print("\n=== Dict Tricks ===")

# Merge dicts
d1 = {"a": 1, "b": 2}
d2 = {"b": 3, "c": 4}
merged = d1 | d2
print(f"Merged: {merged}")

# Dict from pairs
pairs = [("x", 1), ("y", 2), ("z", 3)]
d = dict(pairs)
print(f"From pairs: {d}")

# Invert dict
inverted = {v: k for k, v in d.items()}
print(f"Inverted: {inverted}")

# setdefault
graph = {}
edges = [("a", "b"), ("a", "c"), ("b", "c"), ("c", "d")]
for src, dst in edges:
    graph.setdefault(src, []).append(dst)
print(f"Graph: {graph}")

# === 3. String tricks ===
print("\n=== String Tricks ===")

# Join with filter
parts = ["hello", "", "world", None, "!"]
clean = " ".join(filter(None, parts))
print(f"Joined: {clean}")

# Center/justify
print("centered".center(30, '-'))
print("left".ljust(30, '.'))
print("right".rjust(30, '.'))

# === 4. Unpacking tricks ===
print("\n=== Unpacking ===")

# Extended unpacking
first, *middle, last = range(10)
print(f"first={first}, middle={middle}, last={last}")

# Swap
a, b = 10, 20
a, b = b, a
print(f"Swapped: a={a}, b={b}")

# Nested unpacking
data = [(1, (2, 3)), (4, (5, 6))]
for x, (y, z) in data:
    print(f"  x={x}, y={y}, z={z}")

# === 5. One-liners ===
print("\n=== One-liners ===")

# Flatten
nested = [[1, 2], [3, 4], [5, 6]]
flat = [x for sub in nested for x in sub]
print(f"Flatten: {flat}")

# Transpose
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
transposed = list(map(list, zip(*matrix)))
print(f"Transpose: {transposed}")

# Most common
from collections import Counter
words = "the cat sat on the mat the cat".split()
print(f"Most common: {Counter(words).most_common(2)}")

# === 6. Context managers ===
print("\n=== Suppress Errors ===")

# Suppress specific exceptions
with suppress(FileNotFoundError):
    with open("nonexistent.txt") as f:
        content = f.read()
print("No crash from missing file!")

# === 7. Conditional expressions ===
print("\n=== Conditionals ===")

# Chained comparison
x = 5
print(f"1 < {x} < 10: {1 < x < 10}")

# or for defaults
name = "" or "Anonymous"
print(f"Default name: {name}")

# Conditional dict
config = {"debug": True, **({"verbose": True} if True else {})}
print(f"Config: {config}")

# === 8. functools useful tools ===
print("\n=== functools ===")

from functools import lru_cache, reduce, partial

@lru_cache(maxsize=128)
def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)

print(f"fib(30) = {fib(30)}")
print(f"Cache info: {fib.cache_info()}")

# Partial
def power(base, exponent):
    return base ** exponent

square = partial(power, exponent=2)
cube = partial(power, exponent=3)
print(f"square(5) = {square(5)}, cube(3) = {cube(3)}")

# Reduce
product = reduce(operator.mul, [1, 2, 3, 4, 5])
print(f"Product: {product}")
