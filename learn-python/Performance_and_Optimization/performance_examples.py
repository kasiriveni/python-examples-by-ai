# Performance & Optimization: lru_cache, timeit
from functools import lru_cache
import time

@lru_cache(maxsize=None)
def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)

print(fib(20))

# simple timing
start = time.time()
for _ in range(10000):
    _ = 1+1
print('elapsed', time.time()-start)
