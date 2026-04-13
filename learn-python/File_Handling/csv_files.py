"""
Working with CSV files in Python.
"""
import csv
import io
import tempfile
import os

tmp_dir = tempfile.mkdtemp()
csv_path = os.path.join(tmp_dir, "data.csv")

# Writing CSV
data = [
    ["Name", "Age", "City", "Salary"],
    ["Alice", 30, "New York", 85000],
    ["Bob", 25, "San Francisco", 92000],
    ["Charlie", 35, "Chicago", 78000],
    ["Diana", 28, "Boston", 95000],
]

with open(csv_path, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(data)
print("CSV written.")

# Reading CSV
with open(csv_path, 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)

# DictWriter and DictReader
dict_csv_path = os.path.join(tmp_dir, "employees.csv")
employees = [
    {"name": "Alice", "dept": "Engineering", "salary": 85000},
    {"name": "Bob", "dept": "Marketing", "salary": 72000},
    {"name": "Charlie", "dept": "Engineering", "salary": 90000},
]

with open(dict_csv_path, 'w', newline='') as f:
    fieldnames = ["name", "dept", "salary"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(employees)

print("\nDict CSV:")
with open(dict_csv_path, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"  {row['name']} in {row['dept']}: ${row['salary']}")

# CSV with different delimiters
tsv_path = os.path.join(tmp_dir, "data.tsv")
with open(tsv_path, 'w', newline='') as f:
    writer = csv.writer(f, delimiter='\t')
    writer.writerows(data)

# Handling quoting
quoted_path = os.path.join(tmp_dir, "quoted.csv")
with open(quoted_path, 'w', newline='') as f:
    writer = csv.writer(f, quoting=csv.QUOTE_ALL)
    writer.writerow(["Name", "Description"])
    writer.writerow(["Widget", 'A "special" item, very nice'])

with open(quoted_path, 'r') as f:
    print(f"\nQuoted CSV:\n{f.read()}")

# CSV from string (using io.StringIO)
csv_string = "name,age\nAlice,30\nBob,25"
reader = csv.DictReader(io.StringIO(csv_string))
for row in reader:
    print(f"  {row}")

# Cleanup
import shutil
shutil.rmtree(tmp_dir)
