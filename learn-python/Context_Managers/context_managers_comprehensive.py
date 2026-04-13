"""
Context managers - comprehensive examples.
"""
from contextlib import contextmanager, suppress, redirect_stdout
import io
import tempfile
import os
import time

# === Basic context manager with class ===
class FileManager:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None

    def __enter__(self):
        self.file = open(self.filename, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()
        return False  # don't suppress exceptions

# === contextmanager decorator ===
@contextmanager
def timer(label=""):
    start = time.perf_counter()
    yield
    elapsed = time.perf_counter() - start
    print(f"  {label}: {elapsed:.6f}s")

print("=== Timer ===")
with timer("Sum 1M"):
    total = sum(range(1_000_000))

# === Temporary directory ===
@contextmanager
def temp_workspace():
    path = tempfile.mkdtemp()
    try:
        yield path
    finally:
        import shutil
        shutil.rmtree(path)

print("\n=== Temp Workspace ===")
with temp_workspace() as workspace:
    filepath = os.path.join(workspace, "test.txt")
    with open(filepath, 'w') as f:
        f.write("hello")
    print(f"  Created: {filepath}")
print("  Workspace cleaned up")

# === Database transaction simulator ===
@contextmanager
def transaction(db_name="mydb"):
    print(f"  BEGIN TRANSACTION on {db_name}")
    try:
        yield db_name
        print(f"  COMMIT on {db_name}")
    except Exception as e:
        print(f"  ROLLBACK on {db_name}: {e}")
        raise

print("\n=== Transaction ===")
with transaction() as db:
    print(f"  Inserting into {db}...")

try:
    with transaction() as db:
        raise ValueError("Constraint violation")
except ValueError:
    pass

# === suppress context manager ===
print("\n=== Suppress ===")
with suppress(FileNotFoundError):
    os.remove("nonexistent_file.txt")
print("  No error raised")

# === redirect_stdout ===
print("\n=== Redirect stdout ===")
buffer = io.StringIO()
with redirect_stdout(buffer):
    print("This goes to buffer")
    print("So does this")
print(f"  Captured: {buffer.getvalue()!r}")

# === Nested context managers ===
print("\n=== Nested ===")
@contextmanager
def managed_resource(name):
    print(f"  Acquiring {name}")
    yield name
    print(f"  Releasing {name}")

with managed_resource("A") as a, managed_resource("B") as b:
    print(f"  Using {a} and {b}")

# === Reentrant context manager ===
class IndentPrinter:
    def __init__(self):
        self.level = 0

    @contextmanager
    def indent(self):
        self.level += 1
        yield
        self.level -= 1

    def print(self, text):
        print("  " * self.level + text)

print("\n=== Reentrant ===")
printer = IndentPrinter()
printer.print("Level 0")
with printer.indent():
    printer.print("Level 1")
    with printer.indent():
        printer.print("Level 2")
    printer.print("Back to 1")
printer.print("Back to 0")
