"""
Module 1: Python Foundations - core language features.
"""

# === Data types deep dive ===
print("=== Data Types ===")

# Numeric
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction

# Floating point precision
print(f"0.1 + 0.2 = {0.1 + 0.2}")
print(f"Decimal: {Decimal('0.1') + Decimal('0.2')}")
print(f"Fraction: {Fraction(1, 3) + Fraction(1, 6)}")

# Rounding
price = Decimal("19.995")
print(f"Rounded: {price.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)}")

# === Collections in depth ===
print("\n=== Collections ===")
from collections import OrderedDict, defaultdict, deque, ChainMap

# defaultdict
word_count = defaultdict(int)
for word in "the cat sat on the mat the cat".split():
    word_count[word] += 1
print(f"Word count: {dict(word_count)}")

# deque (double-ended queue)
dq = deque([1, 2, 3], maxlen=5)
dq.appendleft(0)
dq.append(4)
dq.append(5)
print(f"Deque: {dq}")

# ChainMap (layered configuration)
defaults = {"theme": "dark", "lang": "en", "debug": False}
user_prefs = {"theme": "light"}
config = ChainMap(user_prefs, defaults)
print(f"Config theme: {config['theme']}")
print(f"Config lang: {config['lang']}")

# === String processing ===
print("\n=== String Processing ===")

# Template strings
from string import Template
t = Template("Hello, $name! You have $count messages.")
print(t.substitute(name="Alice", count=5))

# Regular expressions
import re
text = "Contact us at support@example.com or sales@company.org"
emails = re.findall(r'[\w.+-]+@[\w-]+\.[\w.]+', text)
print(f"Found emails: {emails}")

# String methods chain
data = "  Hello, World!  "
result = data.strip().lower().replace("world", "python").title()
print(f"Processed: {result}")

# === Unpacking and assignment ===
print("\n=== Advanced Assignment ===")

# Extended unpacking
first, *middle, last = range(10)
print(f"First: {first}, Middle: {middle}, Last: {last}")

# Dictionary merging
a = {"x": 1, "y": 2}
b = {"y": 3, "z": 4}
merged = {**a, **b}  # Python 3.5+
merged2 = a | b      # Python 3.9+
print(f"Merged: {merged}")

# Walrus operator
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
if (n := len(data)) > 5:
    print(f"Long list with {n} elements")

# === Itertools essentials ===
print("\n=== Itertools ===")
import itertools

# Product (cartesian product)
colors = ['red', 'blue']
sizes = ['S', 'M', 'L']
combos = list(itertools.product(colors, sizes))
print(f"Product: {combos[:4]}...")

# Chain (flatten)
lists = [[1, 2], [3, 4], [5, 6]]
flat = list(itertools.chain.from_iterable(lists))
print(f"Chained: {flat}")

# Groupby
data = [("fruit", "apple"), ("veggie", "carrot"), ("fruit", "banana"), ("veggie", "pea")]
data.sort(key=lambda x: x[0])
for key, group in itertools.groupby(data, key=lambda x: x[0]):
    print(f"  {key}: {[item[1] for item in group]}")
