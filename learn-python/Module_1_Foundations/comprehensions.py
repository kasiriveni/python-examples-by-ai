# Example: List, Dict, and Set Comprehensions
# Demonstrates comprehensions with conditions

# List comprehension
squares = [x**2 for x in range(10) if x % 2 == 0]
print("Even squares:", squares)

# Dict comprehension
square_dict = {x: x**2 for x in range(5)}
print("Square dictionary:", square_dict)

# Set comprehension
unique_squares = {x**2 for x in [1, 2, 2, 3, 3, 3]}
print("Unique squares:", unique_squares)
