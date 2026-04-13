"""
Dictionaries in Python - comprehensive examples.
"""

# Creating dictionaries
empty = {}
person = {"name": "Alice", "age": 30, "city": "NYC"}
from_tuples = dict([("a", 1), ("b", 2), ("c", 3)])
from_kwargs = dict(x=10, y=20, z=30)
from_keys = dict.fromkeys(["a", "b", "c"], 0)

print(f"Person: {person}")
print(f"From tuples: {from_tuples}")
print(f"From kwargs: {from_kwargs}")
print(f"From keys: {from_keys}")

# Accessing values
print(f"Name: {person['name']}")
print(f"Get with default: {person.get('salary', 'N/A')}")

# Dictionary comprehensions
squares = {x: x**2 for x in range(6)}
filtered = {k: v for k, v in person.items() if isinstance(v, str)}
print(f"Squares: {squares}")
print(f"String values only: {filtered}")

# Merging dictionaries
defaults = {"color": "blue", "size": "medium", "weight": 10}
overrides = {"color": "red", "weight": 15}
merged = {**defaults, **overrides}
print(f"Merged: {merged}")

# Using | operator (Python 3.9+)
merged2 = defaults | overrides
print(f"Merged with |: {merged2}")

# Iterating
for key in person:
    print(f"Key: {key}")

for key, value in person.items():
    print(f"{key} = {value}")

# setdefault
inventory = {}
inventory.setdefault("apples", []).append("Granny Smith")
inventory.setdefault("apples", []).append("Fuji")
print(f"Inventory: {inventory}")

# defaultdict
from collections import defaultdict
word_count = defaultdict(int)
for word in "the cat sat on the mat the cat".split():
    word_count[word] += 1
print(f"Word count: {dict(word_count)}")

# OrderedDict
from collections import OrderedDict
od = OrderedDict()
od["first"] = 1
od["second"] = 2
od["third"] = 3
od.move_to_end("first")
print(f"OrderedDict: {od}")

# Counter
from collections import Counter
colors = ["red", "blue", "red", "green", "blue", "red"]
counter = Counter(colors)
print(f"Counter: {counter}")
print(f"Most common: {counter.most_common(2)}")
