# Decorators

def decorator_function(original_function):
    def wrapper_function(*args, **kwargs):
        print(f"Wrapper executed before {original_function.__name__}")
        return original_function(*args, **kwargs)
    return wrapper_function

@decorator_function
def display():
    print("Display function ran")

display()

# Function Decorator Example
def uppercase_decorator(func):
    def wrapper():
        result = func()
        return result.upper()
    return wrapper

@uppercase_decorator
def greet():
    return "hello world"

print(greet())

# Class Decorator Example
class AddPrefix:
    def __init__(self, prefix):
        self.prefix = prefix

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            return f"{self.prefix} {func(*args, **kwargs)}"
        return wrapper

@AddPrefix("Mr.")
def get_name():
    return "John Doe"

print(get_name())
