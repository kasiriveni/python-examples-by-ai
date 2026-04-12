# Example: Decorators
# Demonstrates how to use decorators in Python

def my_decorator(func):
    def wrapper():
        print("Before the function call")
        func()
        print("After the function call")
    return wrapper

@my_decorator
def say_hello():
    print("Hello, World!")

say_hello()
