# Core Python Concepts

## Core Themes
- Numerical arrays and basic data processing.
- Aggregation and small-scale statistical analysis.
- Foundations for scientific Python workflows.

## Core Theme Examples
- Example 1: Creating and reshaping NumPy arrays.
- Example 2: Grouping rows and computing aggregations in Pandas.
- Example 3: Computing means and standard deviations on numerical data.

## Files and Concepts
- data_processing.py: CSV parsing, grouping, aggregation, summary statistics
- numpy_basics.py: NumPy arrays, reshaping, sums, means, array operations

## Core Example
This example computes summary statistics from a plain Python dataset.

```python
from statistics import mean

rows = [12, 15, 18, 21]
center = mean(rows)
shifted = [value - center for value in rows]

print(center)
print(shifted)
```
