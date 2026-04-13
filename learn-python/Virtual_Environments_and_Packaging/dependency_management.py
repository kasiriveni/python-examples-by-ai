"""
Virtual Environments and Packaging: Dependency resolution and lock files.
"""
import re
import json
from dataclasses import dataclass, field
from typing import Iterator

# ═══════════════════════════════════════════
# 1. Dependency specification formats
# ═══════════════════════════════════════════
REQUIREMENTS_TXT = """
# requirements.txt — pip-compatible format
# Pinned for reproducibility
requests==2.31.0
urllib3>=1.26.0,<2.0
certifi>=2023.1.1

# With extras
aiohttp[speedups]==3.9.1

# VCS dependency
-e git+https://github.com/user/pkg.git@abc123#egg=mypkg

# Index options
--index-url https://pypi.org/simple/
--extra-index-url https://my-private-pypi.com/simple/
"""

PYPROJECT_DEPS = """
# pyproject.toml dependency groups (PEP 735)
[project]
name = "myapp"
requires-python = ">=3.10"
dependencies = [
    "requests>=2.28",
    "pydantic>=2.0",
    "sqlalchemy[asyncio]>=2.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "mypy>=1.0",
    "ruff>=0.1",
]
docs = [
    "sphinx>=7.0",
    "furo",
]

# pip extras: pip install myapp[dev,docs]
"""

# ═══════════════════════════════════════════
# 2. Dependency graph and simple resolver
# ═══════════════════════════════════════════
@dataclass
class Package:
    name: str
    version: str
    requires: list[str] = field(default_factory=list)

    @property
    def key(self) -> str:
        return self.name.lower()

PACKAGE_INDEX: dict[str, list[Package]] = {
    "requests": [
        Package("requests", "2.31.0", ["urllib3>=1.26.0,<3", "certifi>=2017.4.17"]),
        Package("requests", "2.28.0", ["urllib3>=1.21.1,<3", "certifi>=2017.4.17"]),
    ],
    "urllib3": [
        Package("urllib3", "2.1.0",  []),
        Package("urllib3", "1.26.18",[]),
    ],
    "certifi": [
        Package("certifi", "2024.2.2", []),
        Package("certifi", "2023.1.1", []),
    ],
    "aiohttp": [
        Package("aiohttp", "3.9.3", ["attrs>=17.3.0", "multidict>=4.5,<7.0"]),
    ],
    "attrs": [
        Package("attrs", "23.2.0", []),
    ],
    "multidict": [
        Package("multidict", "6.0.5", []),
    ],
    "pydantic": [
        Package("pydantic", "2.6.1", ["annotated-types>=0.4.0", "pydantic-core>=2.16.1"]),
        Package("pydantic", "1.10.12", []),
    ],
    "annotated-types": [
        Package("annotated-types", "0.6.0", []),
    ],
    "pydantic-core": [
        Package("pydantic-core", "2.16.3", []),
    ],
}

def parse_requirement(req: str) -> tuple[str, str]:
    """Parse 'name>=1.0,<2.0' → ('name', '>=1.0,<2.0')"""
    m = re.match(r'^([\w\-\.]+)\s*([><=!~^].+)?$', req.strip())
    if not m:
        raise ValueError(f"Cannot parse requirement: {req!r}")
    return m.group(1).lower(), (m.group(2) or "").strip()

def satisfies_constraint(version: str, constraint: str) -> bool:
    """Very simplified version of constraint checking."""
    if not constraint:
        return True
    # Parse ">=1.0,<2.0"
    for part in constraint.split(","):
        m = re.match(r'([><=!~^]{1,2})([\d.]+)', part.strip())
        if not m:
            continue
        op, req_ver = m.group(1), m.group(2)
        # Convert to tuples for comparison
        def to_tuple(v): return tuple(int(x) for x in v.split(".") if x.isdigit())
        cur = to_tuple(version)
        req = to_tuple(req_ver)
        # Pad to same length
        while len(cur) < len(req): cur += (0,)
        while len(req) < len(cur): req += (0,)
        ok = {">=": cur>=req, ">": cur>req, "<=": cur<=req,
              "<": cur<req,  "==": cur==req, "!=": cur!=req}.get(op, True)
        if not ok:
            return False
    return True

class DependencyResolver:
    def __init__(self, index: dict[str, list[Package]] = None):
        self.index = index or PACKAGE_INDEX
        self.resolved: dict[str, Package] = {}
        self._visited: set[str] = set()

    def resolve(self, requirements: list[str]) -> dict[str, Package]:
        self.resolved = {}
        self._visited = set()
        for req in requirements:
            name, constraint = parse_requirement(req)
            self._resolve_package(name, constraint)
        return self.resolved

    def _resolve_package(self, name: str, constraint: str) -> Package:
        key = f"{name}{constraint}"
        if key in self._visited:
            return self.resolved.get(name)
        self._visited.add(key)

        if name not in self.index:
            print(f"  [WARNING] Unknown package: {name}")
            return None

        # Pick latest satisfying version
        candidates = [p for p in self.index[name]
                      if satisfies_constraint(p.version, constraint)]
        if not candidates:
            raise RuntimeError(f"No version of '{name}' satisfies '{constraint}'")
        chosen = candidates[0]  # first = latest

        if name in self.resolved:
            existing = self.resolved[name]
            if not satisfies_constraint(existing.version, constraint):
                raise RuntimeError(
                    f"Conflict: {name} {existing.version} already resolved "
                    f"but {constraint} is required"
                )
            return existing

        self.resolved[name] = chosen
        for dep in chosen.requires:
            dep_name, dep_constraint = parse_requirement(dep)
            self._resolve_package(dep_name, dep_constraint)
        return chosen

    def lock_file(self) -> str:
        """Generate a simple lock file."""
        lines = ["# Auto-generated lock file\n"]
        for name in sorted(self.resolved):
            pkg = self.resolved[name]
            lines.append(f"{pkg.name}=={pkg.version}")
            for req in pkg.requires:
                lines.append(f"    # requires: {req}")
        return "\n".join(lines)

# ═══════════════════════════════════════════
# 3. Virtual environment patterns
# ═══════════════════════════════════════════
VENV_COMMANDS = {
    "Create (python3)":      "python3 -m venv .venv",
    "Create (specific)":     "python3.11 -m venv .venv --prompt myapp",
    "Create (no pip)":       "python3 -m venv .venv --without-pip",
    "Activate (bash)":       "source .venv/bin/activate",
    "Activate (fish)":       "source .venv/bin/activate.fish",
    "Activate (Windows)":    r".venv\Scripts\Activate.ps1",
    "Deactivate":            "deactivate",
    "Install package":       "pip install requests",
    "Install with extras":   "pip install myapp[dev]",
    "Install editable":      "pip install -e .",
    "Freeze deps":           "pip freeze > requirements.txt",
    "Install from lock":     "pip install -r requirements.lock",
    "Show package info":     "pip show requests",
    "List outdated":         "pip list --outdated",
    "Upgrade package":       "pip install --upgrade requests",
    "Uninstall":             "pip uninstall requests -y",
    "Audit vulnerabilities": "pip-audit",
}

# ═══════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════
if __name__ == "__main__":
    print("=== Dependency Resolver ===")
    resolver = DependencyResolver()
    requirements = ["requests>=2.28", "aiohttp>=3.8", "pydantic>=2.0"]

    try:
        resolved = resolver.resolve(requirements)
        print(f"\nResolved {len(resolved)} packages:")
        for name, pkg in sorted(resolved.items()):
            print(f"  {pkg.name}=={pkg.version}")
        print(f"\nLock file:\n{resolver.lock_file()}")
    except RuntimeError as e:
        print(f"Resolution error: {e}")

    print("\n=== Constraint Checker ===")
    tests = [("2.31.0", ">=2.28,<3"), ("1.0.0", ">=2.0"),
             ("2.0.0", "==2.0.0"), ("3.0.0", "!=3.0.0")]
    for ver, constraint in tests:
        ok = satisfies_constraint(ver, constraint)
        print(f"  {ver:10s} {constraint:20s} → {'ok' if ok else 'FAIL'}")

    print("\n=== Venv Commands ===")
    for name, cmd in VENV_COMMANDS.items():
        print(f"  {name:28s}: {cmd}")

    print("\n=== requirements.txt format ===")
    print(REQUIREMENTS_TXT)
