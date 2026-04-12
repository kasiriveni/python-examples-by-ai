# Example: Dataclasses and NamedTuple
# Demonstrates how to use dataclasses and NamedTuple

from dataclasses import dataclass
from typing import NamedTuple

@dataclass
class DataClassExample:
    name: str
    age: int

class NamedTupleExample(NamedTuple):
    name: str
    age: int

# Using dataclass
data = DataClassExample(name="AI Engineer", age=30)
print(data)

# Using NamedTuple
tuple_data = NamedTupleExample(name="AI Engineer", age=30)
print(tuple_data)
