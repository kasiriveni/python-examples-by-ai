"""
Sets and Frozensets in Python.
"""

# Creating sets
empty = set()
numbers = {1, 2, 3, 4, 5}
from_list = set([1, 2, 2, 3, 3, 3])
from_string = set("mississippi")
print(f"From list (deduped): {from_list}")
print(f"From string: {from_string}")

# Set operations
a = {1, 2, 3, 4, 5}
b = {4, 5, 6, 7, 8}

print(f"Union: {a | b}")
print(f"Intersection: {a & b}")
print(f"Difference (a-b): {a - b}")
print(f"Symmetric difference: {a ^ b}")

# Subset and superset
print(f"{{1,2}} <= {{1,2,3}}: { {1,2} <= {1,2,3} }")
print(f"{{1,2,3}} >= {{1,2}}: { {1,2,3} >= {1,2} }")
print(f"Disjoint: {a.isdisjoint({10, 11})}")

# Set methods
s = {1, 2, 3}
s.add(4)
s.update([5, 6])
s.discard(6)       # no error if missing
s.remove(5)        # raises KeyError if missing
popped = s.pop()   # removes arbitrary element
print(f"After operations: {s}, popped: {popped}")

# Set comprehension
even_squares = {x**2 for x in range(10) if x % 2 == 0}
print(f"Even squares: {even_squares}")

# Frozenset (immutable set, can be used as dict key)
fs = frozenset([1, 2, 3])
print(f"Frozenset: {fs}")

# Using frozenset as dict key
cache = {frozenset({1, 2}): "pair", frozenset({3}): "single"}
print(f"Cache lookup: {cache[frozenset({1, 2})]}")

# Practical: removing duplicates while preserving order
items = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
seen = set()
unique = []
for item in items:
    if item not in seen:
        seen.add(item)
        unique.append(item)
print(f"Unique (order preserved): {unique}")
