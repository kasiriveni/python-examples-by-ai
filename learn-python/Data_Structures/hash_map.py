"""
Data Structures: Hash Map implementation.
"""

class HashMap:
    """Hash map with chaining for collision resolution."""

    def __init__(self, capacity=16, load_factor=0.75):
        self.capacity = capacity
        self.load_factor = load_factor
        self.size = 0
        self.buckets = [[] for _ in range(capacity)]

    def _hash(self, key):
        return hash(key) % self.capacity

    def put(self, key, value):
        idx = self._hash(key)
        bucket = self.buckets[idx]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return

        bucket.append((key, value))
        self.size += 1

        if self.size / self.capacity > self.load_factor:
            self._resize()

    def get(self, key, default=None):
        idx = self._hash(key)
        for k, v in self.buckets[idx]:
            if k == key:
                return v
        return default

    def delete(self, key):
        idx = self._hash(key)
        bucket = self.buckets[idx]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self.size -= 1
                return True
        return False

    def __contains__(self, key):
        return self.get(key, sentinel := object()) is not sentinel

    def __len__(self):
        return self.size

    def _resize(self):
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0
        for bucket in old_buckets:
            for key, value in bucket:
                self.put(key, value)

    def keys(self):
        for bucket in self.buckets:
            for k, v in bucket:
                yield k

    def values(self):
        for bucket in self.buckets:
            for k, v in bucket:
                yield v

    def items(self):
        for bucket in self.buckets:
            for k, v in bucket:
                yield k, v

    def __repr__(self):
        items = [f"{k!r}: {v!r}" for k, v in self.items()]
        return "{" + ", ".join(items) + "}"

if __name__ == "__main__":
    print("=== Hash Map ===")
    hm = HashMap()

    # Insert
    data = {"name": "Alice", "age": 30, "city": "NYC", "email": "alice@test.com"}
    for k, v in data.items():
        hm.put(k, v)

    print(f"HashMap: {hm}")
    print(f"Size: {len(hm)}")
    print(f"Get 'name': {hm.get('name')}")
    print(f"Contains 'age': {'age' in hm}")
    print(f"Contains 'phone': {'phone' in hm}")

    # Update
    hm.put("age", 31)
    print(f"\nAfter update age: {hm.get('age')}")

    # Delete
    hm.delete("email")
    print(f"After delete email: {hm}")

    # Iteration
    print(f"\nKeys: {list(hm.keys())}")
    print(f"Values: {list(hm.values())}")

    # Stress test (triggers resize)
    print(f"\n=== Resize Test ===")
    hm2 = HashMap(capacity=4)
    for i in range(20):
        hm2.put(f"key_{i}", i)
    print(f"Inserted 20 items, capacity: {hm2.capacity}, size: {hm2.size}")
