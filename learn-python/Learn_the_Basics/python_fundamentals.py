"""
Learn the Basics: Python fundamentals quick reference.
"""

# === 1. Hello World ===
print("=== Hello World ===")
print("Hello, Python!")

# === 2. Variables ===
print("\n=== Variables ===")
name = "Python"     # str
version = 3.12      # float
year = 2024         # int
is_fun = True       # bool
nothing = None      # NoneType

print(f"{name} {version} ({year}), Fun: {is_fun}")

# === 3. Input/Output ===
print("\n=== Input/Output ===")
# name = input("Enter your name: ")  # Interactive input
# print(f"Hello, {name}!")
print("Use input() to get user input")

# === 4. Math ===
print("\n=== Math Operations ===")
print(f"10 + 3 = {10 + 3}")
print(f"10 - 3 = {10 - 3}")
print(f"10 * 3 = {10 * 3}")
print(f"10 / 3 = {10 / 3:.2f}")
print(f"10 // 3 = {10 // 3}")  # Floor division
print(f"10 % 3 = {10 % 3}")    # Modulus
print(f"2 ** 10 = {2 ** 10}")   # Power

import math
print(f"sqrt(16) = {math.sqrt(16)}")
print(f"pi = {math.pi:.4f}")

# === 5. Strings ===
print("\n=== Strings ===")
s = "Hello, World!"
print(f"Length: {len(s)}")
print(f"Upper: {s.upper()}")
print(f"Lower: {s.lower()}")
print(f"Split: {s.split(', ')}")
print(f"Replace: {s.replace('World', 'Python')}")
print(f"Slice [0:5]: {s[0:5]}")
print(f"Reverse: {s[::-1]}")

# Multi-line strings
poem = """
Roses are red,
Violets are blue,
Python is great,
And so are you!
"""
print(poem.strip())

# === 6. Lists ===
print("\n=== Lists ===")
numbers = [1, 2, 3, 4, 5]
print(f"List: {numbers}")
print(f"First: {numbers[0]}, Last: {numbers[-1]}")
numbers.append(6)
print(f"After append: {numbers}")
print(f"Sum: {sum(numbers)}, Len: {len(numbers)}")

# === 7. Conditionals ===
print("\n=== Conditionals ===")
age = 20
if age >= 18:
    print(f"Age {age}: Adult")
elif age >= 13:
    print(f"Age {age}: Teenager")
else:
    print(f"Age {age}: Child")

# === 8. Loops ===
print("\n=== Loops ===")
for fruit in ["apple", "banana", "cherry"]:
    print(f"  Fruit: {fruit}")

for i in range(3):
    print(f"  Count: {i}")

# === 9. Functions ===
print("\n=== Functions ===")

def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

print(greet("Alice"))
print(greet("Bob", "Hi"))

# === 10. Dictionaries ===
print("\n=== Dictionaries ===")
person = {"name": "Alice", "age": 30}
print(f"Name: {person['name']}")
person["city"] = "NYC"
for key, value in person.items():
    print(f"  {key}: {value}")

# === 11. Error Handling ===
print("\n=== Error Handling ===")
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero!")
finally:
    print("This always runs")

# === 12. Files ===
print("\n=== File I/O ===")
print("# Writing: open('file.txt', 'w') as f: f.write('hello')")
print("# Reading: open('file.txt', 'r') as f: f.read()")
print("# Append:  open('file.txt', 'a') as f: f.write('more')")
