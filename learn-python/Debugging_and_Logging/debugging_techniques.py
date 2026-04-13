"""
Debugging techniques in Python.
"""
import traceback
import pdb
import sys
import logging

# === Print debugging ===
print("=== Print Debugging ===")

def calculate(data):
    total = 0
    for i, value in enumerate(data):
        total += value
        # Debug print (use f-string with variable names)
        print(f"  DEBUG: i={i}, value={value}, total={total}")
    return total

result = calculate([10, 20, 30])
print(f"Result: {result}")

# === Logging for debugging ===
print("\n=== Logging Debug ===")
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def process_items(items):
    logger.debug(f"Processing {len(items)} items")
    results = []
    for item in items:
        logger.debug(f"  Processing: {item}")
        results.append(item * 2)
    logger.info(f"Processed {len(results)} items successfully")
    return results

process_items([1, 2, 3])

# === Traceback inspection ===
print("\n=== Traceback ===")

def risky_function():
    return 1 / 0

try:
    risky_function()
except ZeroDivisionError:
    tb = traceback.format_exc()
    print(f"Traceback:\n{tb}")

# === Assert statements ===
print("=== Assertions ===")

def binary_search(arr, target):
    assert isinstance(arr, list), f"Expected list, got {type(arr)}"
    assert arr == sorted(arr), "Array must be sorted"

    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1

print(f"Search result: {binary_search([1, 3, 5, 7, 9], 5)}")

# === Inspecting objects ===
print("\n=== Object Inspection ===")

class MyClass:
    """A sample class."""
    class_var = 42

    def __init__(self, x):
        self.x = x

    def method(self):
        pass

obj = MyClass(10)
print(f"type: {type(obj)}")
print(f"dir: {[a for a in dir(obj) if not a.startswith('_')]}")
print(f"vars: {vars(obj)}")
print(f"isinstance: {isinstance(obj, MyClass)}")
print(f"hasattr 'x': {hasattr(obj, 'x')}")
print(f"id: {id(obj)}")

# === sys.getsizeof ===
print("\n=== Memory Usage ===")
items = [[], [1], list(range(100)), list(range(1000))]
for item in items:
    print(f"  list({len(item)} items): {sys.getsizeof(item)} bytes")

# === Breakpoint (pdb) ===
print("\n=== Breakpoint ===")
print("Use breakpoint() or pdb.set_trace() to start interactive debugging")
print("Commands: n(ext), s(tep), c(ontinue), p(rint), l(ist), q(uit)")
