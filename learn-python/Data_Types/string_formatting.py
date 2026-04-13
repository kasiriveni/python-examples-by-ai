"""
String formatting in Python - all approaches.
"""

name = "Alice"
age = 30
pi = 3.14159265

# 1. f-strings (recommended, Python 3.6+)
print(f"Hello, {name}! You are {age} years old.")
print(f"Pi to 2 decimals: {pi:.2f}")
print(f"Pi in scientific: {pi:.2e}")
print(f"Large number: {1000000:,.0f}")
print(f"Percentage: {0.856:.1%}")
print(f"Binary: {255:08b}")
print(f"Hex: {255:#06x}")
print(f"Padded: {'hello':>20}")
print(f"Centered: {'hello':^20}")
print(f"Left aligned: {'hello':<20}|")

# Debug format (Python 3.8+)
x = 42
print(f"{x = }")
print(f"{x**2 = }")

# 2. str.format()
print("Hello, {}! Age: {}".format(name, age))
print("Hello, {0}! {0} is {1} years old.".format(name, age))
print("Hello, {name}! Age: {age}".format(name=name, age=age))

# 3. %-formatting (old style)
print("Hello, %s! Age: %d" % (name, age))
print("Pi: %.2f" % pi)

# 4. Template strings (safe for user input)
from string import Template
t = Template("Hello, $name! Age: $age")
print(t.substitute(name=name, age=age))
print(t.safe_substitute(name=name))  # missing keys stay as-is

# Multi-line f-strings
message = (
    f"Name: {name}\n"
    f"Age: {age}\n"
    f"Pi: {pi:.4f}"
)
print(message)

# Format spec mini-language
for align, fill, width in [('<', '.', 20), ('>', '.', 20), ('^', '.', 20)]:
    print(f"{'hello':{fill}{align}{width}}")
