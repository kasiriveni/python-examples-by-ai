"""
Working with paths using pathlib (modern approach).
"""
from pathlib import Path
import tempfile

# Creating paths
home = Path.home()
cwd = Path.cwd()
print(f"Home: {home}")
print(f"CWD: {cwd}")

# Path construction
config = home / ".config" / "myapp" / "settings.json"
print(f"Config path: {config}")
print(f"Parent: {config.parent}")
print(f"Name: {config.name}")
print(f"Stem: {config.stem}")
print(f"Suffix: {config.suffix}")
print(f"Parts: {config.parts}")

# Path checks
print(f"\nHome exists: {home.exists()}")
print(f"Home is dir: {home.is_dir()}")
print(f"Home is file: {home.is_file()}")

# Working with temp directory
with tempfile.TemporaryDirectory() as tmp:
    tmp_path = Path(tmp)

    # Create directory structure
    (tmp_path / "src" / "utils").mkdir(parents=True)
    (tmp_path / "tests").mkdir()

    # Create files
    (tmp_path / "README.md").write_text("# My Project")
    (tmp_path / "src" / "main.py").write_text("print('hello')")
    (tmp_path / "src" / "utils" / "helpers.py").write_text("pass")
    (tmp_path / "tests" / "test_main.py").write_text("pass")

    # Glob patterns
    print("\nAll .py files:")
    for py_file in tmp_path.rglob("*.py"):
        print(f"  {py_file.relative_to(tmp_path)}")

    # Reading and writing
    readme = tmp_path / "README.md"
    content = readme.read_text()
    print(f"\nREADME: {content}")

    # Iterating directory
    print("\nDirectory contents:")
    for item in sorted(tmp_path.iterdir()):
        kind = "DIR" if item.is_dir() else "FILE"
        print(f"  [{kind}] {item.name}")

    # File stats
    stat = readme.stat()
    print(f"\nREADME size: {stat.st_size} bytes")

    # Renaming
    new_name = tmp_path / "README.rst"
    readme.rename(new_name)
    print(f"Renamed to: {new_name.name}")

    # Resolve (absolute path)
    relative = Path("src/main.py")
    print(f"\nRelative: {relative}")
    print(f"Is absolute: {relative.is_absolute()}")

# Path matching
p = Path("/usr/local/bin/python3")
print(f"\nMatches '*.py': {p.match('*.py')}")
print(f"Matches 'python*': {p.match('python*')}")
