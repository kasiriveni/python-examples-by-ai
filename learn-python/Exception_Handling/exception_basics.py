"""
Exception handling basics in Python.
"""

# Basic try/except
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"Caught: {e}")

# Multiple except blocks
def parse_data(value):
    try:
        return int(value)
    except ValueError:
        print(f"Cannot convert '{value}' to int")
    except TypeError:
        print(f"Invalid type: {type(value)}")
    return None

parse_data("abc")
parse_data(None)

# try/except/else/finally
def safe_divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("Cannot divide by zero")
        return None
    else:
        print(f"{a} / {b} = {result}")
        return result
    finally:
        print("Division operation complete")

safe_divide(10, 3)
safe_divide(10, 0)

# Catching multiple exceptions
try:
    data = {"key": [1, 2, 3]}
    print(data["missing"][5])
except (KeyError, IndexError) as e:
    print(f"Caught {type(e).__name__}: {e}")

# Re-raising exceptions
def process(value):
    try:
        return int(value)
    except ValueError:
        print(f"Logging: invalid value '{value}'")
        raise  # re-raise the same exception

try:
    process("abc")
except ValueError:
    print("Handled re-raised exception")

# Exception chaining
try:
    try:
        open("nonexistent.txt")
    except FileNotFoundError as e:
        raise RuntimeError("Failed to load config") from e
except RuntimeError as e:
    print(f"Error: {e}")
    print(f"Caused by: {e.__cause__}")

# Using exceptions for flow control (EAFP vs LBYL)
# EAFP: Easier to Ask Forgiveness than Permission
data = {"name": "Alice"}
try:
    age = data["age"]
except KeyError:
    age = "unknown"
print(f"Age: {age}")

# LBYL: Look Before You Leap
if "age" in data:
    age = data["age"]
else:
    age = "unknown"
