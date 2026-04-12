# Example: Functions with *args and **kwargs
# Demonstrates how to use *args, **kwargs, and default values

def greet(name, greeting="Hello"):
    print(f"{greeting}, {name}!")

def print_args(*args):
    print("Positional arguments:", args)

def print_kwargs(**kwargs):
    print("Keyword arguments:", kwargs)

greet("AI Engineer")
greet("AI Engineer", "Hi")

print_args(1, 2, 3)
print_kwargs(a=1, b=2, c=3)
