"""
Modules and Packages: Import system, __init__.py, __all__, relative imports, namespaces.
"""
import sys
import os
import importlib
import importlib.util
import importlib.metadata
import types
import pkgutil
from pathlib import Path

# ═══════════════════════════════════════════
# 1. How imports work
# ═══════════════════════════════════════════
def explain_import_system():
    print("=== Import system internals ===")
    # sys.path — module search path
    print(f"  sys.path count: {len(sys.path)}")
    print(f"  First entry: {sys.path[0]!r}")

    # sys.modules — already-imported modules cache
    print(f"  sys.modules count: {len(sys.modules)}")
    print(f"  'os' in sys.modules: {'os' in sys.modules}")

    # Module attributes
    os_mod = sys.modules["os"]
    print(f"  os.__file__: {os_mod.__file__}")
    print(f"  os.__spec__.name: {os_mod.__spec__.name}")

    # importlib.import_module — dynamic import
    json = importlib.import_module("json")
    print(f"  json.dumps type: {type(json.dumps)}")

def lazy_import(name: str) -> types.ModuleType:
    """Delay module load until attribute access (avoids circular imports)."""
    spec = importlib.util.find_spec(name)
    if spec is None:
        raise ImportError(f"Module {name!r} not found")
    loader = importlib.util.LazyLoader(spec.loader)  # type: ignore
    spec.loader = loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    loader.exec_module(module)
    return module

def import_from_path(path: str, name: str):
    """Import a .py file from an arbitrary path."""
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None:
        raise ImportError(f"Cannot load {path!r}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)   # type: ignore
    return module

# ═══════════════════════════════════════════
# 2. Package structure reference
# ═══════════════════════════════════════════
PACKAGE_STRUCTURE = """
mypackage/
├── __init__.py          # Makes directory a package; exposes public API
├── __main__.py          # python -m mypackage runs this
├── _internal.py         # Private by convention (_prefix)
├── constants.py
├── models/
│   ├── __init__.py      # Relative imports work inside a package
│   ├── user.py
│   └── product.py
└── utils/
    ├── __init__.py
    └── helpers.py

# __init__.py example — curated public API:
from .models.user import User
from .models.product import Product
from .utils.helpers import format_price

__all__ = ["User", "Product", "format_price"]
__version__ = "1.2.3"
__author__ = "Your Name"

# In models/user.py — relative import:
from ..constants import MAX_NAME_LENGTH
from ..utils.helpers import slugify
"""

# ═══════════════════════════════════════════
# 3. __all__ and attribute control
# ═══════════════════════════════════════════
# __all__ controls what `from module import *` exports
# It also acts as the documented public API

def _private_helper():   # underscore = private by convention
    return "internal"

def public_function():
    return "public"

class _InternalClass:
    pass

class PublicClass:
    pass

__all__ = ["public_function", "PublicClass"]
# `from this_module import *` would only import public_function and PublicClass

# ═══════════════════════════════════════════
# 4. Namespace packages (PEP 420)
# ═══════════════════════════════════════════
NAMESPACE_PACKAGE_EXPLANATION = """
# Regular package: directory WITH __init__.py
# Namespace package: directory WITHOUT __init__.py (PEP 420 / implicit)

# Both allow:
#   import myns.sub
#   from myns.sub import something

# Namespace packages enable splitting a package across multiple directories:
#   /path1/myns/contrib.py
#   /path2/myns/core.py
# Both are on sys.path → 'import myns.core' and 'import myns.contrib' both work

# Check if a package is a namespace package:
import importlib
spec = importlib.util.find_spec("email")
print(type(spec))         # ModuleSpec
print(spec.submodule_search_locations)  # _NamespacePath or list
"""

# ═══════════════════════════════════════════
# 5. Discovering sub-modules
# ═══════════════════════════════════════════
def list_package_contents(package_name: str) -> list[str]:
    """List all modules in a package using pkgutil."""
    try:
        pkg = importlib.import_module(package_name)
    except ImportError:
        return []
    path = getattr(pkg, "__path__", [])
    return [info.name for info in pkgutil.walk_packages(path, prefix=package_name+".")]

def get_installed_packages() -> list[tuple[str, str]]:
    """List installed packages via importlib.metadata."""
    packages = []
    for dist in importlib.metadata.distributions():
        try:
            name    = dist.metadata["Name"]
            version = dist.metadata["Version"]
            packages.append((name, version))
        except Exception:
            pass
    return sorted(packages, key=lambda x: x[0].lower())

# ═══════════════════════════════════════════
# 6. Module reloading
# ═══════════════════════════════════════════
def demonstrate_reload():
    """importlib.reload() re-executes module code in the existing module object."""
    import json
    original_id = id(json)
    importlib.reload(json)
    print(f"  json id before: {original_id}")
    print(f"  json id after:  {id(json)}")
    print(f"  Same object: {original_id == id(json)}")

# ═══════════════════════════════════════════
# 7. Entry points (plugin system)
# ═══════════════════════════════════════════
ENTRY_POINTS_EXAMPLE = """
# pyproject.toml [project.entry-points]
[project.entry-points."myapp.plugins"]
csv_exporter  = "myapp.plugins.csv:CsvExporter"
json_exporter = "myapp.plugins.json:JsonExporter"

# Discover at runtime:
from importlib.metadata import entry_points

eps = entry_points(group="myapp.plugins")
for ep in eps:
    plugin_class = ep.load()
    plugin = plugin_class()
    plugin.export(data)

# Console scripts entry point:
[project.scripts]
my-cli = "myapp.cli:main"
"""

# ═══════════════════════════════════════════
# 8. Creating a module object dynamically
# ═══════════════════════════════════════════
def create_module_dynamically() -> types.ModuleType:
    """Build a module object in memory without a .py file."""
    mod = types.ModuleType("synthetic_module")
    mod.__doc__ = "Dynamically created module"
    mod.VERSION = "0.1.0"
    mod.greet = lambda name: f"Hello, {name}!"

    # Functions need __module__ set to look natural
    mod.greet.__module__ = mod.__name__

    sys.modules["synthetic_module"] = mod
    return mod

# ═══════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════
if __name__ == "__main__":
    explain_import_system()

    print("\n=== Dynamic module creation ===")
    m = create_module_dynamically()
    print(f"  synthetic_module.VERSION = {m.VERSION}")
    print(f"  synthetic_module.greet() = {m.greet('World')}")
    import synthetic_module  # now importable
    print(f"  import synthetic_module: {synthetic_module.VERSION}")

    print("\n=== Module reload ===")
    demonstrate_reload()

    print("\n=== email package sub-modules (first 5) ===")
    email_mods = list_package_contents("email")
    for m in email_mods[:5]:
        print(f"  {m}")
    print(f"  ...total: {len(email_mods)}")

    print("\n=== Package structure reference ===")
    print(PACKAGE_STRUCTURE)

    print("=== __all__ controls 'import *' ===")
    print(f"  __all__ = {__all__}")
    print(f"  _private_helper is still callable: {_private_helper()!r}")
