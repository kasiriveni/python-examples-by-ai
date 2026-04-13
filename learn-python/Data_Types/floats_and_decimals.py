"""
Float and Decimal types in Python.
"""
import math
from decimal import Decimal, getcontext

# Float basics
pi = 3.14159
scientific = 2.5e10
negative_exp = 1.5e-3
print(f"pi = {pi}, scientific = {scientific}, negative_exp = {negative_exp}")

# Floating point precision issues
print(f"0.1 + 0.2 = {0.1 + 0.2}")
print(f"0.1 + 0.2 == 0.3? {0.1 + 0.2 == 0.3}")
print(f"math.isclose(0.1 + 0.2, 0.3)? {math.isclose(0.1 + 0.2, 0.3)}")

# Special float values
print(f"float('inf') = {float('inf')}")
print(f"float('-inf') = {float('-inf')}")
print(f"float('nan') = {float('nan')}")
print(f"math.isinf(float('inf')) = {math.isinf(float('inf'))}")
print(f"math.isnan(float('nan')) = {math.isnan(float('nan'))}")

# Decimal for precise calculations
getcontext().prec = 50
d1 = Decimal('0.1')
d2 = Decimal('0.2')
print(f"Decimal('0.1') + Decimal('0.2') = {d1 + d2}")

# Rounding
print(f"round(3.5) = {round(3.5)}")   # Banker's rounding
print(f"round(4.5) = {round(4.5)}")
print(f"round(3.14159, 2) = {round(3.14159, 2)}")

# Float methods
x = 3.75
print(f"{x}.is_integer() = {x.is_integer()}")
print(f"(4.0).is_integer() = {(4.0).is_integer()}")
print(f"{x}.as_integer_ratio() = {x.as_integer_ratio()}")
