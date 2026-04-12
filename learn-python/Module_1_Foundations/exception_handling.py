# Example: Exception Handling
# Demonstrates try/except/finally and custom exceptions

# Try/except/finally
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print("Caught an exception:", e)
finally:
    print("This block always executes.")

# Custom exception
class CustomError(Exception):
    pass

try:
    raise CustomError("This is a custom error.")
except CustomError as e:
    print("Caught a custom exception:", e)
