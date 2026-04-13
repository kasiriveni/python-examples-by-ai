"""
Beginner: Lists, tuples, and basic data structures.
"""

# === Lists ===
print("=== Lists ===")
fruits = ["apple", "banana", "cherry", "date"]
print(f"Fruits: {fruits}")
print(f"Length: {len(fruits)}")
print(f"First: {fruits[0]}, Last: {fruits[-1]}")
print(f"Slice [1:3]: {fruits[1:3]}")

# List methods
fruits.append("elderberry")
print(f"After append: {fruits}")

fruits.insert(1, "avocado")
print(f"After insert at 1: {fruits}")

removed = fruits.pop()
print(f"Popped: {removed}, List: {fruits}")

fruits.remove("banana")
print(f"After remove 'banana': {fruits}")

# List operations
numbers = [3, 1, 4, 1, 5, 9, 2, 6]
print(f"\nNumbers: {numbers}")
print(f"Sorted: {sorted(numbers)}")
print(f"Reversed: {list(reversed(numbers))}")
print(f"Sum: {sum(numbers)}")
print(f"Min: {min(numbers)}, Max: {max(numbers)}")
print(f"Count of 1: {numbers.count(1)}")
print(f"Index of 5: {numbers.index(5)}")

# === Tuples (immutable) ===
print("\n=== Tuples ===")
coordinates = (10, 20)
rgb = (255, 128, 0)
single = (42,)  # note the comma

print(f"Coordinates: {coordinates}")
print(f"RGB: {rgb}")
print(f"Single: {single}")

# Tuple unpacking
x, y = coordinates
print(f"Unpacked: x={x}, y={y}")

r, g, b = rgb
print(f"RGB unpacked: r={r}, g={g}, b={b}")

# Extended unpacking
first, *rest = [1, 2, 3, 4, 5]
print(f"First: {first}, Rest: {rest}")

# Named tuples
from collections import namedtuple
Point = namedtuple('Point', ['x', 'y'])
p = Point(3, 4)
print(f"\nNamedTuple: {p}, x={p.x}, y={p.y}")

# === Dictionaries ===
print("\n=== Dictionaries ===")
person = {"name": "Alice", "age": 30, "city": "NYC"}
print(f"Person: {person}")
print(f"Name: {person['name']}")
print(f"Get with default: {person.get('phone', 'N/A')}")

person["email"] = "alice@example.com"
print(f"After adding email: {person}")

# Dictionary methods
print(f"Keys: {list(person.keys())}")
print(f"Values: {list(person.values())}")
print(f"Items: {list(person.items())}")

# Iterate
print("\nIterating:")
for key, value in person.items():
    print(f"  {key}: {value}")

# === Sets ===
print("\n=== Sets ===")
a = {1, 2, 3, 4, 5}
b = {4, 5, 6, 7, 8}
print(f"A: {a}")
print(f"B: {b}")
print(f"Union: {a | b}")
print(f"Intersection: {a & b}")
print(f"Difference (A-B): {a - b}")
print(f"Symmetric diff: {a ^ b}")

# Set operations
colors = {"red", "green", "blue"}
colors.add("yellow")
colors.discard("green")
print(f"\nColors: {colors}")
print(f"'red' in colors: {'red' in colors}")
