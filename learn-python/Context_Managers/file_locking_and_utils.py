"""
Context Managers: File locking, temporary dirs, and redirect patterns.
"""
import contextlib
import io
import os
import sys
import tempfile
from pathlib import Path

# ═══════════════════════════════════════════
# 1. Suppress exceptions
# ═══════════════════════════════════════════
print("=== contextlib.suppress ===")

with contextlib.suppress(FileNotFoundError):
    os.remove("does_not_exist.txt")
print("  Suppressed FileNotFoundError cleanly")

# Suppress multiple exc types
with contextlib.suppress(KeyError, TypeError):
    d: dict = {}
    _ = d["missing"]
print("  Suppressed KeyError cleanly")

# ═══════════════════════════════════════════
# 2. Redirect stdout / stderr
# ═══════════════════════════════════════════
print("\n=== Redirect Output ===")

buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    print("This goes to the buffer, not the terminal")
    print("So does this")
captured = buf.getvalue()
print(f"Captured:\n{captured.strip()}")

# Capture stderr
err_buf = io.StringIO()
with contextlib.redirect_stderr(err_buf):
    print("This is an error", file=sys.stderr)
print(f"Stderr captured: {err_buf.getvalue().strip()}")

# ═══════════════════════════════════════════
# 3. Temporary files and directories
# ═══════════════════════════════════════════
print("\n=== Temporary Files / Dirs ===")

# tempfile.TemporaryFile (auto-deleted)
with tempfile.TemporaryFile(mode="wb+") as f:
    f.write(b"binary data")
    f.seek(0)
    print(f"  Temp file: {f.read()}")
# auto-deleted here

# Named temp file
with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
    f.write("hello from temp")
    tmp_name = f.name

try:
    content = Path(tmp_name).read_text()
    print(f"  Named temp: {content!r}")
finally:
    os.unlink(tmp_name)

# Temp directory
with tempfile.TemporaryDirectory() as tmpdir:
    p = Path(tmpdir) / "data" / "output.txt"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("nested temp file")
    print(f"  Temp dir: {tmpdir}")
    print(f"  File exists: {p.exists()}")
# tmpdir deleted automatically

# ═══════════════════════════════════════════
# 4. Custom file-locking context manager
# ═══════════════════════════════════════════
import time
import threading

class ResourceLock:
    """Simple threading lock as a context manager."""

    def __init__(self, name: str, timeout: float = 5.0):
        self.name = name
        self.timeout = timeout
        self._lock = threading.Lock()

    def __enter__(self):
        acquired = self._lock.acquire(timeout=self.timeout)
        if not acquired:
            raise TimeoutError(f"Could not acquire lock '{self.name}' within {self.timeout}s")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._lock.release()
        return False  # don't suppress exceptions

    def try_enter(self) -> bool:
        return self._lock.acquire(blocking=False)

    def release(self) -> None:
        if self._lock.locked():
            self._lock.release()

class FileLock:
    """Cross-platform file-based lock using OS advisory locking."""

    def __init__(self, lockfile: str | Path):
        self.lockfile = Path(lockfile)
        self._lock_fd = None

    def acquire(self) -> None:
        self._lock_fd = open(self.lockfile, "w")
        try:
            import msvcrt
            msvcrt.locking(self._lock_fd.fileno(), msvcrt.LK_NBLCK, 1)
        except ImportError:
            import fcntl
            fcntl.flock(self._lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)

    def release(self) -> None:
        if self._lock_fd:
            try:
                import msvcrt
                self._lock_fd.seek(0)
                msvcrt.locking(self._lock_fd.fileno(), msvcrt.LK_UNLCK, 1)
            except ImportError:
                import fcntl
                fcntl.flock(self._lock_fd, fcntl.LOCK_UN)
            self._lock_fd.close()
            self._lock_fd = None
            self.lockfile.unlink(missing_ok=True)

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, *_):
        self.release()

# ═══════════════════════════════════════════
# 5. Timer and benchmark context managers
# ═══════════════════════════════════════════
class Timer:
    """Context manager that measures elapsed time."""

    def __init__(self, name: str = "", verbose: bool = True):
        self.name = name
        self.verbose = verbose
        self.elapsed: float = 0.0

    def __enter__(self):
        self._start = time.perf_counter()
        return self

    def __exit__(self, *_):
        self.elapsed = time.perf_counter() - self._start
        if self.verbose:
            label = f"{self.name}: " if self.name else ""
            print(f"  {label}{self.elapsed*1000:.3f} ms")

@contextlib.contextmanager
def benchmark(iterations: int = 1, name: str = ""):
    """Context manager for benchmarking repeated operations."""
    start = time.perf_counter()
    yield
    total = time.perf_counter() - start
    label = f"{name}: " if name else ""
    print(f"  {label}{iterations:,} iters in {total:.4f}s "
          f"({total/iterations*1e6:.2f} µs/iter)")

# ═══════════════════════════════════════════
# 6. Environment variable scope
# ═══════════════════════════════════════════
@contextlib.contextmanager
def temp_env(**kwargs):
    """Temporarily set env variables, restore on exit."""
    old = {k: os.environ.get(k) for k in kwargs}
    os.environ.update({k: str(v) for k, v in kwargs.items()})
    try:
        yield
    finally:
        for k, v in old.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v

if __name__ == "__main__":
    print("\n=== ResourceLock ===")
    lock = ResourceLock("demo")
    with lock:
        print("  Inside locked section")
    print("  Lock released")

    print("\n=== Timer ===")
    with Timer("List comprehension"):
        _ = [i**2 for i in range(100_000)]

    with Timer("Generator") as t:
        _ = list(i**2 for i in range(100_000))
    print(f"  (Stored elapsed: {t.elapsed*1000:.2f}ms)")

    print("\n=== Benchmark ===")
    N = 50_000
    with benchmark(N, "string join"):
        for _ in range(N):
            "-".join(str(i) for i in range(10))

    print("\n=== Temp Environment ===")
    os.environ["MY_VAR"] = "original"
    print(f"  Before: MY_VAR={os.environ.get('MY_VAR')}")
    with temp_env(MY_VAR="temporary", NEW_VAR="injected"):
        print(f"  Inside: MY_VAR={os.environ.get('MY_VAR')}, NEW_VAR={os.environ.get('NEW_VAR')}")
    print(f"  After:  MY_VAR={os.environ.get('MY_VAR')}, NEW_VAR={os.environ.get('NEW_VAR')}")

    print("\n=== Chained context managers ===")
    with contextlib.ExitStack() as stack:
        f1 = stack.enter_context(io.StringIO())
        f2 = stack.enter_context(io.StringIO())
        f1.write("stream 1")
        f2.write("stream 2")
        print(f"  f1: {f1.getvalue()}, f2: {f2.getvalue()}")
    # Both closed automatically
