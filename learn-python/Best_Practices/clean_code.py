"""
Best practices: Clean code in Python.
"""

# === 1. Use descriptive names ===
# Bad
def calc(x, y, z):
    return x * y * (1 + z)

# Good
def calculate_total_price(quantity, unit_price, tax_rate):
    return quantity * unit_price * (1 + tax_rate)

# === 2. Keep functions small and focused ===
def read_config(filepath):
    """Read configuration from a JSON file."""
    import json
    with open(filepath) as f:
        return json.load(f)

def validate_config(config):
    """Validate configuration has required keys."""
    required = {"host", "port", "database"}
    missing = required - set(config.keys())
    if missing:
        raise ValueError(f"Missing config keys: {missing}")
    return True

# === 3. Use constants instead of magic numbers ===
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30
HTTP_OK = 200
HTTP_NOT_FOUND = 404

# === 4. Use context managers for resource management ===
# Bad: file might not be closed on error
# f = open("data.txt")
# data = f.read()
# f.close()

# Good
# with open("data.txt") as f:
#     data = f.read()

# === 5. Use list comprehensions over map/filter ===
numbers = range(10)

# Prefer
evens = [n for n in numbers if n % 2 == 0]
squares = [n**2 for n in numbers]

# Over
evens_map = list(filter(lambda n: n % 2 == 0, numbers))
squares_map = list(map(lambda n: n**2, numbers))

# === 6. Use unpacking ===
# Bad
point = (3, 4)
x = point[0]
y = point[1]

# Good
x, y = (3, 4)

# === 7. Use enumerate instead of range(len()) ===
fruits = ["apple", "banana", "cherry"]

# Bad
for i in range(len(fruits)):
    print(f"  {i}: {fruits[i]}")

# Good
for i, fruit in enumerate(fruits):
    print(f"  {i}: {fruit}")

# === 8. Use guard clauses (early returns) ===
# Bad
def process_order_bad(order):
    if order is not None:
        if order.get("status") == "valid":
            if order.get("items"):
                return f"Processing {len(order['items'])} items"
    return None

# Good
def process_order(order):
    if order is None:
        return None
    if order.get("status") != "valid":
        return None
    if not order.get("items"):
        return None
    return f"Processing {len(order['items'])} items"

# === 9. Use dataclasses for data containers ===
from dataclasses import dataclass

@dataclass
class User:
    name: str
    email: str
    age: int
    active: bool = True

user = User("Alice", "alice@example.com", 30)
print(f"\nUser: {user}")

# === 10. Use EAFP (Easier to Ask Forgiveness than Permission) ===
data = {"name": "Alice"}

# LBYL (Look Before You Leap) - Less Pythonic
if "age" in data:
    age = data["age"]
else:
    age = None

# EAFP - More Pythonic
try:
    age = data["age"]
except KeyError:
    age = None

# Even better
age = data.get("age")

# === 11. Use pathlib over os.path ===
from pathlib import Path

# Bad: os.path.join("src", "utils", "helpers.py")
# Good:
path = Path("src") / "utils" / "helpers.py"

# === 12. Use f-strings ===
name = "Alice"
age = 30

# Bad: "Hello %s, you are %d" % (name, age)
# Bad: "Hello {}, you are {}".format(name, age)
# Good:
greeting = f"Hello {name}, you are {age}"
print(greeting)
