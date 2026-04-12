# Example: Functools
# Demonstrates partial, lru_cache, and reduce

from functools import partial, lru_cache, reduce

# Partial

def multiply(x, y):
    return x * y

double = partial(multiply, 2)
print("Double of 5:", double(5))

# lru_cache
@lru_cache(maxsize=32)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print("Fibonacci(10):", fibonacci(10))

# Reduce
numbers = [1, 2, 3, 4]
result = reduce(lambda x, y: x + y, numbers)
print("Sum of numbers:", result)
