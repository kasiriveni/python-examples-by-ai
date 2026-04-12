# List, Dict, Set Comprehensions

# List comprehension
squares = [x ** 2 for x in range(5)]
print("Squares:", squares)

# Dict comprehension
square_dict = {x: x ** 2 for x in range(5)}
print("Square Dict:", square_dict)

# Set comprehension
square_set = {x ** 2 for x in range(5)}
print("Square Set:", square_set)
