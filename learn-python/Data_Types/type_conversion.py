"""
Type conversion and casting in Python.
"""

# Implicit conversion (widening)
x = 5       # int
y = 2.5     # float
result = x + y
print(f"{x} + {y} = {result} (type: {type(result).__name__})")

# int() conversions
print(f"int(3.9) = {int(3.9)}")       # truncates
print(f"int('42') = {int('42')}")
print(f"int('0xff', 16) = {int('0xff', 16)}")
print(f"int(True) = {int(True)}")

# float() conversions
print(f"float('3.14') = {float('3.14')}")
print(f"float(42) = {float(42)}")
print(f"float('inf') = {float('inf')}")

# str() conversions
print(f"str(42) = '{str(42)}'")
print(f"str(3.14) = '{str(3.14)}'")
print(f"str([1,2,3]) = '{str([1,2,3])}'")

# bool() conversions (truthy/falsy)
falsy_values = [0, 0.0, "", [], {}, set(), None, False]
for val in falsy_values:
    print(f"bool({val!r}) = {bool(val)}")

# list(), tuple(), set() conversions
print(f"list('hello') = {list('hello')}")
print(f"tuple([1,2,3]) = {tuple([1,2,3])}")
print(f"set([1,1,2,2,3]) = {set([1,1,2,2,3])}")

# ord() and chr()
print(f"ord('A') = {ord('A')}")
print(f"chr(65) = {chr(65)}")

# Custom type conversion with __int__, __float__, __str__
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius

    def __int__(self):
        return int(self.celsius)

    def __float__(self):
        return float(self.celsius)

    def __str__(self):
        return f"{self.celsius}°C"

    def __bool__(self):
        return self.celsius != 0

t = Temperature(36.6)
print(f"int(t) = {int(t)}")
print(f"float(t) = {float(t)}")
print(f"str(t) = {str(t)}")
print(f"bool(t) = {bool(t)}")
