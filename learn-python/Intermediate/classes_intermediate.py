"""
Intermediate: Working with classes and OOP concepts.
"""
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime

# === Composition over inheritance ===
class Engine:
    def __init__(self, horsepower, fuel_type="gasoline"):
        self.horsepower = horsepower
        self.fuel_type = fuel_type
        self.running = False

    def start(self):
        self.running = True
        return f"Engine started ({self.horsepower}HP, {self.fuel_type})"

    def stop(self):
        self.running = False
        return "Engine stopped"

class GPS:
    def __init__(self):
        self.location = (0.0, 0.0)

    def get_location(self):
        return f"Location: {self.location}"

class Car:
    """Uses composition - has an engine and GPS."""
    def __init__(self, make, model, engine, gps=None):
        self.make = make
        self.model = model
        self.engine = engine
        self.gps = gps

    def start(self):
        return f"{self.make} {self.model}: {self.engine.start()}"

    def __repr__(self):
        return f"Car({self.make} {self.model}, {self.engine.horsepower}HP)"

# === Mixins ===
class JsonMixin:
    def to_json(self):
        import json
        return json.dumps(self.__dict__, default=str)

class TimestampMixin:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        original_init = cls.__init__
        def new_init(self, *args, **kwargs):
            original_init(self, *args, **kwargs)
            self.created_at = datetime.now()
        cls.__init__ = new_init

# === Property patterns ===
class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value

    @property
    def area(self):
        import math
        return math.pi * self._radius ** 2

    @property
    def circumference(self):
        import math
        return 2 * math.pi * self._radius

# === Builder pattern ===
@dataclass
class Query:
    table: str
    conditions: list = field(default_factory=list)
    columns: list = field(default_factory=lambda: ["*"])
    limit: Optional[int] = None
    order_by: Optional[str] = None

    def select(self, *columns):
        self.columns = list(columns)
        return self

    def where(self, condition):
        self.conditions.append(condition)
        return self

    def order(self, column):
        self.order_by = column
        return self

    def take(self, n):
        self.limit = n
        return self

    def build(self):
        sql = f"SELECT {', '.join(self.columns)} FROM {self.table}"
        if self.conditions:
            sql += f" WHERE {' AND '.join(self.conditions)}"
        if self.order_by:
            sql += f" ORDER BY {self.order_by}"
        if self.limit:
            sql += f" LIMIT {self.limit}"
        return sql

if __name__ == "__main__":
    # Composition
    car = Car("Tesla", "Model 3", Engine(450, "electric"))
    print(car.start())
    print(car)

    # Properties
    c = Circle(5)
    print(f"\nCircle(r={c.radius}): area={c.area:.2f}, circumference={c.circumference:.2f}")

    # Builder
    query = (Query("users")
             .select("name", "email")
             .where("age > 18")
             .where("active = true")
             .order("name")
             .take(10)
             .build())
    print(f"\nSQL: {query}")
