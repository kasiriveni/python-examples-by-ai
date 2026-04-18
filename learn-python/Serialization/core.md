# Core Python Concepts

## Core Themes
- Text and binary serialization strategies.
- JSON, pickle, CSV, XML, and custom binary encodings.
- Preserving structure and custom types during marshalling.

## Core Theme Examples
- Example 1: JSON serialization with custom encoder classes.
- Example 2: Struct packing for binary record formats.
- Example 3: Pickle preserving Python class and function types.

## Files and Concepts
- binary_serialization.py: struct packing, type tags, dataclass serialization, custom binary formats
- serialization_comprehensive.py: pickle, JSON custom encoders, struct binary formats, record headers
- serialization_examples.py: basic pickle and JSON file operations
- serialization_patterns.py: custom JSON encoders, CSV with dataclasses, XML parsing, marshalling patterns

## Core Example
This example serializes a dictionary to JSON and back again.

```python
import json

payload = {"name": "Alice", "age": 30}
text = json.dumps(payload)
restored = json.loads(text)

print(text)
print(restored["name"])
```
