"""
For loops - comprehensive examples.
"""

# Basic for loop
for i in range(5):
    print(i, end=" ")
print()

# range() variations
print("range(2, 10, 2):", list(range(2, 10, 2)))
print("range(10, 0, -1):", list(range(10, 0, -1)))

# Iterating over strings
for char in "Python":
    print(char, end="-")
print()

# enumerate
fruits = ["apple", "banana", "cherry"]
for index, fruit in enumerate(fruits, start=1):
    print(f"{index}. {fruit}")

# zip
names = ["Alice", "Bob", "Charlie"]
scores = [95, 87, 92]
for name, score in zip(names, scores):
    print(f"{name}: {score}")

# zip_longest
from itertools import zip_longest
short = [1, 2]
long = [10, 20, 30, 40]
for a, b in zip_longest(short, long, fillvalue=0):
    print(f"  {a} + {b} = {a + b}")

# Nested loops
print("\nMultiplication table (1-5):")
for i in range(1, 6):
    for j in range(1, 6):
        print(f"{i*j:4}", end="")
    print()

# Loop with else (executes if loop completes without break)
print("\nSearching for 7 in [1,3,5,7,9]:")
for n in [1, 3, 5, 7, 9]:
    if n == 7:
        print("Found 7!")
        break
else:
    print("7 not found")

# Dictionary iteration
person = {"name": "Alice", "age": 30, "city": "NYC"}
for key, value in person.items():
    print(f"  {key}: {value}")

# List comprehension vs for loop
squares_loop = []
for x in range(10):
    squares_loop.append(x**2)

squares_comp = [x**2 for x in range(10)]
print(f"\nSquares: {squares_comp}")

# Unpacking in loops
pairs = [(1, 'a'), (2, 'b'), (3, 'c')]
for num, letter in pairs:
    print(f"  {num} -> {letter}")

# itertools examples
from itertools import product, combinations, permutations

print("\nProduct:", list(product("AB", "12")))
print("Combinations:", list(combinations("ABCD", 2)))
print("Permutations:", list(permutations("ABC", 2)))
