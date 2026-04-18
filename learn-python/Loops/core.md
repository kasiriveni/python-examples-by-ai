# Core Python Concepts

## Core Themes
- For loops, while loops, and iteration control.
- Enumerate, zip, comprehensions, and loop utilities.
- Loop else blocks, sentinels, and nested iteration patterns.

## Core Theme Examples
- Example 1: For loop with range() and break statement.
- Example 2: Zip pairing sequences with enumerate indexing.
- Example 3: List comprehension filtering with conditional.

## Files and Concepts
- advanced_loops.py: list, dict, set, and generator comprehensions, enumerate, zip, itertools recipes
- for_loops.py: range usage, string iteration, enumerate, zip, nested loops, loop else
- iteration_examples.py: enumerate unpacking, zip pairing, loop else, break, continue, pass
- while_loops.py: while loops, break and continue, while else, sentinel loops, two-pointer patterns

## Core Example
This example uses enumerate, zip, and a comprehension to process sequences.

```python
names = ["Alice", "Bob", "Cara"]
scores = [90, 85, 95]

for index, (name, score) in enumerate(zip(names, scores), start=1):
	print(index, name, score)

passed = [score for score in scores if score >= 90]
print(passed)
```
