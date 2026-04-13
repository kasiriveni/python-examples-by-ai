"""
Lists in Python - comprehensive examples.
"""

# Creating lists
empty = []
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True, None]
nested = [[1, 2], [3, 4], [5, 6]]

# List comprehensions
squares = [x**2 for x in range(10)]
evens = [x for x in range(20) if x % 2 == 0]
matrix_flat = [cell for row in nested for cell in row]
print(f"Squares: {squares}")
print(f"Evens: {evens}")
print(f"Flattened: {matrix_flat}")

# Slicing
data = list(range(10))
print(f"data[2:5] = {data[2:5]}")
print(f"data[::2] = {data[::2]}")
print(f"data[::-1] = {data[::-1]}")
print(f"data[-3:] = {data[-3:]}")

# List methods
fruits = ["apple", "banana", "cherry"]
fruits.append("date")
fruits.insert(1, "blueberry")
fruits.extend(["elderberry", "fig"])
print(f"After modifications: {fruits}")

removed = fruits.pop(2)
print(f"Popped: {removed}, List: {fruits}")

fruits.sort()
print(f"Sorted: {fruits}")

fruits.reverse()
print(f"Reversed: {fruits}")

# Copying lists (shallow vs deep)
import copy
original = [[1, 2], [3, 4]]
shallow = original.copy()
deep = copy.deepcopy(original)
original[0][0] = 99
print(f"Original: {original}")
print(f"Shallow copy: {shallow}")  # affected
print(f"Deep copy: {deep}")  # not affected

# Unpacking
first, *middle, last = [1, 2, 3, 4, 5]
print(f"first={first}, middle={middle}, last={last}")

# zip and enumerate
names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 35]
for i, (name, age) in enumerate(zip(names, ages)):
    print(f"{i}: {name} is {age} years old")
