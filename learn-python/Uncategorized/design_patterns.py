"""
Uncategorized: Design patterns in Python (creational, structural, behavioral).
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Callable, Iterator

# ═══════════════════════════════════════════
# CREATIONAL PATTERNS
# ═══════════════════════════════════════════

# 1. Singleton
class Singleton:
    """One instance per class."""
    _instance: "Singleton | None" = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

# 2. Factory Method
class Animal(ABC):
    @abstractmethod
    def speak(self) -> str: ...

class Dog(Animal): speak = lambda self: "Woof!"
class Cat(Animal): speak = lambda self: "Meow!"
class Duck(Animal): speak = lambda self: "Quack!"

def animal_factory(kind: str) -> Animal:
    registry = {"dog": Dog, "cat": Cat, "duck": Duck}
    cls = registry.get(kind.lower())
    if cls is None:
        raise ValueError(f"Unknown animal: {kind}")
    return cls()

# 3. Builder
@dataclass
class Pizza:
    size: str = "medium"
    crust: str = "thin"
    sauce: str = "tomato"
    toppings: list[str] = field(default_factory=list)

class PizzaBuilder:
    def __init__(self):       self._pizza = Pizza()
    def size(self, s):        self._pizza.size = s;       return self
    def crust(self, c):       self._pizza.crust = c;      return self
    def sauce(self, s):       self._pizza.sauce = s;      return self
    def topping(self, t):     self._pizza.toppings.append(t); return self
    def build(self) -> Pizza: return self._pizza

# 4. Prototype
import copy

class Prototype:
    def clone(self) -> "Prototype":
        return copy.deepcopy(self)

@dataclass
class Template(Prototype):
    title: str = ""
    sections: list[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)

# ═══════════════════════════════════════════
# STRUCTURAL PATTERNS
# ═══════════════════════════════════════════

# 5. Adapter
class EuropeanSocket:
    voltage = 230; hertz = 50

class USASocket:
    voltage = 120; hertz = 60

class EUtoUSAdapter:
    """Adapt EU socket to US interface."""
    def __init__(self, eu: EuropeanSocket): self._eu = eu
    @property
    def voltage(self): return 120           # transform
    @property
    def hertz(self):   return 60

# 6. Decorator (structural)
class TextProcessor:
    def process(self, text: str) -> str: return text

class UpperCaseDecorator:
    def __init__(self, proc): self._proc = proc
    def process(self, text): return self._proc.process(text).upper()

class TrimDecorator:
    def __init__(self, proc): self._proc = proc
    def process(self, text): return self._proc.process(text).strip()

class HTMLEscapeDecorator:
    def __init__(self, proc): self._proc = proc
    def process(self, text):
        import html
        return html.escape(self._proc.process(text))

# 7. Facade
class OrderFacade:
    """Simplified interface over OrderProcessor, InventorySystem, PaymentGateway."""
    def __init__(self):
        self._orders:    list[dict] = []
        self._inventory: dict[str, int] = {"pizza": 10, "burger": 5}
        self._revenue:   float = 0.0

    def place_order(self, item: str, qty: int, price: float) -> bool:
        if self._inventory.get(item, 0) < qty:
            print(f"  [Inventory] Not enough {item}")
            return False
        self._inventory[item] -= qty
        total = qty * price
        self._revenue += total
        self._orders.append({"item": item, "qty": qty, "total": total})
        print(f"  [Order] Placed: {qty}x {item} = ${total:.2f}")
        return True

    def report(self):
        print(f"  [Report] Orders: {len(self._orders)}, Revenue: ${self._revenue:.2f}")

# 8. Composite
class FileSystemNode(ABC):
    def __init__(self, name: str):
        self.name = name
    @abstractmethod
    def size(self) -> int: ...
    @abstractmethod
    def display(self, indent: int = 0) -> None: ...

class File(FileSystemNode):
    def __init__(self, name, size):
        super().__init__(name); self._size = size
    def size(self): return self._size
    def display(self, indent=0): print(" " * indent + f"📄 {self.name} ({self._size}B)")

class Directory(FileSystemNode):
    def __init__(self, name):
        super().__init__(name); self._children: list[FileSystemNode] = []
    def add(self, child): self._children.append(child); return self
    def size(self): return sum(c.size() for c in self._children)
    def display(self, indent=0):
        print(" " * indent + f"📁 {self.name}/ ({self.size()}B)")
        for c in self._children: c.display(indent + 4)

# ═══════════════════════════════════════════
# BEHAVIORAL PATTERNS
# ═══════════════════════════════════════════

# 9. Observer
class EventEmitter:
    def __init__(self):
        self._listeners: dict[str, list[Callable]] = {}

    def on(self, event: str, handler: Callable) -> None:
        self._listeners.setdefault(event, []).append(handler)

    def off(self, event: str, handler: Callable) -> None:
        self._listeners.get(event, []).remove(handler)

    def emit(self, event: str, *args, **kwargs) -> None:
        for h in self._listeners.get(event, []):
            h(*args, **kwargs)

# 10. Strategy
class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data: list) -> list: ...

class AscendingSort(SortStrategy):   sort = lambda self, d: sorted(d)
class DescendingSort(SortStrategy):  sort = lambda self, d: sorted(d, reverse=True)
class AbsoluteSort(SortStrategy):    sort = lambda self, d: sorted(d, key=abs)

class Sorter:
    def __init__(self, strategy: SortStrategy):
        self._strategy = strategy
    def set_strategy(self, s): self._strategy = s
    def sort(self, data): return self._strategy.sort(data)

# 11. Command
class Command(ABC):
    @abstractmethod
    def execute(self) -> None: ...
    @abstractmethod
    def undo(self) -> None: ...

class TextEditor:
    def __init__(self): self.text = ""
    def insert(self, text): self.text += text
    def delete(self, n): self.text = self.text[:-n] if n else self.text

class InsertCommand(Command):
    def __init__(self, editor, text):
        self._editor = editor; self._text = text
    def execute(self): self._editor.insert(self._text)
    def undo(self):    self._editor.delete(len(self._text))

class CommandHistory:
    def __init__(self): self._history: list[Command] = []
    def execute(self, cmd):
        cmd.execute(); self._history.append(cmd)
    def undo(self):
        if self._history: self._history.pop().undo()

# ─────────────────────────────────────────
if __name__ == "__main__":
    print("=== Singleton ===")
    a, b = Singleton(), Singleton()
    print(f"  a is b: {a is b}")

    print("\n=== Factory ===")
    for kind in ["dog", "cat", "duck"]:
        print(f"  {kind}: {animal_factory(kind).speak()}")

    print("\n=== Builder ===")
    pizza = (PizzaBuilder()
             .size("large").crust("thick").sauce("pesto")
             .topping("mushrooms").topping("olives").build())
    print(f"  {pizza}")

    print("\n=== Prototype ===")
    tmpl  = Template("Report", ["intro", "body"], {"author": "Alice"})
    clone = tmpl.clone()
    clone.title = "Clone"; clone.sections.append("conclusion")
    print(f"  Original: {tmpl}")
    print(f"  Clone:    {clone}")

    print("\n=== Adapter ===")
    eu = EuropeanSocket(); adapter = EUtoUSAdapter(eu)
    print(f"  EU: {eu.voltage}V {eu.hertz}Hz")
    print(f"  Adapted: {adapter.voltage}V {adapter.hertz}Hz")

    print("\n=== Decorator chain ===")
    proc = HTMLEscapeDecorator(TrimDecorator(UpperCaseDecorator(TextProcessor())))
    print(f"  {proc.process('  <hello world>  ')}")

    print("\n=== Composite (filesystem) ===")
    root = Directory("project")
    src  = Directory("src").add(File("main.py", 2048)).add(File("utils.py", 512))
    root.add(src).add(File("README.md", 1024)).add(File(".gitignore", 128))
    root.display()
    print(f"  Total size: {root.size()} bytes")

    print("\n=== Observer ===")
    emitter = EventEmitter()
    emitter.on("login", lambda user: print(f"  User logged in: {user}"))
    emitter.on("login", lambda user: print(f"  Send welcome email to: {user}"))
    emitter.emit("login", "alice@example.com")

    print("\n=== Strategy ===")
    data = [3, -1, 4, -1, 5, -9, 2, 6]
    sorter = Sorter(AscendingSort())
    print(f"  Ascending: {sorter.sort(data)}")
    sorter.set_strategy(AbsoluteSort())
    print(f"  Absolute:  {sorter.sort(data)}")

    print("\n=== Command + Undo ===")
    editor = TextEditor(); hist = CommandHistory()
    for word in ["Hello", ", ", "World", "!"]:
        hist.execute(InsertCommand(editor, word))
    print(f"  After 4 inserts: {editor.text!r}")
    hist.undo(); hist.undo()
    print(f"  After 2 undos:   {editor.text!r}")
