"""
Modules and packages in Python.
"""
import sys
import importlib
import types

# === Import mechanisms ===
print("=== Import Mechanisms ===")

# Standard import
import os
print(f"os.name = {os.name}")

# From import
from pathlib import Path
print(f"Path.cwd() = {Path.cwd()}")

# Import with alias
import collections as col
print(f"Counter: {col.Counter('hello')}")

# === Module attributes ===
print("\n=== Module Attributes ===")
print(f"__name__: {__name__}")
print(f"__file__: {__file__}")

# List module contents
import math
public_attrs = [a for a in dir(math) if not a.startswith('_')]
print(f"math module has {len(public_attrs)} public attributes")
print(f"First 10: {public_attrs[:10]}")

# === sys.path ===
print("\n=== sys.path ===")
for i, path in enumerate(sys.path[:5]):
    print(f"  [{i}] {path}")
print(f"  ... ({len(sys.path)} total entries)")

# === Dynamic imports ===
print("\n=== Dynamic Imports ===")
json_module = importlib.import_module("json")
data = json_module.dumps({"key": "value"})
print(f"Dynamic import json.dumps: {data}")

# Import submodule
os_path = importlib.import_module("os.path")
print(f"os.path.sep = {os_path.sep}")

# === Creating a module dynamically ===
print("\n=== Dynamic Module ===")
my_module = types.ModuleType("my_module")
my_module.greeting = "Hello from dynamic module!"
my_module.add = lambda a, b: a + b
sys.modules["my_module"] = my_module

import my_module
print(f"  {my_module.greeting}")
print(f"  add(3, 4) = {my_module.add(3, 4)}")

# Cleanup
del sys.modules["my_module"]

# === Module reload ===
print("\n=== Module Reload ===")
import json
importlib.reload(json)
print("  json module reloaded successfully")

# === __all__ and public API ===
print("\n=== __all__ ===")

# Check if module defines __all__
modules_with_all = []
for name in ["os", "json", "sys", "typing"]:
    mod = importlib.import_module(name)
    if hasattr(mod, '__all__'):
        modules_with_all.append(f"{name} ({len(mod.__all__)} exports)")
print(f"  Modules with __all__: {modules_with_all}")

# === Package structure example ===
print("\n=== Package Structure ===")
print("""
mypackage/
    __init__.py          # Makes it a package
    module_a.py          # mypackage.module_a
    module_b.py          # mypackage.module_b
    subpackage/
        __init__.py      # Makes it a subpackage
        module_c.py      # mypackage.subpackage.module_c

# __init__.py can:
# - Run initialization code
# - Define __all__ for 'from package import *'
# - Import submodules for convenient access
""")
