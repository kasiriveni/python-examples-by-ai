"""
Function basics in Python.
"""

# Simple function
def greet(name):
    return f"Hello, {name}!"

# Default parameters
def power(base, exponent=2):
    return base ** exponent

# *args and **kwargs
def flexible(*args, **kwargs):
    print(f"Positional: {args}")
    print(f"Keyword: {kwargs}")

# Keyword-only arguments (after *)
def configure(*, host, port, debug=False):
    print(f"Configuring {host}:{port} (debug={debug})")

# Positional-only arguments (before /)
def distance(x1, y1, x2, y2, /):
    return ((x2 - x1)**2 + (y2 - y1)**2) ** 0.5

# Return multiple values
def divmod_custom(a, b):
    return a // b, a % b

# Docstrings
def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """
    Calculate Body Mass Index.

    Args:
        weight_kg: Weight in kilograms.
        height_m: Height in meters.

    Returns:
        BMI value as a float.
    """
    return weight_kg / (height_m ** 2)

if __name__ == "__main__":
    print(greet("Alice"))
    print(f"3^4 = {power(3, 4)}")
    print(f"5^2 = {power(5)}")
    flexible(1, 2, 3, name="Alice", age=30)
    configure(host="localhost", port=8080, debug=True)
    print(f"Distance: {distance(0, 0, 3, 4)}")
    q, r = divmod_custom(17, 5)
    print(f"17 / 5 = {q} remainder {r}")
    print(f"BMI: {calculate_bmi(70, 1.75):.1f}")
