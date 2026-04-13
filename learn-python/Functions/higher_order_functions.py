"""
First-class functions and higher-order functions.
"""

# Functions are first-class objects
def square(x):
    return x ** 2

def cube(x):
    return x ** 3

# Passing functions as arguments
def apply(func, value):
    return func(value)

print(f"apply(square, 5) = {apply(square, 5)}")
print(f"apply(cube, 3) = {apply(cube, 3)}")

# Storing functions in data structures
operations = {
    "square": square,
    "cube": cube,
    "negate": lambda x: -x,
    "double": lambda x: x * 2,
}

for name, func in operations.items():
    print(f"{name}(4) = {func(4)}")

# Returning functions
def make_validator(min_val, max_val):
    def validate(value):
        return min_val <= value <= max_val
    return validate

is_valid_age = make_validator(0, 150)
is_valid_score = make_validator(0, 100)
print(f"\nAge 25 valid: {is_valid_age(25)}")
print(f"Score 150 valid: {is_valid_score(150)}")

# map, filter, reduce
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
squared = list(map(square, numbers))
evens = list(filter(lambda x: x % 2 == 0, numbers))

from functools import reduce
total = reduce(lambda a, b: a + b, numbers)

print(f"\nSquared: {squared}")
print(f"Evens: {evens}")
print(f"Sum: {total}")

# Function composition
def compose(*functions):
    def composed(x):
        for func in reversed(functions):
            x = func(x)
        return x
    return composed

add_one = lambda x: x + 1
double = lambda x: x * 2
add_one_then_double = compose(double, add_one)
print(f"\ncompose(double, add_one)(5) = {add_one_then_double(5)}")

# partial application
from functools import partial

def power(base, exponent):
    return base ** exponent

square = partial(power, exponent=2)
cube = partial(power, exponent=3)
print(f"square(5) = {square(5)}")
print(f"cube(3) = {cube(3)}")
