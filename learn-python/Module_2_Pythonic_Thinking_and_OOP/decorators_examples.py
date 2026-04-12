# Example: Decorators
# Demonstrates @property, @staticmethod, @classmethod, and custom decorators

class MyClass:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    @staticmethod
    def static_method():
        print("This is a static method.")

    @classmethod
    def class_method(cls):
        print("This is a class method.")

# Custom decorator
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Before the function call")
        result = func(*args, **kwargs)
        print("After the function call")
        return result
    return wrapper

@my_decorator
def say_hello():
    print("Hello, World!")

# Using the class
obj = MyClass(10)
print(obj.value)
MyClass.static_method()
MyClass.class_method()

# Using the custom decorator
say_hello()
