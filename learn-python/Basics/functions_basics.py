"""
Basics: Functions and scope.
"""

# === Defining functions ===
print("=== Basic Functions ===")

def greet(name):
    return f"Hello, {name}!"

print(greet("Alice"))

# === Default arguments ===
def power(base, exponent=2):
    return base ** exponent

print(f"3^2 = {power(3)}")
print(f"2^10 = {power(2, 10)}")

# === *args and **kwargs ===
print("\n=== *args and **kwargs ===")

def sum_all(*args):
    return sum(args)

print(f"sum_all(1, 2, 3, 4) = {sum_all(1, 2, 3, 4)}")

def build_profile(**kwargs):
    return {k: v for k, v in kwargs.items()}

profile = build_profile(name="Alice", age=30, city="NYC")
print(f"Profile: {profile}")

def mixed(a, b, *args, key="default", **kwargs):
    print(f"  a={a}, b={b}")
    print(f"  args={args}")
    print(f"  key={key}")
    print(f"  kwargs={kwargs}")

mixed(1, 2, 3, 4, key="custom", x=10, y=20)

# === Return multiple values ===
print("\n=== Multiple Returns ===")

def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([5, 2, 8, 1, 9])
print(f"Min: {lo}, Max: {hi}")

# === Lambda functions ===
print("\n=== Lambda ===")

square = lambda x: x ** 2
add = lambda x, y: x + y

print(f"square(5) = {square(5)}")
print(f"add(3, 4) = {add(3, 4)}")

# Sort with custom key
students = [("Alice", 90), ("Bob", 75), ("Charlie", 85)]
students.sort(key=lambda s: s[1], reverse=True)
print(f"Sorted by grade: {students}")

# === Scope ===
print("\n=== Scope ===")

global_var = "I'm global"

def outer():
    outer_var = "I'm from outer"

    def inner():
        inner_var = "I'm from inner"
        print(f"  inner sees: {inner_var}, {outer_var}, {global_var}")

    inner()
    print(f"  outer sees: {outer_var}, {global_var}")

outer()

# === Docstrings ===
print("\n=== Docstrings ===")

def calculate_bmi(weight_kg, height_m):
    """
    Calculate Body Mass Index.

    Args:
        weight_kg: Weight in kilograms
        height_m: Height in meters

    Returns:
        BMI value as float
    """
    return weight_kg / (height_m ** 2)

bmi = calculate_bmi(70, 1.75)
print(f"BMI: {bmi:.1f}")
print(f"Docstring: {calculate_bmi.__doc__.strip().split(chr(10))[0]}")

# === Type hints ===
print("\n=== Type Hints ===")

def add_numbers(a: int, b: int) -> int:
    return a + b

def greet_list(names: list[str]) -> list[str]:
    return [f"Hello, {name}!" for name in names]

print(add_numbers(5, 3))
print(greet_list(["Alice", "Bob"]))
