# Core Python Concepts in Data Science Example

Source: [Data_Science_and_ML/data_processing.py](Data_Science_and_ML/data_processing.py#L1-L94)

- **CSV parsing:** using the `csv` module and `csv.DictReader` with `io.StringIO` to parse CSV text into dictionaries.
- **Type conversion:** converting string fields to integers (`int`) for numeric operations.
- **Lists & comprehensions:** building lists, filtering (e.g. senior employees), and creating derived lists (salaries, years).
- **Sorting & `operator.itemgetter`:** `sorted(..., key=itemgetter(...))` for ordering before slicing/grouping.
- **Grouping (`itertools.groupby`):** grouping sorted data by a key (department) to compute per-group aggregates.
- **`collections.defaultdict`:** nested `defaultdict` for building pivot-like structures without manual key checks.
- **Aggregation functions:** `sum`, `min`, `max`, and the `statistics` module (`mean`, `median`, `stdev`).
- **String formatting / f-strings:** readable numeric formatting (e.g. `f"${val:,.0f}"`) and interpolated output.
- **Conditional expressions:** inline `X if cond else Y` to set `seniority` labels.
- **Enumerate:** using `enumerate` when printing ordered results (top earners).
- **Functional tools & builtins:** `zip`, generator expressions, and `sum` for concise numeric computations.
- **Manual statistics (Pearson correlation):** implementing covariance/std calculations with generator expressions and basic math.
- **Lambda factory:** `defaultdict(lambda: defaultdict(list))` to create nested containers lazily.
- **Dictionary access & mutation:** reading and updating dict rows (e.g. `row['salary'] = int(...)`) to normalize data.
- **Readable, modular steps:** parsing → cleaning → aggregating → grouping → transforming → reporting — a common data-processing pipeline.

Notes / Best practices visible in the example:
- Sort before `groupby` to ensure groups are contiguous.
- Convert types early (normalize data) so later code assumes correct types.
- Use the `statistics` module for standard summary metrics when available.
- For larger data, replace in-memory lists with streaming or chunked processing.

If you want, I can expand each item with short code snippets or move this file into `Data_Science_and_ML/`.
