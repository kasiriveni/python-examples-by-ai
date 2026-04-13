"""
Uncategorized: Python one-liners, comprehension tricks, and idiomatic patterns.
"""

# ═══════════════════════════════════════════
# 1. Clever one-liners
# ═══════════════════════════════════════════
print("=== One-Liners ===")

# Flatten list
nested = [[1, 2, 3], [4, 5], [6, 7, 8, 9]]
flat = [x for row in nested for x in row]
print(f"Flatten: {flat}")

# Transpose matrix
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
transposed = list(map(list, zip(*matrix)))
print(f"Transpose: {transposed}")

# Deduplicate preserving order
seq = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
seen = set(); unique = [x for x in seq if not (x in seen or seen.add(x))]
print(f"Unique (ordered): {unique}")

# Most common element
from collections import Counter
most_common = Counter(seq).most_common(1)[0][0]
print(f"Most common: {most_common}")

# Chunk a list
lst = list(range(13))
chunk_size = 4
chunks = [lst[i:i+chunk_size] for i in range(0, len(lst), chunk_size)]
print(f"Chunks of 4: {chunks}")

# Rotate list
def rotate(lst, k):
    k %= len(lst)
    return lst[k:] + lst[:k]
print(f"Rotate [1..5] by 2: {rotate([1,2,3,4,5], 2)}")

# Merge dicts (Python 3.9+)
a, b = {"x": 1, "y": 2}, {"y": 3, "z": 4}
merged = a | b
print(f"Merged dicts: {merged}")

# ═══════════════════════════════════════════
# 2. Comprehension mastery
# ═══════════════════════════════════════════
print("\n=== Comprehension Patterns ===")

# Nested comprehension with condition
matrix = [[1,-2,3],[-4,5,-6],[7,-8,9]]
positive_only = [[x for x in row if x > 0] for row in matrix]
print(f"Only positives: {positive_only}")

# Dict comprehension from two lists
keys = ["a", "b", "c", "d"]
values = [1, 2, 3, 4]
zipped = {k: v for k, v in zip(keys, values)}
print(f"Zip to dict: {zipped}")

# Invert a dictionary
inverted = {v: k for k, v in zipped.items()}
print(f"Inverted:    {inverted}")

# Group by first letter
words = ["apple", "banana", "avocado", "blueberry", "cherry", "apricot"]
from collections import defaultdict
by_letter = defaultdict(list)
for w in words: by_letter[w[0]].append(w)
print(f"Grouped: {dict(by_letter)}")

# Set comprehension: unique lengths
lengths = {len(w) for w in words}
print(f"Unique lengths: {lengths}")

# Generator expression (memory-efficient)
import sys
lst_expr = [x**2 for x in range(10000)]
gen_expr = (x**2 for x in range(10000))
print(f"List size: {sys.getsizeof(lst_expr):,} bytes")
print(f"Gen size:  {sys.getsizeof(gen_expr)} bytes")

# ═══════════════════════════════════════════
# 3. Walrus operator (:=) PEP 572
# ═══════════════════════════════════════════
print("\n=== Walrus Operator ===")

# Filter long words and see their lengths
long_words = [
    (word, n)
    for word in ["python", "go", "javascript", "rust", "c"]
    if (n := len(word)) > 4
]
print(f"Words len>4: {long_words}")

# Read lines until empty (simulated)
lines = ["hello", "world", "", "!")
result = [line.upper() for line in lines if (s := line.strip())]
print(f"Non-empty upper: {result}")

# ═══════════════════════════════════════════
# 4. Structural pattern matching (Python 3.10+)
# ═══════════════════════════════════════════
print("\n=== Structural Pattern Matching ===")

def classify_command(command: dict) -> str:
    match command:
        case {"action": "move", "direction": direction, "steps": steps}:
            return f"Moving {direction} by {steps}"
        case {"action": "shoot", "target": target}:
            return f"Shooting at {target}"
        case {"action": "pickup", "item": item}:
            return f"Picking up {item}"
        case {"action": action}:
            return f"Unknown action: {action}"
        case _:
            return "Invalid command"

commands = [
    {"action": "move", "direction": "north", "steps": 3},
    {"action": "shoot", "target": "enemy"},
    {"action": "pickup", "item": "sword"},
    {"action": "dance"},
    {},
]
for cmd in commands:
    print(f"  {cmd} → {classify_command(cmd)}")

# ═══════════════════════════════════════════
# 5. Context variable tricks
# ═══════════════════════════════════════════
print("\n=== Assignment Tricks ===")

# Swap without temp
a, b = 3, 7
a, b = b, a
print(f"Swapped: a={a}, b={b}")

# Multiple assignment from function return
def divmod_custom(a, b): return a // b, a % b
quotient, remainder = divmod_custom(17, 5)
print(f"17 ÷ 5 = {quotient} rem {remainder}")

# Extended unpacking
first, *middle, last = [1, 2, 3, 4, 5]
print(f"first={first}, middle={middle}, last={last}")

# ═══════════════════════════════════════════
# 6. Useful builtins rarely used
# ═══════════════════════════════════════════
print("\n=== Under-used Builtins ===")

# zip_longest
from itertools import zip_longest
a, b = [1, 2, 3], ["x", "y"]
print(f"zip_longest: {list(zip_longest(a, b, fillvalue=0))}")

# accumulate with max (running maximum)
from itertools import accumulate
from operator import mul
data = [3, 1, 4, 1, 5, 9, 2, 6]
print(f"Running max: {list(accumulate(data, max))}")
print(f"Running mul: {list(accumulate(data, mul))}")

# vars() and __dict__
class Point:
    def __init__(self, x, y): self.x = x; self.y = y
p = Point(3, 4)
print(f"vars(p): {vars(p)}")

# object comparison with is vs ==
a, b = [1, 2, 3], [1, 2, 3]
print(f"a == b: {a == b}   a is b: {a is b}")
c = a
print(f"a is c: {a is c}  (same object)")

# divmod, powmod
print(f"divmod(17,5) = {divmod(17, 5)}")
print(f"pow(2, 10, 1000) = {pow(2, 10, 1000)}  (modular exp)")
