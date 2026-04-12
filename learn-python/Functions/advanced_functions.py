# Functions: first-class, closures, decorators(with args), recursion, annotations
from functools import wraps

# Closure
def make_multiplier(n):
    def multiplier(x):
        return x * n
    return multiplier

double = make_multiplier(2)
print(double(5))

# Decorator with args
def repeat(times):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for _ in range(times):
                fn(*args, **kwargs)
        return wrapper
    return decorator

@repeat(2)
def say(msg: str) -> None:
    print(msg)

say("Hello")

# Recursion
def factorial(n: int) -> int:
    return 1 if n<=1 else n*factorial(n-1)

print(factorial(5))
