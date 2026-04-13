"""
Serialization: Protocol Buffers, MessagePack, and YAML patterns.
"""
import json
import pickle
import struct
from dataclasses import dataclass, asdict, field
from typing import Any

# === Custom binary serialization ===
print("=== Custom Binary Format ===")

class BinarySerializer:
    """Simple binary serializer for fixed schemas."""

    TYPE_INT = 0x01
    TYPE_FLOAT = 0x02
    TYPE_STRING = 0x03
    TYPE_BOOL = 0x04
    TYPE_LIST = 0x05

    def serialize(self, data):
        buffer = bytearray()
        self._encode(buffer, data)
        return bytes(buffer)

    def _encode(self, buffer, value):
        if isinstance(value, bool):
            buffer.append(self.TYPE_BOOL)
            buffer.append(1 if value else 0)
        elif isinstance(value, int):
            buffer.append(self.TYPE_INT)
            buffer.extend(struct.pack('>q', value))
        elif isinstance(value, float):
            buffer.append(self.TYPE_FLOAT)
            buffer.extend(struct.pack('>d', value))
        elif isinstance(value, str):
            buffer.append(self.TYPE_STRING)
            encoded = value.encode('utf-8')
            buffer.extend(struct.pack('>I', len(encoded)))
            buffer.extend(encoded)
        elif isinstance(value, list):
            buffer.append(self.TYPE_LIST)
            buffer.extend(struct.pack('>I', len(value)))
            for item in value:
                self._encode(buffer, item)

    def deserialize(self, data):
        return self._decode(data, [0])

    def _decode(self, data, pos):
        type_byte = data[pos[0]]
        pos[0] += 1

        if type_byte == self.TYPE_BOOL:
            val = bool(data[pos[0]])
            pos[0] += 1
            return val
        elif type_byte == self.TYPE_INT:
            val = struct.unpack('>q', data[pos[0]:pos[0]+8])[0]
            pos[0] += 8
            return val
        elif type_byte == self.TYPE_FLOAT:
            val = struct.unpack('>d', data[pos[0]:pos[0]+8])[0]
            pos[0] += 8
            return val
        elif type_byte == self.TYPE_STRING:
            length = struct.unpack('>I', data[pos[0]:pos[0]+4])[0]
            pos[0] += 4
            val = data[pos[0]:pos[0]+length].decode('utf-8')
            pos[0] += length
            return val
        elif type_byte == self.TYPE_LIST:
            length = struct.unpack('>I', data[pos[0]:pos[0]+4])[0]
            pos[0] += 4
            return [self._decode(data, pos) for _ in range(length)]

bs = BinarySerializer()
for value in [42, 3.14, "hello", True, [1, 2, 3]]:
    encoded = bs.serialize(value)
    decoded = bs.deserialize(encoded)
    print(f"  {value!r:20s} -> {len(encoded)} bytes -> {decoded!r}")

# === Dataclass serialization ===
print("\n=== Dataclass Serialization ===")

@dataclass
class Address:
    street: str
    city: str
    zip_code: str

@dataclass
class Person:
    name: str
    age: int
    email: str
    address: Address
    tags: list[str] = field(default_factory=list)

    def to_json(self):
        return json.dumps(asdict(self), indent=2)

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        data['address'] = Address(**data['address'])
        return cls(**data)

    def to_dict(self):
        return asdict(self)

person = Person("Alice", 30, "alice@test.com", Address("123 Main St", "NYC", "10001"), ["dev", "python"])
json_str = person.to_json()
print(f"JSON:\n{json_str}")

restored = Person.from_json(json_str)
print(f"\nRestored: {restored}")

# === Serialization comparison ===
print("\n=== Format Comparison ===")

data = {"name": "Alice", "scores": [95, 87, 92], "active": True, "gpa": 3.8}

# JSON
json_bytes = json.dumps(data).encode()

# Pickle
pickle_bytes = pickle.dumps(data)

# Custom binary (list of values)
values = list(data.values())
# Binary for individual values
bin_sizes = sum(len(bs.serialize(v)) for v in values)

print(f"  JSON:   {len(json_bytes):4d} bytes")
print(f"  Pickle: {len(pickle_bytes):4d} bytes")
print(f"  Binary: {bin_sizes:4d} bytes (individual values)")

# === Schema validation ===
print("\n=== Schema Validation ===")

class Schema:
    def __init__(self, **fields):
        self.fields = fields

    def validate(self, data):
        errors = []
        for field_name, field_type in self.fields.items():
            if field_name not in data:
                errors.append(f"Missing field: {field_name}")
            elif not isinstance(data[field_name], field_type):
                errors.append(f"{field_name}: expected {field_type.__name__}, got {type(data[field_name]).__name__}")
        return errors

schema = Schema(name=str, age=int, email=str, active=bool)
valid_data = {"name": "Alice", "age": 30, "email": "a@b.com", "active": True}
invalid_data = {"name": "Alice", "age": "thirty"}

print(f"Valid:   errors = {schema.validate(valid_data)}")
print(f"Invalid: errors = {schema.validate(invalid_data)}")