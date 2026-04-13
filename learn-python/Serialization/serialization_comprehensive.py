"""
Serialization: pickle, json, yaml, msgpack examples.
"""
import pickle
import json
import struct
from dataclasses import dataclass, asdict
from datetime import datetime

# --- Pickle (Python-specific binary) ---
print("=== Pickle ===")

data = {
    "name": "Alice",
    "scores": [95, 87, 92],
    "metadata": {"enrolled": True, "year": 2024},
}

# Serialize
pickled = pickle.dumps(data)
print(f"Pickled size: {len(pickled)} bytes")

# Deserialize
restored = pickle.loads(pickled)
print(f"Restored: {restored}")

# Pickle custom objects
@dataclass
class Student:
    name: str
    age: int
    gpa: float

    def is_honors(self):
        return self.gpa >= 3.5

student = Student("Alice", 20, 3.8)
pickled_student = pickle.dumps(student)
restored_student = pickle.loads(pickled_student)
print(f"Student: {restored_student}, Honors: {restored_student.is_honors()}")

# --- JSON ---
print("\n=== JSON ===")

# Custom serializer/deserializer
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return {"__datetime__": obj.isoformat()}
        if isinstance(obj, set):
            return {"__set__": list(obj)}
        return super().default(obj)

def json_decoder(dct):
    if "__datetime__" in dct:
        return datetime.fromisoformat(dct["__datetime__"])
    if "__set__" in dct:
        return set(dct["__set__"])
    return dct

data_with_types = {
    "timestamp": datetime(2024, 3, 15, 10, 30),
    "tags": {"python", "tutorial"},
    "count": 42,
}

encoded = json.dumps(data_with_types, cls=JSONEncoder, indent=2)
print(f"Encoded:\n{encoded}")

decoded = json.loads(encoded, object_hook=json_decoder)
print(f"Decoded: {decoded}")
print(f"Type of tags: {type(decoded['tags'])}")

# --- struct (binary packing) ---
print("\n=== Struct (Binary) ===")

# Pack data into bytes
format_str = '>I f 10s'  # big-endian: uint32, float, 10-char string
packed = struct.pack(format_str, 42, 3.14, b'Hello     ')
print(f"Packed: {packed} ({len(packed)} bytes)")

# Unpack
unpacked = struct.unpack(format_str, packed)
print(f"Unpacked: id={unpacked[0]}, value={unpacked[1]:.2f}, name={unpacked[2].strip()}")

# --- Custom serialization ---
print("\n=== Custom Binary Format ===")

class Record:
    HEADER = b'REC\x01'

    def __init__(self, id, name, value):
        self.id = id
        self.name = name
        self.value = value

    def to_bytes(self):
        name_bytes = self.name.encode('utf-8')
        return (
            self.HEADER
            + struct.pack('>I', self.id)
            + struct.pack('>H', len(name_bytes))
            + name_bytes
            + struct.pack('>d', self.value)
        )

    @classmethod
    def from_bytes(cls, data):
        offset = len(cls.HEADER)
        id_ = struct.unpack('>I', data[offset:offset+4])[0]
        offset += 4
        name_len = struct.unpack('>H', data[offset:offset+2])[0]
        offset += 2
        name = data[offset:offset+name_len].decode('utf-8')
        offset += name_len
        value = struct.unpack('>d', data[offset:offset+8])[0]
        return cls(id_, name, value)

record = Record(1, "sensor_a", 23.456)
binary = record.to_bytes()
print(f"Serialized: {binary.hex()}")

restored = Record.from_bytes(binary)
print(f"Restored: id={restored.id}, name={restored.name}, value={restored.value}")
