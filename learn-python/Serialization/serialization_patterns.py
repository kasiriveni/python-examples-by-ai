"""
Serialization: JSON, pickle, CSV, XML, and custom marshalling patterns.
"""
import json
import csv
import pickle
import xml.etree.ElementTree as ET
import io
from dataclasses import dataclass, asdict, field
from datetime import datetime, date
from typing import Any
from uuid import UUID, uuid4
from enum import Enum

# ═══════════════════════════════════════════
# 1. JSON with custom encoder / decoder
# ═══════════════════════════════════════════
class Status(Enum):
    ACTIVE   = "active"
    INACTIVE = "inactive"

@dataclass
class User:
    id:         UUID
    name:       str
    email:      str
    created_at: datetime
    status:     Status
    tags:       list[str] = field(default_factory=list)

class AppJSONEncoder(json.JSONEncoder):
    """Handles datetime, date, UUID, Enum, dataclasses."""
    def default(self, obj):
        if isinstance(obj, datetime): return {"__type__": "datetime", "value": obj.isoformat()}
        if isinstance(obj, date):     return {"__type__": "date",     "value": obj.isoformat()}
        if isinstance(obj, UUID):     return {"__type__": "uuid",     "value": str(obj)}
        if isinstance(obj, Enum):     return {"__type__": "enum",     "value": obj.value}
        if hasattr(obj, "__dataclass_fields__"):
            d = asdict(obj)
            d["__class__"] = type(obj).__name__
            return d
        return super().default(obj)

def app_json_decoder(dct: dict) -> Any:
    t = dct.get("__type__")
    if t == "datetime": return datetime.fromisoformat(dct["value"])
    if t == "date":     return date.fromisoformat(dct["value"])
    if t == "uuid":     return UUID(dct["value"])
    if t == "enum":     return dct["value"]  # just return the value string
    return dct

def demo_json():
    print("=== JSON Serialization ===")
    user = User(
        id=uuid4(), name="Alice", email="alice@example.com",
        created_at=datetime(2024, 1, 15, 10, 30),
        status=Status.ACTIVE, tags=["admin", "beta"]
    )
    json_str = json.dumps(user, cls=AppJSONEncoder, indent=2)
    print(f"  Serialized (first 120 chars): {json_str[:120]}...")

    rebuilt = json.loads(json_str, object_hook=app_json_decoder)
    print(f"  created_at type: {type(rebuilt['created_at']).__name__}")
    print(f"  id type: {type(rebuilt['id']).__name__}")

    # JSON Schema patterns
    schema_example = {
        "type": "object",
        "required": ["name", "email"],
        "properties": {
            "name":  {"type": "string", "minLength": 1},
            "email": {"type": "string", "format": "email"},
            "age":   {"type": "integer", "minimum": 0, "maximum": 150},
        }
    }
    print(f"  Schema example: {json.dumps(schema_example, indent=2)[:100]}...")

# ═══════════════════════════════════════════
# 2. CSV reading / writing
# ═══════════════════════════════════════════
@dataclass
class Product:
    sku:      str
    name:     str
    price:    float
    quantity: int
    category: str

def demo_csv():
    print("\n=== CSV ===")
    products = [
        Product("P001", "Widget A", 9.99,  100, "gadgets"),
        Product("P002", "Gizmo B",  24.50, 50,  "tools"),
        Product("P003", "Doohickey",4.75,  200, "gadgets"),
    ]

    # Write
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=["sku","name","price","quantity","category"])
    writer.writeheader()
    for p in products:
        writer.writerow(asdict(p))
    csv_content = buf.getvalue()
    print(f"  CSV output:\n{csv_content}")

    # Read back
    reader = csv.DictReader(io.StringIO(csv_content))
    loaded = [Product(r["sku"], r["name"], float(r["price"]),
                      int(r["quantity"]), r["category"]) for r in reader]
    print(f"  Loaded {len(loaded)} products")
    total_value = sum(p.price * p.quantity for p in loaded)
    print(f"  Inventory value: ${total_value:,.2f}")

    # csv.reader (positional)
    raw = "alice,30,alice@example.com\nbob,25,bob@example.com"
    for row in csv.reader(io.StringIO(raw)):
        name, age, email = row
        print(f"  name={name}, age={age}, email={email}")

# ═══════════════════════════════════════════
# 3. Pickle (Python objects)
# ═══════════════════════════════════════════
def demo_pickle():
    print("\n=== Pickle ===")
    data = {
        "users": [{"name": "Alice", "active": True}, {"name": "Bob", "active": False}],
        "config": {"debug": False, "max_retries": 3},
        "scores": [95.5, 88.0, 72.3],
    }
    # Serialize
    blob = pickle.dumps(data)
    print(f"  Pickled bytes: {len(blob)}")

    # Deserialize
    restored = pickle.loads(blob)
    print(f"  Restored users: {[u['name'] for u in restored['users']]}")

    # Custom __reduce__
    class SafeBox:
        def __init__(self, value: int):
            self.value = value
            self._secret = "DO_NOT_SERIALIZE"
        def __reduce__(self):
            # Only serialize `value`, not _secret
            return (SafeBox, (self.value,))
        def __repr__(self): return f"SafeBox({self.value})"

    box = SafeBox(42)
    restored_box: SafeBox = pickle.loads(pickle.dumps(box))
    print(f"  SafeBox: {restored_box}, has _secret = {hasattr(restored_box, '_secret')}")

# ═══════════════════════════════════════════
# 4. XML building and parsing
# ═══════════════════════════════════════════
def demo_xml():
    print("\n=== XML ===")

    # Build XML
    root = ET.Element("catalog")
    root.set("version", "1.0")
    root.set("date", "2024-01-15")

    items = [
        ("book",   {"id": "B01", "price": "29.99"}, "Python Mastery"),
        ("ebook",  {"id": "E01", "price": "14.99"}, "Async Python"),
    ]
    for tag, attrs, title in items:
        item = ET.SubElement(root, "item", attrib=attrs)
        item.set("type", tag)
        title_el = ET.SubElement(item, "title")
        title_el.text = title
        ET.SubElement(item, "available").text = "true"

    ET.indent(root, space="  ")
    xml_str = ET.tostring(root, encoding="unicode")
    print(f"  Built XML:\n{xml_str}")

    # Parse XML
    tree = ET.fromstring(xml_str)
    for item in tree.findall("item"):
        t = item.find("title")
        print(f"  [{item.get('type')}] {item.get('id')}: {t.text} @ ${item.get('price')}")

# ═══════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════
if __name__ == "__main__":
    demo_json()
    demo_csv()
    demo_pickle()
    demo_xml()
