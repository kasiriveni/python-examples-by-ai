# Example: Functions
import nt


def greet(name):
    return f"Hello, {name}!"

print(greet("Alice"))


# Example: Lambda Function
square = lambda x: x * x

print(square(5))

# Lambda Function Example
add = lambda x, y: x + y
print("Lambda Add:", add(5, 3))

# print inbuild function list
print(len("Hello, World!"))


# write fucntion with default parameter
def defaultgreet(name="Guest"):
    return f"Hello, {name}!"

print(defaultgreet())


# Example: Variable Scope
def outer_function():
    outer_var = "I am outside!"

    def inner_function():
        inner_var = "I am inside!"
        print(outer_var)  # Accessing outer variable
        print(inner_var)  # Accessing inner variable

    inner_function()

# print(inner_var)  # This will raise an error because inner_var is not accessible here


print(outer_function())


# Example: Recursive Function
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)

print("Factorial of 5:", factorial(5))

# function with variable number of arguments
def variable_args(*args):
    return f"Arguments: {args}"

print(variable_args(1, 2, 3, "Hello", [4, 5],7,88,99,100,101,102,103,104,105,106,107,108,109,110))


# Higher-Order Function Example
def apply_function(func, value):
    return func(value)

def square(x):
    return x * x

print("Square of 5:", apply_function(square, 5))

# Using map, filter, and reduce
from functools import reduce

numbers = [1, 2, 3, 4, 5]

# Map example
squared_numbers = list(map(lambda x: x ** 2, numbers))
print("Squared Numbers:", squared_numbers)

# Filter example
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print("Even Numbers:", even_numbers)

# Reduce example
sum_of_numbers = reduce(lambda x, y: x + y, numbers)
print("Sum of Numbers:", sum_of_numbers)
