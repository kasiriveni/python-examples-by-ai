"""
Debugging and Logging: Using pdb and debugging strategies.
"""
import sys
import traceback
import warnings
from contextlib import contextmanager
import time

# === 1. Exception inspection ===
print("=== Exception Inspection ===")

def risky_function():
    data = {"key": "value"}
    return data["missing_key"]

try:
    risky_function()
except KeyError:
    exc_type, exc_value, exc_tb = sys.exc_info()
    print(f"Type: {exc_type.__name__}")
    print(f"Value: {exc_value}")
    print(f"Traceback:")
    traceback.print_tb(exc_tb)

# === 2. Custom traceback formatting ===
print("\n=== Custom Traceback ===")

def format_error(exc):
    tb_lines = traceback.format_exception(type(exc), exc, exc.__traceback__)
    return "".join(tb_lines)

try:
    1 / 0
except ZeroDivisionError as e:
    formatted = format_error(e)
    print(formatted[:200])

# === 3. Warnings ===
print("\n=== Warnings ===")

def deprecated_function():
    warnings.warn("This function is deprecated, use new_function() instead",
                  DeprecationWarning, stacklevel=2)
    return "old result"

# Capture warnings
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    deprecated_function()
    if w:
        print(f"Warning: {w[0].message}")
        print(f"Category: {w[0].category.__name__}")

# === 4. Debug context manager ===
print("\n=== Debug Timer ===")

@contextmanager
def debug_timer(label="Operation"):
    start = time.perf_counter()
    print(f"[DEBUG] Starting: {label}")
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        print(f"[DEBUG] {label} completed in {elapsed:.4f}s")

with debug_timer("List comprehension"):
    result = [x**2 for x in range(100_000)]

# === 5. Variable inspector ===
print("\n=== Variable Inspector ===")

def inspect_vars(**kwargs):
    for name, value in kwargs.items():
        print(f"  {name}: {type(value).__name__} = {repr(value)[:80]}")

x = [1, 2, 3]
y = {"key": "value"}
z = 42.5
inspect_vars(x=x, y=y, z=z)

# === 6. Assertion patterns ===
print("\n=== Assertions ===")

def divide(a, b):
    assert isinstance(a, (int, float)), f"Expected number, got {type(a)}"
    assert isinstance(b, (int, float)), f"Expected number, got {type(b)}"
    assert b != 0, "Division by zero"
    return a / b

print(f"divide(10, 3) = {divide(10, 3):.2f}")

try:
    divide(10, 0)
except AssertionError as e:
    print(f"Assertion: {e}")

# === 7. Debugging with print (structured) ===
print("\n=== Structured Debug Print ===")

class DebugLogger:
    def __init__(self, enabled=True):
        self.enabled = enabled
        self.indent = 0

    def enter(self, func_name):
        if self.enabled:
            print(f"{'  ' * self.indent}-> {func_name}")
            self.indent += 1

    def exit(self, func_name, result=None):
        if self.enabled:
            self.indent -= 1
            print(f"{'  ' * self.indent}<- {func_name} = {result}")

    def log(self, msg):
        if self.enabled:
            print(f"{'  ' * self.indent}   {msg}")

debug = DebugLogger()

def factorial(n):
    debug.enter(f"factorial({n})")
    if n <= 1:
        debug.exit(f"factorial({n})", 1)
        return 1
    result = n * factorial(n - 1)
    debug.exit(f"factorial({n})", result)
    return result

factorial(4)

# === 8. pdb reference ===
print("\n=== pdb Commands Reference ===")
PDB_COMMANDS = """
  breakpoint()     # Set breakpoint in code (Python 3.7+)
  import pdb; pdb.set_trace()  # Older way

  n (next)         # Execute next line
  s (step)         # Step into function
  c (continue)     # Continue to next breakpoint
  l (list)         # Show source code
  p expr           # Print expression
  pp expr          # Pretty-print expression
  w (where)        # Show call stack
  u/d (up/down)    # Move up/down call stack
  b N              # Set breakpoint at line N
  cl               # Clear breakpoints
  q (quit)         # Quit debugger
"""
print(PDB_COMMANDS)
