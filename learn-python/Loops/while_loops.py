"""
While loops - comprehensive examples.
"""

# Basic while loop
count = 0
while count < 5:
    print(f"Count: {count}")
    count += 1

# While with break
print("\nFinding first multiple of 7 > 50:")
n = 1
while True:
    if n % 7 == 0 and n > 50:
        print(f"Found: {n}")
        break
    n += 1

# While with continue
print("\nOdd numbers 1-10:")
n = 0
while n < 10:
    n += 1
    if n % 2 == 0:
        continue
    print(n, end=" ")
print()

# While with else
print("\nCountdown:")
n = 5
while n > 0:
    print(n, end=" ")
    n -= 1
else:
    print("Liftoff!")

# Sentinel value pattern
print("\nProcessing until sentinel:")
data = [10, 20, 30, -1, 40, 50]  # -1 is sentinel
i = 0
total = 0
while i < len(data) and data[i] != -1:
    total += data[i]
    i += 1
print(f"Sum before sentinel: {total}")

# Two-pointer technique
def is_palindrome(s):
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True

for word in ["racecar", "hello", "madam"]:
    print(f"  '{word}' palindrome: {is_palindrome(word)}")

# Exponential backoff simulation
import time
print("\nExponential backoff (simulated):")
attempt = 0
max_attempts = 5
delay = 1
while attempt < max_attempts:
    print(f"  Attempt {attempt + 1}, delay: {delay}s")
    delay *= 2
    attempt += 1

# Collatz conjecture
def collatz_steps(n):
    steps = 0
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        steps += 1
    return steps

for n in [6, 11, 27]:
    print(f"Collatz({n}): {collatz_steps(n)} steps")
