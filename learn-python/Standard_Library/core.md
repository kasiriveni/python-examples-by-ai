# Core Python Concepts

## Core Themes
- Core utility modules from the Python standard library.
- Collections, itertools, functools, and math-related helpers.
- Operating-system, hashing, statistics, and date utilities.

## Core Theme Examples
- Example 1: os.path.exists() or sys.platform for environment checking.
- Example 2: Counter.most_common() and itertools.combinations() for data analysis.
- Example 3: hashlib.sha256() hash computation or datetime.now() timestamp.

## Files and Concepts
- collections_itertools_functools.py: Counter, defaultdict, deque, namedtuple, combinations, chains
- collections_tour.py: Counter methods, defaultdict nesting, OrderedDict, deque, namedtuple
- stdlib_comprehensive.py: os, sys, math, random, hashlib, textwrap, statistics
- stdlib_examples.py: basic os, sys, datetime, and math examples

## Core Example
This example uses common standard-library tools for counting and combinations.

```python
from collections import Counter
from itertools import combinations

words = ["python", "core", "python", "docs"]
counts = Counter(words)
print(counts["python"])

for pair in combinations([1, 2, 3], 2):
	print(pair)
```
