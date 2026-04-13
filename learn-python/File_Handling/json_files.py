"""
Working with JSON files in Python.
"""
import json
import tempfile
import os
from datetime import datetime, date
from pathlib import Path

tmp_dir = tempfile.mkdtemp()

# Basic JSON serialization
data = {
    "name": "Alice",
    "age": 30,
    "languages": ["Python", "JavaScript", "Go"],
    "address": {
        "city": "New York",
        "zip": "10001"
    },
    "active": True,
    "score": None
}

# Pretty print
json_str = json.dumps(data, indent=2)
print(f"JSON string:\n{json_str}")

# Write to file
json_path = os.path.join(tmp_dir, "data.json")
with open(json_path, 'w') as f:
    json.dump(data, f, indent=2)

# Read from file
with open(json_path, 'r') as f:
    loaded = json.load(f)
print(f"\nLoaded: {loaded}")

# Custom serializer for non-serializable types
class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        if isinstance(obj, set):
            return list(obj)
        if isinstance(obj, bytes):
            return obj.hex()
        return super().default(obj)

complex_data = {
    "timestamp": datetime.now(),
    "tags": {"python", "json", "tutorial"},
    "binary": b'\x00\x01\x02',
}

result = json.dumps(complex_data, cls=CustomEncoder, indent=2)
print(f"\nCustom encoded:\n{result}")

# Custom decoder
def date_decoder(dct):
    for key, value in dct.items():
        if isinstance(value, str):
            try:
                dct[key] = datetime.fromisoformat(value)
            except (ValueError, TypeError):
                pass
    return dct

json_with_dates = '{"created": "2024-03-15T10:30:00", "name": "test"}'
decoded = json.loads(json_with_dates, object_hook=date_decoder)
print(f"\nDecoded with dates: {decoded}")

# Sorting keys and compact format
compact = json.dumps(data, separators=(',', ':'))
sorted_keys = json.dumps(data, sort_keys=True, indent=2)
print(f"\nCompact: {compact[:50]}...")

# JSON Lines format
jsonl_path = os.path.join(tmp_dir, "data.jsonl")
records = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
    {"id": 3, "name": "Charlie"},
]
with open(jsonl_path, 'w') as f:
    for record in records:
        f.write(json.dumps(record) + '\n')

with open(jsonl_path, 'r') as f:
    loaded_records = [json.loads(line) for line in f]
print(f"\nJSON Lines: {loaded_records}")

# Cleanup
import shutil
shutil.rmtree(tmp_dir)
