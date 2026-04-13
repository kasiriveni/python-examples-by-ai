"""
Closures and scope in Python.
"""

# LEGB Rule: Local -> Enclosing -> Global -> Built-in
x = "global"

def outer():
    x = "enclosing"

    def inner():
        x = "local"
        print(f"inner: {x}")

    inner()
    print(f"outer: {x}")

outer()
print(f"module: {x}")

# Closures
def make_multiplier(factor):
    def multiply(n):
        return n * factor
    return multiply

double = make_multiplier(2)
triple = make_multiplier(3)
print(f"double(5) = {double(5)}")
print(f"triple(5) = {triple(5)}")

# nonlocal keyword
def counter():
    count = 0
    def increment():
        nonlocal count
        count += 1
        return count
    return increment

c = counter()
print(f"Count: {c()}, {c()}, {c()}")

# Closure for memoization
def memoize(func):
    cache = {}
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper

@memoize
def expensive_computation(n):
    print(f"  Computing {n}...")
    return n ** 2

print(f"Result: {expensive_computation(5)}")
print(f"Cached: {expensive_computation(5)}")

# Closure capturing loop variable (common pitfall)
# Wrong way
funcs_wrong = []
for i in range(3):
    funcs_wrong.append(lambda: i)
print(f"Wrong: {[f() for f in funcs_wrong]}")  # all return 2

# Right way
funcs_right = []
for i in range(3):
    funcs_right.append(lambda i=i: i)
print(f"Right: {[f() for f in funcs_right]}")
