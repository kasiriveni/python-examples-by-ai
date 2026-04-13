"""
Packaging and Distribution: Namespace packages and plugin systems.
"""
import importlib
import importlib.util
import sys
from pathlib import Path
from typing import Protocol, runtime_checkable

# ─────────────────────────────────────────────────────────
# 1. Namespace packages (PEP 420)
# ─────────────────────────────────────────────────────────
NAMESPACE_EXPLAINER = """
Namespace packages allow splitting a single package across multiple directories.
They DON'T have __init__.py in the namespace root.

Example file structure:
  pkg-a/
    mycompany/          ← no __init__.py  (namespace root)
      auth/
        __init__.py
        login.py

  pkg-b/
    mycompany/          ← no __init__.py  (same namespace)
      payments/
        __init__.py
        checkout.py

After installing both packages:
  from mycompany.auth.login import login_user
  from mycompany.payments.checkout import checkout

Both mycompany.auth and mycompany.payments work from the same 'mycompany' namespace.
"""

# ─────────────────────────────────────────────────────────
# 2. Plugin protocol
# ─────────────────────────────────────────────────────────
@runtime_checkable
class PluginProtocol(Protocol):
    """Every plugin must implement this interface."""
    name: str
    version: str

    def execute(self, data: dict) -> dict:
        ...

    def validate(self, data: dict) -> bool:
        ...

# ─────────────────────────────────────────────────────────
# 3. Plugin registry
# ─────────────────────────────────────────────────────────
class PluginRegistry:
    def __init__(self):
        self._plugins: dict[str, PluginProtocol] = {}

    def register(self, plugin: PluginProtocol) -> None:
        if not isinstance(plugin, PluginProtocol):
            raise TypeError(f"{plugin!r} does not implement PluginProtocol")
        self._plugins[plugin.name] = plugin
        print(f"  Registered plugin: {plugin.name} v{plugin.version}")

    def get(self, name: str) -> PluginProtocol:
        if name not in self._plugins:
            raise KeyError(f"Plugin '{name}' not found. Available: {list(self._plugins)}")
        return self._plugins[name]

    def execute(self, name: str, data: dict) -> dict:
        plugin = self.get(name)
        if not plugin.validate(data):
            raise ValueError(f"Invalid data for plugin '{name}'")
        return plugin.execute(data)

    def list_plugins(self) -> list[dict]:
        return [{"name": p.name, "version": p.version} for p in self._plugins.values()]

# ─────────────────────────────────────────────────────────
# 4. Sample plugins
# ─────────────────────────────────────────────────────────
class JSONPlugin:
    name = "json_processor"
    version = "1.0.0"

    def validate(self, data: dict) -> bool:
        return "payload" in data

    def execute(self, data: dict) -> dict:
        import json
        payload = data["payload"]
        serialized = json.dumps(payload, indent=2)
        return {"result": serialized, "bytes": len(serialized)}

class HashPlugin:
    name = "hash_processor"
    version = "2.1.0"

    def validate(self, data: dict) -> bool:
        return "text" in data

    def execute(self, data: dict) -> dict:
        import hashlib
        alg = data.get("algorithm", "sha256")
        h = hashlib.new(alg, data["text"].encode())
        return {"hash": h.hexdigest(), "algorithm": alg}

class TransformPlugin:
    name = "text_transform"
    version = "1.0.0"

    def validate(self, data: dict) -> bool:
        return "text" in data and "operation" in data

    def execute(self, data: dict) -> dict:
        ops = {
            "upper": str.upper, "lower": str.lower,
            "title": str.title, "reverse": lambda s: s[::-1],
        }
        op = data.get("operation", "upper")
        if op not in ops:
            raise ValueError(f"Unknown op: {op}")
        return {"result": ops[op](data["text"])}

# ─────────────────────────────────────────────────────────
# 5. Entry points discovery (simulated)
# ─────────────────────────────────────────────────────────
def discover_plugins_from_entry_points(group: str) -> list:
    """
    Real usage:
        from importlib.metadata import entry_points
        plugins = entry_points(group='myapp.plugins')
        for ep in plugins:
            plugin_class = ep.load()
            registry.register(plugin_class())

    In pyproject.toml, register like:
        [project.entry-points."myapp.plugins"]
        json  = "mypackage.plugins.json_plugin:JSONPlugin"
        hash  = "mypackage.plugins.hash_plugin:HashPlugin"
    """
    try:
        from importlib.metadata import entry_points
        eps = entry_points(group=group)
        loaded = []
        for ep in eps:
            try:
                cls = ep.load()
                loaded.append(cls())
            except Exception as e:
                print(f"  Failed to load {ep.name}: {e}")
        return loaded
    except Exception:
        return []  # No plugins installed in this environment

# ─────────────────────────────────────────────────────────
# 6. Dynamic import
# ─────────────────────────────────────────────────────────
def load_plugin_from_path(module_path: str, class_name: str):
    """Load a plugin class from an arbitrary .py file path."""
    path = Path(module_path)
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if not spec or not spec.loader:
        raise ImportError(f"Cannot load: {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, class_name)

if __name__ == "__main__":
    print("=== Plugin Registry ===\n")

    registry = PluginRegistry()
    registry.register(JSONPlugin())
    registry.register(HashPlugin())
    registry.register(TransformPlugin())

    print(f"\nLoaded plugins: {registry.list_plugins()}\n")

    print("=== Execute Plugins ===")
    result = registry.execute("json_processor", {"payload": {"name": "Alice", "age": 30}})
    print(f"JSON plugin: {result}\n")

    result = registry.execute("hash_processor", {"text": "Hello, World!", "algorithm": "md5"})
    print(f"Hash plugin: {result}\n")

    result = registry.execute("text_transform", {"text": "hello world", "operation": "title"})
    print(f"Transform plugin: {result}\n")

    print("=== Protocol Check ===")
    print(f"JSONPlugin implements PluginProtocol: {isinstance(JSONPlugin(), PluginProtocol)}")

    bad_plugin = object()
    print(f"object() implements PluginProtocol: {isinstance(bad_plugin, PluginProtocol)}")

    print("\n=== Namespace Packages ===")
    print(NAMESPACE_EXPLAINER)
