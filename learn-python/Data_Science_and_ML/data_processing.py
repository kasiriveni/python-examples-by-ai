"""
Data Science: Pandas-like data processing with standard library.
"""
import csv
import io
import statistics
from collections import defaultdict
from itertools import groupby
from operator import itemgetter

# === Working with tabular data ===
CSV_DATA = """name,department,salary,years
Alice,Engineering,95000,5
Bob,Marketing,72000,3
Charlie,Engineering,88000,4
Diana,Sales,68000,2
Eve,Engineering,105000,7
Frank,Marketing,78000,5
Grace,Sales,71000,3
Henry,Engineering,92000,6
Ivy,Marketing,85000,4
Jack,Sales,75000,4
"""

# Parse CSV data
reader = csv.DictReader(io.StringIO(CSV_DATA))
employees = []
for row in reader:
    row['salary'] = int(row['salary'])
    row['years'] = int(row['years'])
    employees.append(row)

# === Aggregation ===
print("=== Basic Statistics ===")
salaries = [e['salary'] for e in employees]
print(f"Count: {len(salaries)}")
print(f"Mean salary: ${statistics.mean(salaries):,.0f}")
print(f"Median salary: ${statistics.median(salaries):,.0f}")
print(f"Std dev: ${statistics.stdev(salaries):,.0f}")
print(f"Min: ${min(salaries):,}, Max: ${max(salaries):,}")

# === Group by ===
print("\n=== Group By Department ===")
sorted_employees = sorted(employees, key=itemgetter('department'))
for dept, group in groupby(sorted_employees, key=itemgetter('department')):
    group_list = list(group)
    dept_salaries = [e['salary'] for e in group_list]
    print(f"\n{dept}:")
    print(f"  Count: {len(group_list)}")
    print(f"  Avg salary: ${statistics.mean(dept_salaries):,.0f}")
    print(f"  Total payroll: ${sum(dept_salaries):,}")

# === Filtering ===
print("\n=== Filtering ===")
senior = [e for e in employees if e['years'] >= 5]
print(f"Senior employees (5+ years): {[e['name'] for e in senior]}")

high_earners = [e for e in employees if e['salary'] >= 85000]
print(f"High earners (85K+): {[e['name'] for e in high_earners]}")

# === Sorting ===
print("\n=== Top Earners ===")
top_3 = sorted(employees, key=itemgetter('salary'), reverse=True)[:3]
for i, e in enumerate(top_3, 1):
    print(f"  {i}. {e['name']}: ${e['salary']:,} ({e['department']})")

# === Pivot table ===
print("\n=== Pivot: Avg Salary by Dept and Seniority ===")
for e in employees:
    e['seniority'] = 'Senior' if e['years'] >= 4 else 'Junior'

pivot = defaultdict(lambda: defaultdict(list))
for e in employees:
    pivot[e['department']][e['seniority']].append(e['salary'])

for dept in sorted(pivot.keys()):
    print(f"{dept}:")
    for level in ['Junior', 'Senior']:
        sals = pivot[dept].get(level, [])
        if sals:
            print(f"  {level}: ${statistics.mean(sals):,.0f} (n={len(sals)})")

# === Correlation ===
print("\n=== Correlation: Years vs Salary ===")
years = [e['years'] for e in employees]
n = len(years)
mean_x = sum(years) / n
mean_y = sum(salaries) / n
cov = sum((x - mean_x) * (y - mean_y) for x, y in zip(years, salaries)) / n
std_x = (sum((x - mean_x)**2 for x in years) / n) ** 0.5
std_y = (sum((y - mean_y)**2 for y in salaries) / n) ** 0.5
correlation = cov / (std_x * std_y)
print(f"Pearson correlation: {correlation:.3f}")
