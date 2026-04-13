"""
Intermediate: Comprehensions and data processing.
"""

# === List comprehensions ===
print("=== List Comprehensions ===")

# Basic
squares = [x**2 for x in range(10)]
print(f"Squares: {squares}")

# With condition
evens = [x for x in range(20) if x % 2 == 0]
print(f"Evens: {evens}")

# Nested
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [x for row in matrix for x in row]
print(f"Flattened: {flat}")

# Conditional expression
labels = ["even" if x % 2 == 0 else "odd" for x in range(6)]
print(f"Labels: {labels}")

# === Dict comprehensions ===
print("\n=== Dict Comprehensions ===")

# Basic
squares_dict = {x: x**2 for x in range(6)}
print(f"Squares dict: {squares_dict}")

# Inverting a dict
original = {"a": 1, "b": 2, "c": 3}
inverted = {v: k for k, v in original.items()}
print(f"Inverted: {inverted}")

# Filtering
scores = {"Alice": 95, "Bob": 67, "Charlie": 82, "Diana": 91}
passing = {k: v for k, v in scores.items() if v >= 80}
print(f"Passing: {passing}")

# From two lists
keys = ["name", "age", "city"]
values = ["Alice", 30, "NYC"]
combined = {k: v for k, v in zip(keys, values)}
print(f"Combined: {combined}")

# === Set comprehensions ===
print("\n=== Set Comprehensions ===")

words = "hello world hello python world python".split()
unique_lengths = {len(w) for w in words}
print(f"Unique word lengths: {unique_lengths}")

# === Generator expressions ===
print("\n=== Generator Expressions ===")
import sys

# Memory efficient
gen_sum = sum(x**2 for x in range(1_000_000))
print(f"Sum of squares (1M): {gen_sum}")

# Lazy evaluation
gen = (x**2 for x in range(10))
print(f"Generator: {gen}")
print(f"First 3: {next(gen)}, {next(gen)}, {next(gen)}")

# === Data processing pipeline ===
print("\n=== Data Processing ===")

students = [
    {"name": "Alice", "grades": [90, 85, 92, 88]},
    {"name": "Bob", "grades": [78, 82, 75, 80]},
    {"name": "Charlie", "grades": [95, 98, 92, 96]},
    {"name": "Diana", "grades": [65, 70, 72, 68]},
    {"name": "Eve", "grades": [88, 91, 85, 90]},
]

# Pipeline: calculate averages -> filter -> sort -> format
results = sorted(
    [
        {"name": s["name"], "avg": sum(s["grades"]) / len(s["grades"])}
        for s in students
    ],
    key=lambda x: x["avg"],
    reverse=True
)

print("Student rankings:")
for i, r in enumerate(results, 1):
    status = "Honor Roll" if r["avg"] >= 90 else "Pass" if r["avg"] >= 70 else "At Risk"
    print(f"  {i}. {r['name']}: {r['avg']:.1f} ({status})")

# === Walrus operator in comprehensions ===
print("\n=== Walrus Operator ===")
data = [1, 5, 3, 8, 2, 9, 4, 7, 6]
# Process and filter in one pass
results = [(x, y) for x in data if (y := x**2) > 20]
print(f"Values with square > 20: {results}")
