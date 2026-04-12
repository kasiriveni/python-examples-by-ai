# Example: Type Hints and Typing Module
# Demonstrates Union, Optional, Literal, and TypeVar

from typing import Union, Optional, Literal, TypeVar

T = TypeVar("T")

def process_data(data: Union[int, str]) -> str:
    if isinstance(data, int):
        return f"Processed integer: {data}"
    return f"Processed string: {data}"

def greet(name: Optional[str] = None) -> str:
    if name:
        return f"Hello, {name}!"
    return "Hello, World!"

def direction_choice(direction: Literal["left", "right", "up", "down"]):
    print(f"You chose to go {direction}.")

print(process_data(10))
print(process_data("AI"))
print(greet())
print(greet("Engineer"))
direction_choice("left")
