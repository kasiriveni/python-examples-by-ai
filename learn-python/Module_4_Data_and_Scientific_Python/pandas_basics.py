# Example: Pandas Basics
# Demonstrates basic operations with Pandas

import pandas as pd

# Create a DataFrame
data = {
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [25, 30, 35],
    "City": ["New York", "Los Angeles", "Chicago"]
}
df = pd.DataFrame(data)
print("DataFrame:")
print(df)

# Filter rows
filtered = df[df["Age"] > 28]
print("Filtered DataFrame:")
print(filtered)

# Add a new column
df["Salary"] = [70000, 80000, 90000]
print("Updated DataFrame:")
print(df)
