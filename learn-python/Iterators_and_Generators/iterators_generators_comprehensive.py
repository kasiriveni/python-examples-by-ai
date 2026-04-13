"""
Iterators and generators comprehensive examples.
"""

# === Custom Iterator ===
class Countdown:
    def __init__(self, start):
        self.start = start

    def __iter__(self):
        self.current = self.start
        return self

    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value

print("Countdown:")
for n in Countdown(5):
    print(f"  {n}")

# === Generator Functions ===
def fibonacci_gen():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

print("\nFirst 10 Fibonacci numbers:")
fib = fibonacci_gen()
for _ in range(10):
    print(f"  {next(fib)}")

# === Generator with send() ===
def accumulator():
    total = 0
    while True:
        value = yield total
        if value is None:
            break
        total += value

print("\nAccumulator:")
acc = accumulator()
next(acc)  # prime the generator
for val in [10, 20, 30, 40]:
    result = acc.send(val)
    print(f"  Sent {val}, total = {result}")

# === Generator expression vs list comprehension ===
import sys

list_comp = [x**2 for x in range(10000)]
gen_exp = (x**2 for x in range(10000))

print(f"\nList comp memory: {sys.getsizeof(list_comp)} bytes")
print(f"Generator memory: {sys.getsizeof(gen_exp)} bytes")

# === yield from (delegation) ===
def flatten(nested):
    for item in nested:
        if isinstance(item, (list, tuple)):
            yield from flatten(item)
        else:
            yield item

nested = [1, [2, 3, [4, 5]], [6, [7, 8, [9]]]]
print(f"\nFlattened: {list(flatten(nested))}")

# === Generator pipeline ===
def read_data():
    """Simulate reading data."""
    data = [
        "Alice,30,NYC",
        "Bob,25,LA",
        "Charlie,35,Chicago",
        "Diana,28,Boston",
    ]
    yield from data

def parse_records(lines):
    for line in lines:
        name, age, city = line.split(',')
        yield {"name": name, "age": int(age), "city": city}

def filter_by_age(records, min_age):
    for record in records:
        if record["age"] >= min_age:
            yield record

def format_output(records):
    for record in records:
        yield f"{record['name']} ({record['age']}) - {record['city']}"

# Pipeline
print("\nGenerator pipeline (age >= 28):")
pipeline = format_output(
    filter_by_age(
        parse_records(read_data()),
        min_age=28
    )
)
for item in pipeline:
    print(f"  {item}")

# === itertools ===
import itertools

# Chain
chained = itertools.chain([1, 2], [3, 4], [5, 6])
print(f"\nChained: {list(chained)}")

# Islice
print(f"Islice: {list(itertools.islice(range(100), 5, 15, 2))}")

# Groupby
data = sorted(["apple", "avocado", "banana", "blueberry", "cherry"], key=lambda x: x[0])
for key, group in itertools.groupby(data, key=lambda x: x[0]):
    print(f"  {key}: {list(group)}")

# Tee (duplicate iterator)
original = iter(range(5))
iter1, iter2 = itertools.tee(original)
print(f"\nTee 1: {list(iter1)}")
print(f"Tee 2: {list(iter2)}")
