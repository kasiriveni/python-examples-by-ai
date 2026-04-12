# Example: Variables and Data Types
# Demonstrates type conversion and dynamic typing

# Dynamic typing
x = 10
print(f"x is {x} and its type is {type(x)}")
x = "Hello"
print(f"x is now {x} and its type is {type(x)}")

# Type conversion
num_str = "123"
num = int(num_str)
print(f"Converted {num_str} to {num} (type: {type(num)})")

float_num = float(num)
print(f"Converted {num} to {float_num} (type: {type(float_num)})")
