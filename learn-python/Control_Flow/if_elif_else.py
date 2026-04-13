"""
Control flow: if, elif, else - comprehensive examples.
"""

# Basic if/elif/else
score = 85
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"
print(f"Score {score} -> Grade {grade}")

# Ternary operator
age = 20
status = "adult" if age >= 18 else "minor"
print(f"Age {age} -> {status}")

# Nested ternary (use sparingly)
x = 0
result = "positive" if x > 0 else "negative" if x < 0 else "zero"
print(f"{x} is {result}")

# Truthy / Falsy values
values = [0, 1, "", "hello", [], [1], {}, {"a": 1}, None, True, False]
for v in values:
    print(f"  bool({v!r:12s}) = {bool(v)}")

# Chained comparisons
x = 15
print(f"\n10 < {x} < 20: {10 < x < 20}")
print(f"1 <= {x} <= 100: {1 <= x <= 100}")

# Walrus operator (:=) Python 3.8+
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
if (n := len(data)) > 5:
    print(f"\nList has {n} elements (more than 5)")

# Pattern matching (Python 3.10+)
def http_status(status):
    match status:
        case 200:
            return "OK"
        case 301:
            return "Moved Permanently"
        case 404:
            return "Not Found"
        case 500:
            return "Internal Server Error"
        case _:
            return "Unknown"

for code in [200, 301, 404, 500, 418]:
    print(f"HTTP {code}: {http_status(code)}")

# Guard patterns
def classify_number(n):
    match n:
        case x if x < 0:
            return "negative"
        case 0:
            return "zero"
        case x if x % 2 == 0:
            return "positive even"
        case _:
            return "positive odd"

for n in [-5, 0, 4, 7]:
    print(f"  {n}: {classify_number(n)}")
