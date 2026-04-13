"""
Tuples in Python - comprehensive examples.
"""

# Creating tuples
empty = ()
single = (42,)  # note the comma
coords = (3, 4)
mixed = (1, "hello", 3.14, True)
nested = ((1, 2), (3, 4), (5, 6))

# From iterable
from_range = tuple(range(5))
from_string = tuple("hello")
print(f"From range: {from_range}")
print(f"From string: {from_string}")

# Tuple unpacking
x, y = coords
print(f"x={x}, y={y}")

# Swap variables using tuples
a, b = 10, 20
a, b = b, a
print(f"After swap: a={a}, b={b}")

# Extended unpacking
first, *rest = (1, 2, 3, 4, 5)
print(f"first={first}, rest={rest}")

# Named tuples
from collections import namedtuple
Point = namedtuple('Point', ['x', 'y'])
p = Point(3, 4)
print(f"Point: {p}, x={p.x}, y={p.y}")
print(f"As dict: {p._asdict()}")

# Replace values (returns new namedtuple)
p2 = p._replace(x=10)
print(f"Replaced: {p2}")

# Tuple methods
numbers = (1, 2, 3, 2, 4, 2, 5)
print(f"Count of 2: {numbers.count(2)}")
print(f"Index of 3: {numbers.index(3)}")

# Tuples as dictionary keys (they're hashable)
grid = {}
grid[(0, 0)] = "origin"
grid[(1, 0)] = "right"
grid[(0, 1)] = "up"
print(f"Grid: {grid}")

# Tuple comparison (lexicographic)
print(f"(1, 2) < (1, 3): {(1, 2) < (1, 3)}")
print(f"(1, 2) < (2, 0): {(1, 2) < (2, 0)}")

# Tuple as function return
def min_max(items):
    return min(items), max(items)

lo, hi = min_max([5, 2, 8, 1, 9])
print(f"Min: {lo}, Max: {hi}")
