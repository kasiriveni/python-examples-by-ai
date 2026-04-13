"""
Automation: File system operations.
"""
import os
import shutil
import tempfile
from pathlib import Path
import glob

# Create temp workspace
workspace = Path(tempfile.mkdtemp())
print(f"Workspace: {workspace}")

# Create directory structure
dirs = ["src", "tests", "docs", "data/raw", "data/processed"]
for d in dirs:
    (workspace / d).mkdir(parents=True, exist_ok=True)
print("Directories created.")

# Create sample files
files = {
    "src/main.py": "print('main')",
    "src/utils.py": "print('utils')",
    "tests/test_main.py": "# tests",
    "docs/README.md": "# Documentation",
    "data/raw/data1.csv": "a,b,c\n1,2,3",
    "data/raw/data2.csv": "a,b,c\n4,5,6",
}
for path, content in files.items():
    (workspace / path).write_text(content)
print("Files created.")

# List directory tree
def tree(path, prefix=""):
    entries = sorted(path.iterdir(), key=lambda p: (p.is_file(), p.name))
    for i, entry in enumerate(entries):
        connector = "└── " if i == len(entries) - 1 else "├── "
        print(f"{prefix}{connector}{entry.name}")
        if entry.is_dir():
            extension = "    " if i == len(entries) - 1 else "│   "
            tree(entry, prefix + extension)

print("\nDirectory tree:")
tree(workspace)

# Find files by pattern
print("\nPython files:")
for f in workspace.rglob("*.py"):
    print(f"  {f.relative_to(workspace)}")

# File size and stats
print("\nFile sizes:")
for f in workspace.rglob("*"):
    if f.is_file():
        size = f.stat().st_size
        print(f"  {f.relative_to(workspace)}: {size} bytes")

# Copy files
src = workspace / "data/raw/data1.csv"
dst = workspace / "data/processed/data1_copy.csv"
shutil.copy2(src, dst)
print(f"\nCopied: {src.name} -> {dst.name}")

# Move/rename files
old = workspace / "docs/README.md"
new = workspace / "docs/GUIDE.md"
old.rename(new)
print(f"Renamed: README.md -> GUIDE.md")

# Batch rename
print("\nBatch renaming CSV files:")
for csv_file in (workspace / "data/raw").glob("*.csv"):
    new_name = csv_file.with_name(f"processed_{csv_file.name}")
    csv_file.rename(new_name)
    print(f"  {csv_file.name} -> {new_name.name}")

# Cleanup
shutil.rmtree(workspace)
print("\nWorkspace cleaned up.")
