# Example: Type Hints
# Demonstrates how to use type hints in Python
from typing import List, Optional

def greet(name: str, age: Optional[int] = None) -> str:
    if age:
        return f"Hello, {name}. You are {age} years old."
    return f"Hello, {name}."

def sum_numbers(numbers: List[int]) -> int:
    return sum(numbers)

print(greet("AI Engineer", 30))
print(sum_numbers([1, 2, 3, 4, 5]))
