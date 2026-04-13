"""
Module 4: Data and Scientific Python - data manipulation patterns.
"""
import csv
import io
import json
import statistics
from collections import defaultdict
from itertools import groupby
from operator import itemgetter

# === CSV Processing ===
print("=== CSV Processing ===")

CSV_DATA = """date,product,quantity,price
2024-01-01,Widget,10,29.99
2024-01-01,Gadget,5,49.99
2024-01-02,Widget,15,29.99
2024-01-02,Gadget,8,49.99
2024-01-03,Widget,12,29.99
2024-01-03,Doohickey,20,9.99
"""

reader = csv.DictReader(io.StringIO(CSV_DATA))
sales = []
for row in reader:
    row['quantity'] = int(row['quantity'])
    row['price'] = float(row['price'])
    row['total'] = row['quantity'] * row['price']
    sales.append(row)

# Revenue by product
print("Revenue by product:")
sales_sorted = sorted(sales, key=itemgetter('product'))
for product, group in groupby(sales_sorted, key=itemgetter('product')):
    items = list(group)
    revenue = sum(i['total'] for i in items)
    qty = sum(i['quantity'] for i in items)
    print(f"  {product}: ${revenue:,.2f} ({qty} units)")

# === JSON Processing ===
print("\n=== JSON Processing ===")

data = {
    "users": [
        {"name": "Alice", "scores": [90, 85, 92]},
        {"name": "Bob", "scores": [78, 82, 88]},
        {"name": "Charlie", "scores": [95, 91, 97]},
    ]
}

json_str = json.dumps(data, indent=2)
parsed = json.loads(json_str)

for user in parsed["users"]:
    avg = statistics.mean(user["scores"])
    print(f"  {user['name']}: avg={avg:.1f}")

# === Statistical Analysis ===
print("\n=== Statistics ===")

data = [23, 45, 67, 12, 89, 34, 56, 78, 90, 11, 42, 65]
print(f"Mean: {statistics.mean(data):.1f}")
print(f"Median: {statistics.median(data):.1f}")
print(f"Mode: {statistics.mode([1,2,2,3,3,3,4])}")
print(f"Std Dev: {statistics.stdev(data):.1f}")
print(f"Variance: {statistics.variance(data):.1f}")

# Quantiles
quantiles = statistics.quantiles(data, n=4)
print(f"Quartiles: {[f'{q:.1f}' for q in quantiles]}")

# === Matrix Operations (pure Python) ===
print("\n=== Matrix Ops ===")

class Matrix:
    def __init__(self, data):
        self.data = data
        self.rows = len(data)
        self.cols = len(data[0])

    def __repr__(self):
        return '\n'.join(['  [' + ', '.join(f'{x:6.1f}' for x in row) + ']' for row in self.data])

    def __add__(self, other):
        return Matrix([[a + b for a, b in zip(r1, r2)]
                       for r1, r2 in zip(self.data, other.data)])

    def __mul__(self, other):
        result = [[sum(a * b for a, b in zip(row, col))
                    for col in zip(*other.data)]
                   for row in self.data]
        return Matrix(result)

    def transpose(self):
        return Matrix(list(map(list, zip(*self.data))))

A = Matrix([[1, 2], [3, 4]])
B = Matrix([[5, 6], [7, 8]])

print("A + B:")
print(A + B)
print("\nA * B:")
print(A * B)
print("\nA^T:")
print(A.transpose())

# === Data Pipeline ===
print("\n=== Data Pipeline ===")

def pipeline(*functions):
    def process(data):
        result = data
        for func in functions:
            result = func(result)
        return result
    return process

# Pipeline steps
def normalize(data):
    min_v, max_v = min(data), max(data)
    return [(x - min_v) / (max_v - min_v) for x in data]

def remove_outliers(data, threshold=2):
    mean = statistics.mean(data)
    std = statistics.stdev(data) if len(data) > 1 else 0
    return [x for x in data if abs(x - mean) <= threshold * std]

def round_values(data, decimals=3):
    return [round(x, decimals) for x in data]

process = pipeline(remove_outliers, normalize, round_values)
raw = [10, 12, 11, 100, 13, 9, 14, 11, 12]  # 100 is outlier
result = process(raw)
print(f"Raw: {raw}")
print(f"Processed: {result}")
