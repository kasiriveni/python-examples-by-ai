"""
Type hints and annotations in Python.
"""
from typing import (
    List, Dict, Tuple, Set, Optional, Union,
    Callable, Iterator, Generator, Any,
    TypeVar, Generic, Protocol, Literal,
    NamedTuple, TypedDict
)

# Basic type hints
def greet(name: str) -> str:
    return f"Hello, {name}!"

def add(a: int, b: int) -> int:
    return a + b

# Optional (can be None)
def find_user(user_id: int) -> Optional[str]:
    users = {1: "Alice", 2: "Bob"}
    return users.get(user_id)

# Union types
def process(value: Union[int, str]) -> str:
    return str(value)

# Python 3.10+ union syntax
def process_new(value: int | str) -> str:
    return str(value)

# Collection types
def sum_list(numbers: list[int]) -> int:
    return sum(numbers)

def word_count(text: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for word in text.split():
        counts[word] = counts.get(word, 0) + 1
    return counts

# Callable type
def apply(func: Callable[[int, int], int], a: int, b: int) -> int:
    return func(a, b)

# TypeVar for generics
T = TypeVar('T')

def first(items: list[T]) -> T:
    return items[0]

# Generic class
class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()

# Protocol (structural subtyping)
class Drawable(Protocol):
    def draw(self) -> None: ...

class Circle:
    def draw(self) -> None:
        print("Drawing circle")

def render(shape: Drawable) -> None:
    shape.draw()

# TypedDict
class MovieDict(TypedDict):
    title: str
    year: int
    rating: float

movie: MovieDict = {"title": "Inception", "year": 2010, "rating": 8.8}

# Literal types
def set_mode(mode: Literal["read", "write", "append"]) -> None:
    print(f"Mode set to: {mode}")

# NamedTuple with types
class Coordinate(NamedTuple):
    lat: float
    lon: float
    alt: float = 0.0

coord = Coordinate(40.7128, -74.0060)
print(f"Coordinate: {coord}")

if __name__ == "__main__":
    print(greet("World"))
    print(find_user(1))
    render(Circle())
    set_mode("read")
