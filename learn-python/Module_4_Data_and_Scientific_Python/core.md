# Core Python Concepts

## Core Themes
- NumPy, Pandas, and Matplotlib fundamentals.
- Data cleaning, grouping, and tabular transformations.
- Scientific computing and visualization basics.

## Core Theme Examples
- Example 1: Filtering DataFrames and computing column averages.
- Example 2: Creating line and scatter plots with Matplotlib.
- Example 3: Array operations and statistical computation with NumPy.

## Files and Concepts
- data_manipulation.py: CSV workflows, groupby operations, itertools, revenue analysis
- matplotlib_basics.py: line plots, scatter plots, labels, legends
- numpy_basics.py: array math, sums, means, standard deviation
- pandas_basics.py: DataFrame creation, filtering, column operations

## Core Example
This example mirrors filtering and aggregation with plain dictionaries and lists.

```python
records = [
	{"name": "Alice", "score": 90},
	{"name": "Bob", "score": 80},
]

high_scores = [record for record in records if record["score"] >= 85]
average = sum(record["score"] for record in records) / len(records)

print(high_scores)
print(average)
```
