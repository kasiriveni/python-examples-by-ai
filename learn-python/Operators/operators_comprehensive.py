"""
Python operators - comprehensive examples.
"""

# Arithmetic operators
a, b = 17, 5
print("=== Arithmetic ===")
print(f"{a} + {b} = {a + b}")
print(f"{a} - {b} = {a - b}")
print(f"{a} * {b} = {a * b}")
print(f"{a} / {b} = {a / b}")       # true division
print(f"{a} // {b} = {a // b}")      # floor division
print(f"{a} % {b} = {a % b}")        # modulo
print(f"{a} ** {b} = {a ** b}")      # exponentiation

# Comparison operators
print("\n=== Comparison ===")
print(f"5 == 5: {5 == 5}")
print(f"5 != 3: {5 != 3}")
print(f"5 > 3: {5 > 3}")
print(f"5 < 3: {5 < 3}")
print(f"5 >= 5: {5 >= 5}")
print(f"5 <= 3: {5 <= 3}")

# Logical operators
print("\n=== Logical ===")
print(f"True and False: {True and False}")
print(f"True or False: {True or False}")
print(f"not True: {not True}")

# Short-circuit evaluation
print(f"0 and 'hello': {0 and 'hello'}")     # 0 (short-circuits)
print(f"1 and 'hello': {1 and 'hello'}")     # 'hello'
print(f"'' or 'default': {'' or 'default'}") # 'default'
print(f"'value' or 'default': {'value' or 'default'}") # 'value'

# Bitwise operators
print("\n=== Bitwise ===")
x, y = 0b1010, 0b1100  # 10, 12
print(f"{x} & {y} = {x & y} ({bin(x & y)})")    # AND
print(f"{x} | {y} = {x | y} ({bin(x | y)})")    # OR
print(f"{x} ^ {y} = {x ^ y} ({bin(x ^ y)})")    # XOR
print(f"~{x} = {~x}")                            # NOT
print(f"{x} << 2 = {x << 2}")                    # left shift
print(f"{x} >> 1 = {x >> 1}")                    # right shift

# Identity operators
print("\n=== Identity ===")
a = [1, 2, 3]
b = a
c = [1, 2, 3]
print(f"a is b: {a is b}")      # True (same object)
print(f"a is c: {a is c}")      # False (different object)
print(f"a == c: {a == c}")      # True (same value)
print(f"a is not c: {a is not c}")

# Membership operators
print("\n=== Membership ===")
fruits = ["apple", "banana", "cherry"]
print(f"'apple' in fruits: {'apple' in fruits}")
print(f"'grape' not in fruits: {'grape' not in fruits}")
print(f"'Py' in 'Python': {'Py' in 'Python'}")

# Walrus operator (:=)
print("\n=== Walrus ===")
numbers = [1, 2, 3, 4, 5]
if (total := sum(numbers)) > 10:
    print(f"Sum {total} is greater than 10")

# Assignment operators
print("\n=== Augmented Assignment ===")
x = 10
x += 5;  print(f"x += 5: {x}")
x -= 3;  print(f"x -= 3: {x}")
x *= 2;  print(f"x *= 2: {x}")
x //= 3; print(f"x //= 3: {x}")
x **= 2; print(f"x **= 2: {x}")
x %= 7;  print(f"x %= 7: {x}")
