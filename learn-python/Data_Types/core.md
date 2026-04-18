# Core Python Concepts

## Core Themes
- Python scalar and collection types in depth.
- Type conversion, formatting, and annotations.
- Specialized types such as datetime, Enum, bytes, and dataclasses.

## Core Theme Examples
- Example 1: Scalar types (int, float, str) combined in collection.
- Example 2: f-string formatting with type-cast conversion.
- Example 3: datetime object creation and Enum definition.

## Files and Concepts
- booleans.py: boolean values, truthiness
- bytes_and_bytearray.py: binary data, encoding and decoding, memoryview, struct packing
- complex_numbers.py: complex arithmetic, polar coordinates, cmath
- dataclasses_example.py: dataclass decorator, fields, frozen dataclasses, type hints
- dates_and_times.py: datetime, date, time, timedelta, timezone formatting
- deep_dive.py: type hints, Enum, dataclass, mutable and immutable behavior
- dictionaries.py: dictionary creation, access, comprehensions, merging, iteration
- enums.py: Enum basics, auto values, IntEnum, Flag enums
- floats_and_decimals.py: float precision, Decimal type, special float values
- integers.py: integer literals, bit operations, base conversions
- lists.py: list creation, slicing, comprehensions, copy behavior
- none_type.py: None semantics, None checks
- numbers.py: numeric types, built-in math helpers, conversions
- regex_with_strings.py: regular expressions, capturing groups, substitution, lookarounds
- sets_and_frozensets.py: set operations, frozensets, hashable set usage
- strings.py: string methods, string operations
- string_formatting.py: f-strings, format method, percent formatting, Template strings
- tuples.py: tuple creation, unpacking, named tuples, tuple keys
- type_conversion.py: casting with int, float, str, bool, list, tuple, set
- type_hints.py: type annotations, Optional, Union, Callable, Generic, Protocol

## Core Example
This example mixes scalar values with common collection types and conversions.

```python
age = 25
price = 19.5
name = "Alice"
tags = {"python", "basics"}
record = {"name": name, "age": str(age)}

values = [age, int(price), len(tags)]
print(record)
print(tuple(values))
```
