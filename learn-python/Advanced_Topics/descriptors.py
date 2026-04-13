"""
Descriptors in Python - controlling attribute access.
"""

# === Data descriptor ===
class Validated:
    def __init__(self, validator, error_msg="Invalid value"):
        self.validator = validator
        self.error_msg = error_msg
        self.attr_name = None

    def __set_name__(self, owner, name):
        self.attr_name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, f'_{self.attr_name}', None)

    def __set__(self, obj, value):
        if not self.validator(value):
            raise ValueError(f"{self.attr_name}: {self.error_msg} (got {value!r})")
        setattr(obj, f'_{self.attr_name}', value)

# === Using descriptors ===
class Product:
    name = Validated(lambda v: isinstance(v, str) and len(v) > 0, "must be non-empty string")
    price = Validated(lambda v: isinstance(v, (int, float)) and v >= 0, "must be non-negative number")
    quantity = Validated(lambda v: isinstance(v, int) and v >= 0, "must be non-negative integer")

    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def total_value(self):
        return self.price * self.quantity

    def __repr__(self):
        return f"Product({self.name!r}, ${self.price}, qty={self.quantity})"

# === Lazy property descriptor ===
class LazyProperty:
    def __init__(self, func):
        self.func = func
        self.attr_name = None

    def __set_name__(self, owner, name):
        self.attr_name = f'_lazy_{name}'

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if not hasattr(obj, self.attr_name):
            setattr(obj, self.attr_name, self.func(obj))
        return getattr(obj, self.attr_name)

class DataProcessor:
    def __init__(self, data):
        self.data = data

    @LazyProperty
    def sorted_data(self):
        print("  Computing sorted_data (expensive)...")
        return sorted(self.data)

    @LazyProperty
    def statistics(self):
        print("  Computing statistics (expensive)...")
        n = len(self.data)
        mean = sum(self.data) / n
        variance = sum((x - mean) ** 2 for x in self.data) / n
        return {"mean": mean, "variance": variance, "count": n}

if __name__ == "__main__":
    # Validated descriptor
    p = Product("Widget", 9.99, 100)
    print(f"Product: {p}")
    print(f"Total value: ${p.total_value():.2f}")

    try:
        p.price = -5
    except ValueError as e:
        print(f"Validation error: {e}")

    # Lazy property
    print("\n--- Lazy Property ---")
    dp = DataProcessor([5, 2, 8, 1, 9, 3])
    print("Accessing sorted_data twice:")
    print(f"  First: {dp.sorted_data}")
    print(f"  Second: {dp.sorted_data}")  # cached, no recomputation
    print(f"\nStats: {dp.statistics}")
