"""
Basics: Control flow - if/else, loops, and match.
"""

# === If / Elif / Else ===
print("=== Conditionals ===")

score = 85

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"
print(f"Score {score} -> Grade {grade}")

# Ternary
status = "pass" if score >= 60 else "fail"
print(f"Status: {status}")

# Truthiness
values = [0, "", None, [], False, 1, "hello", [1], True]
for v in values:
    print(f"  {str(v):10s} -> {'Truthy' if v else 'Falsy'}")

# === For Loops ===
print("\n=== For Loops ===")

# Range
for i in range(5):
    print(f"  i = {i}", end="  ")
print()

# Enumerate
fruits = ["apple", "banana", "cherry"]
for idx, fruit in enumerate(fruits, 1):
    print(f"  {idx}. {fruit}")

# Zip
names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 35]
for name, age in zip(names, ages):
    print(f"  {name} is {age}")

# === While Loops ===
print("\n=== While Loops ===")

count = 5
while count > 0:
    print(f"  Countdown: {count}")
    count -= 1
print("  Liftoff!")

# === Break, Continue, Else ===
print("\n=== Break & Continue ===")

# Find first even
numbers = [1, 3, 5, 4, 7, 2]
for n in numbers:
    if n % 2 == 0:
        print(f"First even: {n}")
        break

# Skip negatives
data = [1, -2, 3, -4, 5]
positives = []
for n in data:
    if n < 0:
        continue
    positives.append(n)
print(f"Positives: {positives}")

# For-else: runs when loop completes without break
print("\nSearching for prime:")
for n in [4, 6, 7, 9]:
    for d in range(2, n):
        if n % d == 0:
            print(f"  {n} is NOT prime (divisible by {d})")
            break
    else:
        print(f"  {n} IS prime")

# === Nested loops ===
print("\n=== Multiplication Table (1-5) ===")
for i in range(1, 6):
    row = ""
    for j in range(1, 6):
        row += f"{i*j:4d}"
    print(row)

# === Match Statement (Python 3.10+) ===
print("\n=== Pattern Matching ===")

def handle_command(command):
    match command.split():
        case ["quit"]:
            return "Quitting..."
        case ["hello", name]:
            return f"Hello, {name}!"
        case ["add", *numbers]:
            return f"Sum: {sum(int(n) for n in numbers)}"
        case _:
            return f"Unknown command: {command}"

commands = ["quit", "hello World", "add 1 2 3", "unknown"]
for cmd in commands:
    print(f"  '{cmd}' -> {handle_command(cmd)}")
