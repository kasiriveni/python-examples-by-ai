# Type Casting & Exceptions
# This script demonstrates type casting and exception handling.

# Type Casting
num_str = "123"
num = int(num_str)
print("Converted to integer:", num)

# Exception Handling
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero!")
