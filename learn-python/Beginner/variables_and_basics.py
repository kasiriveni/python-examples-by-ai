"""
Beginner: Variables, input/output, and basic operations.
"""

# === Variables and data types ===
print("=== Variables ===")

name = "Alice"          # string
age = 25               # integer
height = 5.6           # float
is_student = True      # boolean
favorite_color = None  # NoneType

print(f"Name: {name} (type: {type(name).__name__})")
print(f"Age: {age} (type: {type(age).__name__})")
print(f"Height: {height} (type: {type(height).__name__})")
print(f"Student: {is_student} (type: {type(is_student).__name__})")
print(f"Color: {favorite_color} (type: {type(favorite_color).__name__})")

# === Multiple assignment ===
print("\n=== Multiple Assignment ===")
x, y, z = 1, 2, 3
print(f"x={x}, y={y}, z={z}")

# Swap
x, y = y, x
print(f"After swap: x={x}, y={y}")

# Same value
a = b = c = 0
print(f"a={a}, b={b}, c={c}")

# === String operations ===
print("\n=== Strings ===")
greeting = "Hello, World!"
print(f"Upper: {greeting.upper()}")
print(f"Lower: {greeting.lower()}")
print(f"Length: {len(greeting)}")
print(f"Slice [0:5]: {greeting[0:5]}")
print(f"Replace: {greeting.replace('World', 'Python')}")
print(f"Split: {greeting.split(', ')}")
print(f"Strip: {'  hello  '.strip()}")
print(f"Starts with 'Hello': {greeting.startswith('Hello')}")
print(f"Count 'l': {greeting.count('l')}")

# === String formatting ===
print("\n=== String Formatting ===")
item = "coffee"
price = 4.99
quantity = 3

# f-strings (recommended)
print(f"You ordered {quantity} {item}(s) at ${price:.2f} each")
print(f"Total: ${price * quantity:.2f}")

# Alignment
print(f"{'Item':<15}{'Price':>10}")
print(f"{item:<15}${price:>9.2f}")

# === Basic arithmetic ===
print("\n=== Arithmetic ===")
a, b = 17, 5
print(f"{a} + {b} = {a + b}")
print(f"{a} - {b} = {a - b}")
print(f"{a} * {b} = {a * b}")
print(f"{a} / {b} = {a / b}")       # float division
print(f"{a} // {b} = {a // b}")      # integer division
print(f"{a} % {b} = {a % b}")        # modulus
print(f"{a} ** {b} = {a ** b}")      # exponent

# === Type conversion ===
print("\n=== Type Conversion ===")
num_str = "42"
num_int = int(num_str)
num_float = float(num_str)
back_to_str = str(num_int)
print(f"String '42' -> int: {num_int}")
print(f"String '42' -> float: {num_float}")
print(f"int 42 -> str: '{back_to_str}' (type: {type(back_to_str).__name__})")

# === Boolean operations ===
print("\n=== Boolean ===")
print(f"True and False = {True and False}")
print(f"True or False = {True or False}")
print(f"not True = {not True}")
print(f"5 > 3 = {5 > 3}")
print(f"5 == 5 = {5 == 5}")
print(f"5 != 3 = {5 != 3}")
