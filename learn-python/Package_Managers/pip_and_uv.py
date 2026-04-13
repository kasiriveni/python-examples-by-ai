"""
Package Managers: pip, venv, pipx, uv — usage patterns and dependency tooling.
"""
import subprocess
import sys
import os
import json
import re
from pathlib import Path
from dataclasses import dataclass, field

# ═══════════════════════════════════════════
# 1. Pip usage reference
# ═══════════════════════════════════════════
PIP_COMMANDS = {
    "install": "pip install <package>                    # install latest",
    "install_version": "pip install 'requests==2.31.0'          # exact version",
    "install_range": "pip install 'flask>=2.0,<3.0'           # version range",
    "install_extras": "pip install 'fastapi[standard]'          # with extras",
    "install_editable": "pip install -e .                         # editable install",
    "install_requirements": "pip install -r requirements.txt       # from file",
    "uninstall": "pip uninstall <package>                 # remove package",
    "list": "pip list                                # list installed",
    "list_outdated": "pip list --outdated                     # show upgradable",
    "show": "pip show <package>                      # package metadata",
    "freeze": "pip freeze > requirements.txt          # export locked deps",
    "check": "pip check                               # detect conflicts",
    "download": "pip download <pkg> -d ./wheels          # download WHL files",
    "install_offline": "pip install --no-index --find-links=./wheels <pkg>  # offline",
    "upgrade_pip": "python -m pip install --upgrade pip   # upgrade pip itself",
}

def print_pip_cheatsheet():
    print("=== pip cheatsheet ===")
    for key, cmd in PIP_COMMANDS.items():
        print(f"  {cmd}")

# ═══════════════════════════════════════════
# 2. Virtual environment management
# ═══════════════════════════════════════════
VENV_GUIDE = {
    "create": "python -m venv .venv",
    "activate_linux":  "source .venv/bin/activate",
    "activate_windows": ".venv\\Scripts\\activate",
    "deactivate": "deactivate",
    "python_in_venv": ".venv/bin/python  (Linux) | .venv\\Scripts\\python.exe (Windows)",
}

def create_venv(path: Path, python: str | None = None) -> Path:
    """Create a virtual environment at path."""
    import venv
    builder = venv.EnvBuilder(
        system_site_packages=False,
        clear=True,
        symlinks=False,
        upgrade=False,
        with_pip=True,
    )
    builder.create(path)
    return path

def get_venv_python(venv_path: Path) -> Path:
    """Return the Python executable inside a venv."""
    if sys.platform == "win32":
        return venv_path / "Scripts" / "python.exe"
    return venv_path / "bin" / "python"

# ═══════════════════════════════════════════
# 3. requirements.txt formats
# ═══════════════════════════════════════════
REQUIREMENTS_FORMATS = """
# requirements.txt — various specification formats

# Exact version (pinned — used in lock files)
requests==2.31.0

# Compatible release (>=2.31.0, <3.0.0)
requests~=2.31

# Minimum version
flask>=3.0

# Version range
django>=4.2,<5.0

# Without version (latest) — avoid in production
numpy

# With extras
fastapi[standard]>=0.100

# From a VCS (git)
git+https://github.com/org/repo.git@main#egg=mypackage

# Editable local package
-e ./packages/mylib

# Include another file
-r base-requirements.txt

# Hash pinning (most secure)
requests==2.31.0 \\
    --hash=sha256:58cd2187423839... \\
    --hash=sha256:942c5a758f98...
"""

# ═══════════════════════════════════════════
# 4. pyproject.toml dependency groups
# ═══════════════════════════════════════════
PYPROJECT_TOML_DEPS = """
[project]
name = "my-app"
version = "1.0.0"
requires-python = ">=3.11"
dependencies = [
    "requests>=2.31",
    "pydantic>=2.0",
    "fastapi>=0.100",
]

[project.optional-dependencies]
dev  = ["pytest>=7", "ruff>=0.1", "mypy>=1.0"]
test = ["pytest>=7", "pytest-asyncio", "httpx"]
docs = ["sphinx", "sphinx-rtd-theme"]

# Install with: pip install -e '.[dev,test]'
"""

# ═══════════════════════════════════════════
# 5. PipManager helper class
# ═══════════════════════════════════════════
@dataclass
class PackageInfo:
    name: str
    version: str
    location: str = ""
    requires: list[str] = field(default_factory=list)

class PipManager:
    """Wrapper around pip commands via subprocess."""

    def __init__(self, python: str = sys.executable):
        self.python = python

    def _run(self, *args: str) -> tuple[int, str]:
        result = subprocess.run(
            [self.python, "-m", "pip", *args],
            capture_output=True, text=True
        )
        return result.returncode, result.stdout + result.stderr

    def list_packages(self) -> list[dict]:
        rc, out = self._run("list", "--format=json")
        if rc != 0: return []
        try:
            return json.loads(out)
        except json.JSONDecodeError:
            return []

    def show(self, package: str) -> PackageInfo | None:
        rc, out = self._run("show", package)
        if rc != 0: return None
        info: dict[str, str] = {}
        for line in out.splitlines():
            if ":" in line:
                k, _, v = line.partition(":")
                info[k.strip().lower().replace("-", "_")] = v.strip()
        return PackageInfo(
            name=info.get("name", package),
            version=info.get("version", ""),
            location=info.get("location", ""),
            requires=[r.strip() for r in info.get("requires", "").split(",") if r.strip()],
        )

    def is_installed(self, package: str) -> bool:
        return self.show(package) is not None

    def freeze(self) -> list[str]:
        rc, out = self._run("freeze")
        if rc != 0: return []
        return [line for line in out.splitlines() if line and not line.startswith("#")]

# ═══════════════════════════════════════════
# 6. uv / pipx reference (modern tooling)
# ═══════════════════════════════════════════
UV_COMMANDS = {
    "init":             "uv init myproject                      # create new project",
    "venv":             "uv venv                                # create .venv",
    "add":              "uv add requests                        # add dependency",
    "add_dev":          "uv add --dev pytest                    # add dev dependency",
    "remove":           "uv remove requests                     # remove dependency",
    "sync":             "uv sync                                # install from lockfile",
    "run":              "uv run python app.py                   # run in project venv",
    "run_tool":         "uv run pytest                          # run dev tool",
    "lock":             "uv lock                                # regenerate lockfile",
    "pip_install":      "uv pip install requests                # drop-in pip replacement",
    "python_install":   "uv python install 3.12                 # install Python version",
}

PIPX_COMMANDS = {
    "install":          "pipx install ruff                      # install CLI tool globally",
    "upgrade":          "pipx upgrade ruff                      # upgrade a tool",
    "list":             "pipx list                              # show installed tools",
    "run":              "pipx run black .                       # run without installing",
    "inject":           "pipx inject myenv requests             # add dep to existing env",
    "uninstall":        "pipx uninstall ruff                    # remove tool",
}

# ═══════════════════════════════════════════
# 7. Dependency resolver (simple)
# ═══════════════════════════════════════════
def parse_requirement(req: str) -> tuple[str, str]:
    """Parse 'package>=1.0,<2.0' into ('package', '>=1.0,<2.0')."""
    match = re.match(r"([A-Za-z0-9_\-\.]+)(.*)", req.strip())
    if not match:
        return req, ""
    return match.group(1), match.group(2).strip()

def check_conflicts(requirements: list[str]) -> list[str]:
    """Detect packages specified more than once (potential conflict)."""
    seen: dict[str, list[str]] = {}
    for req in requirements:
        name, spec = parse_requirement(req)
        seen.setdefault(name.lower(), []).append(spec)
    return [
        f"{name}: {specs}"
        for name, specs in seen.items()
        if len(specs) > 1
    ]

# ═══════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════
if __name__ == "__main__":
    print_pip_cheatsheet()

    print("\n=== Current Python environment ===")
    mgr = PipManager()
    pkgs = mgr.list_packages()
    print(f"  Installed packages: {len(pkgs)}")
    for pkg in sorted(pkgs, key=lambda p: p["name"])[:8]:
        print(f"    {pkg['name']:30s} {pkg['version']}")
    if len(pkgs) > 8:
        print(f"    ... and {len(pkgs)-8} more")

    print("\n=== pip show requests ===")
    info = mgr.show("requests")
    if info:
        print(f"  {info.name} {info.version}")
        print(f"  requires: {info.requires[:5]}")
    else:
        print("  requests not installed")

    print("\n=== Freeze (first 5) ===")
    for line in mgr.freeze()[:5]:
        print(f"  {line}")

    print("\n=== parse_requirement ===")
    for req in ["requests>=2.31.0,<3", "flask[async]>=2.0", "numpy", "mypy==1.5"]:
        name, spec = parse_requirement(req)
        print(f"  {req!r} → name={name!r} spec={spec!r}")

    print("\n=== conflict check ===")
    reqs = ["requests>=2.0", "flask>=2.0", "requests==2.31.0"]
    conflicts = check_conflicts(reqs)
    if conflicts:
        for c in conflicts:
            print(f"  ⚠ Conflict: {c}")
    else:
        print("  No conflicts")

    print("\n=== uv commands reference ===")
    for name, cmd in UV_COMMANDS.items():
        print(f"  {cmd}")

    print("\n=== pipx commands reference ===")
    for name, cmd in PIPX_COMMANDS.items():
        print(f"  {cmd}")
