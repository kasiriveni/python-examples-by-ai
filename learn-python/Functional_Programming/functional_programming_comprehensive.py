"""
Functional programming in Python.
"""
from functools import reduce, partial, wraps
from itertools import chain, starmap, groupby, accumulate
from operator import add, mul, itemgetter

# Pure functions (no side effects)
def add_pure(a, b):
    return a + b

# Immutable data transformations
data = [1, 2, 3, 4, 5]
doubled = tuple(map(lambda x: x * 2, data))
print(f"Doubled: {doubled}")

# map with multiple iterables
a = [1, 2, 3]
b = [10, 20, 30]
sums = list(map(add, a, b))
print(f"Pairwise sums: {sums}")

# filter
numbers = range(1, 21)
primes = list(filter(lambda n: all(n % i != 0 for i in range(2, int(n**0.5)+1)) and n > 1, numbers))
print(f"Primes: {primes}")

# reduce
factorial = reduce(mul, range(1, 6))
print(f"5! = {factorial}")

# accumulate (running totals)
running_sum = list(accumulate([1, 2, 3, 4, 5]))
running_max = list(accumulate([3, 1, 4, 1, 5, 9, 2, 6], max))
print(f"Running sum: {running_sum}")
print(f"Running max: {running_max}")

# Function composition
def compose(*fns):
    def inner(x):
        for fn in reversed(fns):
            x = fn(x)
        return x
    return inner

pipeline = compose(str, lambda x: x * 2, lambda x: x + 10)
print(f"Pipeline(5): {pipeline(5)}")

# Partial application
def power(base, exp):
    return base ** exp

square = partial(power, exp=2)
cube = partial(power, exp=3)
print(f"square(5) = {square(5)}, cube(3) = {cube(3)}")

# Currying
def curry(func):
    @wraps(func)
    def curried(*args):
        if len(args) >= func.__code__.co_argcount:
            return func(*args)
        return lambda *more: curried(*args, *more)
    return curried

@curry
def multiply(a, b, c):
    return a * b * c

print(f"Curried: {multiply(2)(3)(4)}")
print(f"Partial: {multiply(2, 3)(4)}")

# groupby
from itertools import groupby
words = sorted(["apple", "ant", "banana", "bat", "cherry", "cat"], key=lambda w: w[0])
for letter, group in groupby(words, key=lambda w: w[0]):
    print(f"  {letter}: {list(group)}")

# chain
combined = list(chain([1, 2], [3, 4], [5, 6]))
print(f"\nChained: {combined}")

# Sorting with itemgetter/attrgetter
employees = [
    {"name": "Alice", "salary": 85000},
    {"name": "Bob", "salary": 72000},
    {"name": "Charlie", "salary": 90000},
]
by_salary = sorted(employees, key=itemgetter("salary"), reverse=True)
print(f"Top earner: {by_salary[0]['name']}")
