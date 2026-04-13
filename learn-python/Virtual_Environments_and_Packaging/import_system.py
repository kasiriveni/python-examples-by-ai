"""
Virtual Environments and Packaging: Understanding Python's import system.
"""
import sys
import importlib
import importlib.util
import importlib.machinery
import types
import os
from pathlib import Path

# ═══════════════════════════════════════════
# 1. Import system internals
# ═══════════════════════════════════════════
print("=== Import System ===")

# sys.path — ordered list of search locations
print("\nsys.path entries:")
for p in sys.path[:5]:
    print(f"  {p or '(cwd)'}")

# sys.modules — already-loaded modules cache
print(f"\nLoaded modules count: {len(sys.modules)}")
print(f"'os' in cache:  {'os' in sys.modules}")
print(f"'math' in cache before import: {'math' in sys.modules}")
import math
print(f"'math' in cache after  import: {'math' in sys.modules}")
print(f"math origin: {math.__spec__.origin}")

# ═══════════════════════════════════════════
# 2. importlib.util — dynamic imports
# ═══════════════════════════════════════════
print("\n=== importlib.util ===")

def find_module(name: str) -> bool:
    spec = importlib.util.find_spec(name)
    return spec is not None

for module_name in ["os", "json", "numpy", "pandas", "nonexistent_pkg"]:
    available = find_module(module_name)
    print(f"  {module_name:20s}: {'found' if available else 'not found'}")

# Lazy import — import only when first accessed
def lazy_import(name: str) -> types.ModuleType:
    """Import a module lazily — it won't load until an attribute is accessed."""
    spec = importlib.util.find_spec(name)
    if spec is None:
        raise ImportError(f"No module named {name!r}")
    loader = importlib.util.LazyLoader(spec.loader)
    spec.loader = loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    loader.exec_module(module)
    return module

lazy_json = lazy_import("json")
print(f"\nLazy-loaded json module: {lazy_json.dumps({'a': 1})}")

# ═══════════════════════════════════════════
# 3. Load module from file path
# ═══════════════════════════════════════════
print("\n=== Load from File Path ===")

import tempfile

_SOURCE = """
def greet(name: str) -> str:
    return f"Hello, {name}!"

class Plugin:
    version = "1.0.0"
    def execute(self): return "plugin executed"
"""

with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
    f.write(_SOURCE)
    tmp_path = f.name

try:
    spec = importlib.util.spec_from_file_location("dynamic_module", tmp_path)
    mod  = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    print(f"greet: {mod.greet('World')}")
    p = mod.Plugin()
    print(f"Plugin v{p.version}: {p.execute()}")
finally:
    os.unlink(tmp_path)

# ═══════════════════════════════════════════
# 4. Custom import hook (meta path finder)
# ═══════════════════════════════════════════
print("\n=== Custom Import Hook ===")

class InMemoryFinder(importlib.abc.MetaPathFinder):
    """
    Import hook: makes modules defined in a dict importable.
    Usage: InMemoryFinder.register("virtual.hello", source_code)
    """
    _registry: dict[str, str] = {}

    @classmethod
    def register(cls, name: str, source: str) -> None:
        cls._registry[name] = source

    def find_spec(self, fullname, path, target=None):
        if fullname not in self._registry:
            return None
        return importlib.machinery.ModuleSpec(
            fullname, InMemoryLoader(self._registry[fullname]), origin="<in-memory>"
        )

class InMemoryLoader(importlib.abc.Loader):
    def __init__(self, source: str):
        self._source = source

    def create_module(self, spec): return None

    def exec_module(self, module):
        code = compile(self._source, "<in-memory>", "exec")
        exec(code, module.__dict__)

# Register the hook
sys.meta_path.insert(0, InMemoryFinder())

# Register a virtual module
InMemoryFinder.register("virtual.math_utils", """
def square(n): return n * n
def cube(n):   return n * n * n
PI = 3.14159265358979
""")

import virtual.math_utils as vmu  # type: ignore
print(f"virtual.math_utils.square(7): {vmu.square(7)}")
print(f"virtual.math_utils.PI:         {vmu.PI}")

# ═══════════════════════════════════════════
# 5. Package structure patterns
# ═══════════════════════════════════════════
print("\n=== Package Structure ===")

_PACKAGE_LAYOUTS = {
    "src layout (recommended)": """
mypackage/
├── src/
│   └── mypackage/
│       ├── __init__.py
│       ├── core.py
│       └── utils.py
├── tests/
│   └── test_core.py
├── pyproject.toml
└── README.md
""",
    "flat layout": """
mypackage/
├── mypackage/
│   ├── __init__.py
│   └── core.py
├── tests/
├── pyproject.toml
└── README.md
""",
    "namespace package (no __init__)": """
myorg/
└── mypackage/    ← no __init__.py at myorg level
    ├── __init__.py
    └── module.py
""",
}

for name, layout in _PACKAGE_LAYOUTS.items():
    print(f"  {name}:{layout}")

# ═══════════════════════════════════════════
# 6. Module attributes
# ═══════════════════════════════════════════
print("=== Module Attributes ===")
import json
attrs = ["__name__", "__file__", "__package__", "__spec__", "__loader__"]
for attr in attrs:
    val = getattr(json, attr, "N/A")
    if hasattr(val, "__class__"):
        val = str(val)[:60]
    print(f"  json.{attr:12s} = {val}")
