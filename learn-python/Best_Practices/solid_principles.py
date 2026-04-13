"""
Best Practices: Clean code, SOLID principles, code smells, and Pythonic idioms.
"""
from __future__ import annotations
import abc
import functools
import logging
from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable, Sequence

logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════
# 1. SOLID — Single Responsibility Principle
#    Each class has ONE reason to change
# ═══════════════════════════════════════════

# ❌ Violates SRP — does too many things
class BadUserService:
    def get_user(self, user_id: int) -> dict:
        return {"id": user_id}   # DB logic
    def format_user_email(self, user: dict) -> str:
        return f"<b>{user['id']}</b>"  # rendering logic
    def send_welcome_email(self, user: dict) -> None:
        pass   # email logic

# ✅ SRP applied
@dataclass
class User:
    id: int; name: str; email: str

class UserRepository:
    def get_by_id(self, user_id: int) -> User | None:
        # DB fetch goes here (stub)
        if user_id == 1:
            return User(1, "Alice", "alice@example.com")
        return None

class UserHTMLRenderer:
    def render(self, user: User) -> str:
        return f"<span>{user.name} &lt;{user.email}&gt;</span>"

class EmailService:
    def send_welcome(self, user: User) -> None:
        logger.info("Sending welcome email to %s", user.email)

# ═══════════════════════════════════════════
# 2. SOLID — Open/Closed Principle
#    Open for extension, closed for modification
# ═══════════════════════════════════════════
class DiscountStrategy(Protocol):
    def apply(self, price: float) -> float: ...

@dataclass
class NoDiscount:
    def apply(self, price: float) -> float: return price

@dataclass
class PercentageDiscount:
    percent: float  # 0-100
    def apply(self, price: float) -> float:
        return price * (1 - self.percent / 100)

@dataclass
class FixedDiscount:
    amount: float
    def apply(self, price: float) -> float:
        return max(0.0, price - self.amount)

@dataclass
class BuyNGetOneFreeDiscount:
    n: int = 1  # buy n, get 1 free
    def apply(self, price: float) -> float:
        # Applied per n+1 item set
        return price * self.n / (self.n + 1)

class Order:
    def __init__(self, items: list[tuple[str, float]],
                 discount: DiscountStrategy = NoDiscount()):
        self.items = items
        self.discount = discount

    def total(self) -> float:
        raw = sum(qty for _, qty in self.items)
        return self.discount.apply(raw)

# ═══════════════════════════════════════════
# 3. SOLID — Liskov Substitution Principle
#    Subclasses must honour the base contract
# ═══════════════════════════════════════════
class Rectangle2:
    def __init__(self, w: float, h: float):
        self._w = w; self._h = h
    @property
    def width(self)  -> float: return self._w
    @property
    def height(self) -> float: return self._h
    def area(self) -> float: return self._w * self._h
    def __repr__(self): return f"Rect({self._w}x{self._h})"

# ❌ Classic LSP violation: Square inherits Rectangle but changes behaviour
class BadSquare(Rectangle2):
    def __init__(self, side: float):
        super().__init__(side, side)
    # Setting width changes height — breaks the Rectangle contract

# ✅ Better: separate types sharing an interface
class Shape2D(abc.ABC):
    @abc.abstractmethod
    def area(self) -> float: ...

@dataclass
class SquareShape(Shape2D):
    side: float
    def area(self) -> float: return self.side ** 2

@dataclass
class RectangleShape(Shape2D):
    width: float; height: float
    def area(self) -> float: return self.width * self.height

# ═══════════════════════════════════════════
# 4. SOLID — Interface Segregation Principle
#    Many small interfaces > one fat interface
# ═══════════════════════════════════════════
class Readable(Protocol):
    def read(self, size: int = -1) -> bytes: ...

class Writable(Protocol):
    def write(self, data: bytes) -> int: ...

class Seekable(Protocol):
    def seek(self, pos: int) -> None: ...
    def tell(self) -> int: ...

# Clients depend only on what they need
def copy_data(src: Readable, dst: Writable, chunk: int = 4096) -> int:
    total = 0
    while data := src.read(chunk):
        dst.write(data); total += len(data)
    return total

# ═══════════════════════════════════════════
# 5. SOLID — Dependency Inversion Principle
#    Depend on abstractions, not concretions
# ═══════════════════════════════════════════
@runtime_checkable
class MessageBroker(Protocol):
    def publish(self, topic: str, message: str) -> None: ...
    def subscribe(self, topic: str) -> list[str]: ...  # simplification

class StdoutBroker:
    def publish(self, topic: str, message: str) -> None:
        print(f"[{topic}] {message}")
    def subscribe(self, topic: str) -> list[str]:
        return []

class InMemoryBroker:
    def __init__(self): self._store: dict[str, list[str]] = {}
    def publish(self, topic: str, message: str) -> None:
        self._store.setdefault(topic, []).append(message)
    def subscribe(self, topic: str) -> list[str]:
        return list(self._store.get(topic, []))

class NotificationService:
    """Depends on abstraction (MessageBroker), not a concrete class."""
    def __init__(self, broker: MessageBroker):
        self._broker = broker

    def notify_user(self, user: User, event: str) -> None:
        self._broker.publish(f"user.{user.id}", f"{event}: {user.name}")

# ═══════════════════════════════════════════
# 6. Pythonic idioms
# ═══════════════════════════════════════════
def pythonic_examples():
    print("=== Pythonic idioms ===")

    # ── EAFP vs LBYL ──
    data = {"key": 42}
    # LBYL (Look Before You Leap) — common in other languages
    if "key" in data:
        value = data["key"]

    # EAFP (Easier to Ask Forgiveness than Permission) — Pythonic
    try:
        value = data["missing"]
    except KeyError:
        value = None

    # ── Use get() with default ──
    val = data.get("missing", "default")

    # ── Unpacking ──
    first, *middle, last = [1, 2, 3, 4, 5]
    print(f"  first={first}, middle={middle}, last={last}")

    # ── enumerate + start offset ──
    for i, item in enumerate(["a", "b", "c"], start=10):
        pass

    # ── zip with strict (Python 3.10+) ──
    pairs = list(zip([1,2,3], ["a","b","c"], strict=True))
    print(f"  zip strict: {pairs}")

    # ── dict merge (Python 3.9+) ──
    defaults = {"debug": False, "log_level": "INFO", "timeout": 30}
    overrides = {"debug": True, "timeout": 10}
    config = defaults | overrides
    print(f"  dict merge: {config}")

    # ── Walrus operator ──
    numbers = [1, 7, 2, 9, 4, 10, 3]
    if (n := max(numbers)) > 8:
        print(f"  Max {n} exceeds threshold")

    # ── Conditional assignment ──
    raw_name = "  alice  "
    name = raw_name.strip().title() or "Anonymous"
    print(f"  name = {name!r}")

    # ── Avoid mutable default argument ──
    def bad(items=[]):     # ❌ shared across calls
        items.append(1); return items

    def good(items=None):  # ✅
        if items is None: items = []
        items.append(1); return items

# ═══════════════════════════════════════════
# 7. Common code smells and fixes
# ═══════════════════════════════════════════
def code_smells_demo():
    print("\n=== Code smells ===")

    # ── Long function → extract helpers ──
    # ── Magic numbers → named constants ──
    MAX_RETRIES = 3
    BASE_DELAY_SECS = 0.1
    HTTP_OK = 200

    # ── Excessive comments → self-documenting names ──
    # ❌ bad = x * 0.0175   # multiply by daily interest
    DAILY_INTEREST_RATE = 0.0175
    balance = 1000.0
    interest = balance * DAILY_INTEREST_RATE

    # ── Repeated code → DRY with a function ──
    templates = ["You have {count} message(s)", "You have {count} notification(s)"]
    counts    = [3, 0]
    def format_count(template: str, n: int) -> str:
        return template.format(count=n)
    results = [format_count(t, c) for t, c in zip(templates, counts)]
    print(f"  DRY: {results}")

    # ── Flag argument → two separate functions ──
    def get_users_active():   return []
    def get_users_inactive(): return []
    # instead of: get_users(is_active=True)

    # ── Return early (guard clauses) ──
    def process(order: dict | None) -> str:
        if order is None: return "no order"
        if not order.get("items"): return "empty order"
        if order.get("total", 0) < 0: return "invalid total"
        return f"processed: {len(order['items'])} items"

    for o in [None, {}, {"items": ["a"]}, {"items":["a"],"total":-1}, {"items":["a","b"],"total":50}]:
        print(f"  process({o!r}) → {process(o)!r}")

# ═══════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════
if __name__ == "__main__":
    print("=== SRP Demo ===")
    repo = UserRepository()
    user = repo.get_by_id(1)
    if user:
        html = UserHTMLRenderer().render(user)
        print(f"  HTML: {html}")
        EmailService().send_welcome(user)

    print("\n=== OCP Discount Demo ===")
    items = [("Widget", 30.0), ("Gadget", 50.0), ("Tool", 20.0)]
    for disc in [NoDiscount(), PercentageDiscount(10), FixedDiscount(5), BuyNGetOneFreeDiscount(2)]:
        order = Order(items, disc)
        print(f"  {type(disc).__name__}: ${order.total():.2f}")

    print("\n=== DIP Demo ===")
    broker = InMemoryBroker()
    svc = NotificationService(broker)
    if (u := UserRepository().get_by_id(1)):
        svc.notify_user(u, "login")
        svc.notify_user(u, "purchase")
    messages = broker.subscribe(f"user.1")
    print(f"  Captured {len(messages)} notifications: {messages}")

    pythonic_examples()
    code_smells_demo()
