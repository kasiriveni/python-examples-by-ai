# Example: Dunder/Magic Methods
# Demonstrates __repr__, __str__, and __call__

class MyClass:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"MyClass(value={self.value})"

    def __str__(self):
        return f"Value: {self.value}"

    def __call__(self):
        print(f"Called with value: {self.value}")

obj = MyClass(10)
print(repr(obj))
print(str(obj))
obj()
