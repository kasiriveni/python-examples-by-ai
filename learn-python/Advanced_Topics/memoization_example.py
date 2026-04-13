"""
Example of using functools.lru_cache for memoization.
"""
from functools import lru_cache

@lru_cache(maxsize=32)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

if __name__ == "__main__":
    print(fibonacci(10))
