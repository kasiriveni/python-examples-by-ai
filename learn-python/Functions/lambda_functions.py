"""
Lambda functions in Python.
"""

# Basic lambda
square = lambda x: x ** 2
add = lambda x, y: x + y
print(f"square(5) = {square(5)}")
print(f"add(3, 4) = {add(3, 4)}")

# Lambda with conditionals
classify = lambda x: "positive" if x > 0 else ("negative" if x < 0 else "zero")
print(f"classify(5) = {classify(5)}")
print(f"classify(-3) = {classify(-3)}")
print(f"classify(0) = {classify(0)}")

# Sorting with lambda
students = [
    {"name": "Charlie", "grade": 85},
    {"name": "Alice", "grade": 92},
    {"name": "Bob", "grade": 78},
]
by_name = sorted(students, key=lambda s: s["name"])
by_grade = sorted(students, key=lambda s: s["grade"], reverse=True)
print(f"\nBy name: {[s['name'] for s in by_name]}")
print(f"By grade: {[s['name'] for s in by_grade]}")

# Multi-key sorting
data = [(1, 'b'), (2, 'a'), (1, 'a'), (2, 'b')]
sorted_data = sorted(data, key=lambda x: (x[0], x[1]))
print(f"Multi-key sort: {sorted_data}")

# Lambda with map and filter
numbers = list(range(1, 11))
doubled = list(map(lambda x: x * 2, numbers))
odds = list(filter(lambda x: x % 2 != 0, numbers))
print(f"\nDoubled: {doubled}")
print(f"Odds: {odds}")

# Lambda in dictionary
operations = {
    '+': lambda a, b: a + b,
    '-': lambda a, b: a - b,
    '*': lambda a, b: a * b,
    '/': lambda a, b: a / b if b != 0 else float('inf'),
}

for op, func in operations.items():
    print(f"10 {op} 3 = {func(10, 3)}")

# Immediately invoked lambda
result = (lambda x, y: x + y)(5, 3)
print(f"\nImmediately invoked: {result}")

# Lambda with default arguments
increment = lambda x, step=1: x + step
print(f"increment(5) = {increment(5)}")
print(f"increment(5, 3) = {increment(5, 3)}")
