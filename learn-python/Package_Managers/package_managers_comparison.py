"""
Package Managers: pip, pipx, uv, and poetry comparison.
"""

# === Pip (Standard) ===
PIP_USAGE = """
=== pip (Standard Package Manager) ===

pip install requests              # Install
pip install requests==2.31.0      # Specific version
pip install "requests>=2.28,<3"   # Version constraint
pip install -r requirements.txt   # From requirements file
pip install -e ".[dev]"           # Editable install with extras
pip uninstall requests            # Uninstall
pip freeze                        # List installed versions
pip list --outdated               # Show outdated packages
pip cache purge                   # Clear download cache
"""

# === UV (Modern, fast) ===
UV_USAGE = """
=== uv (Modern Rust-based installer) ===

# Install uv
pip install uv

# Package management (drop-in pip replacement)
uv pip install requests
uv pip install -r requirements.txt
uv pip freeze

# Project management
uv init myproject                 # Create new project
uv add requests                   # Add dependency
uv remove requests                # Remove dependency
uv lock                           # Generate lockfile
uv sync                           # Install from lockfile

# Virtual environment
uv venv                           # Create .venv
uv venv --python 3.12             # Specific Python

# Run tools
uvx ruff check .                  # Run tool without install
uvx pytest                        # Run pytest
"""

# === Poetry ===
POETRY_USAGE = """
=== poetry (Dependency Management) ===

# Install poetry
pip install poetry

# Project management
poetry new myproject              # Create new project
poetry init                       # Initialize in existing dir
poetry add requests               # Add dependency
poetry add --group dev pytest     # Add dev dependency
poetry remove requests            # Remove dependency
poetry install                    # Install all dependencies
poetry update                     # Update dependencies
poetry lock                       # Generate lockfile
poetry show                       # Show installed packages
poetry shell                      # Activate virtual env
poetry run pytest                 # Run command in env
poetry build                      # Build package
poetry publish                    # Publish to PyPI
"""

# === Comparison ===
COMPARISON = """
=== Comparison ===

Feature     | pip          | uv           | poetry
------------|-------------|--------------|--------
Speed       | Moderate    | Very Fast    | Moderate
Lockfile    | No          | Yes          | Yes
Resolver    | Basic       | Advanced     | Advanced
Venv        | Manual      | Built-in     | Built-in
Build       | Separate    | Built-in     | Built-in
Standards   | PEP 517     | PEP 517     | Custom*
Best for    | Simple      | Performance  | Full DX
"""

# === Practical: Reading installed packages ===
import importlib.metadata

def list_installed_packages(limit=10):
    """List installed packages using importlib.metadata."""
    packages = []
    for dist in importlib.metadata.distributions():
        packages.append({
            "name": dist.metadata["Name"],
            "version": dist.metadata["Version"],
        })

    # Deduplicate and sort
    seen = set()
    unique = []
    for p in packages:
        if p["name"] not in seen:
            seen.add(p["name"])
            unique.append(p)
    unique.sort(key=lambda p: p["name"].lower())

    return unique[:limit]

if __name__ == "__main__":
    print(PIP_USAGE)
    print(UV_USAGE)
    print(POETRY_USAGE)
    print(COMPARISON)

    print("\n=== Currently Installed Packages (first 10) ===")
    for pkg in list_installed_packages():
        print(f"  {pkg['name']:30s} {pkg['version']}")
