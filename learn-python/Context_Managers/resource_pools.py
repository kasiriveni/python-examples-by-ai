"""
Context Managers: Resource pools, connection pooling, and object reuse.
"""
import threading
import time
import queue
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import TypeVar, Generic, Callable

T = TypeVar("T")

# ═══════════════════════════════════════════
# 1. Generic Object Pool
# ═══════════════════════════════════════════
class ObjectPool(Generic[T]):
    """
    Thread-safe object pool.
    Objects are reused across borrows to avoid creation overhead.
    """

    def __init__(self, factory: Callable[[], T], max_size: int = 10):
        self._factory = factory
        self._max_size = max_size
        self._pool: queue.Queue[T] = queue.Queue(maxsize=max_size)
        self._created = 0
        self._lock = threading.Lock()

    def _create(self) -> T:
        with self._lock:
            if self._created < self._max_size:
                obj = self._factory()
                self._created += 1
                return obj
        raise RuntimeError("Pool exhausted")

    @contextmanager
    def acquire(self, timeout: float = 5.0):
        """Borrow an object from the pool."""
        try:
            obj = self._pool.get(timeout=timeout)
        except queue.Empty:
            obj = self._create()

        try:
            yield obj
        finally:
            self._pool.put(obj)

    @property
    def available(self) -> int:
        return self._pool.qsize()

    def stats(self) -> dict:
        return {"created": self._created, "available": self.available,
                "max_size": self._max_size}

# ═══════════════════════════════════════════
# 2. Database Connection Pool
# ═══════════════════════════════════════════
class FakeDBConnection:
    """Simulated database connection."""
    _id_counter = 0

    def __init__(self, dsn: str):
        FakeDBConnection._id_counter += 1
        self.id = FakeDBConnection._id_counter
        self.dsn = dsn
        self._in_use = False
        print(f"    [DB:{self.id}] Connecting to {dsn}")

    def execute(self, sql: str) -> list:
        time.sleep(0.002)
        return [{"result": sql, "conn_id": self.id}]

    def close(self):
        print(f"    [DB:{self.id}] Closing connection")

    def __repr__(self):
        return f"DBConn(id={self.id})"

class ConnectionPool:
    """Connection pool with health checks and reconnect."""

    def __init__(self, dsn: str, pool_size: int = 5):
        self.dsn = dsn
        self.pool_size = pool_size
        self._available: queue.Queue = queue.Queue()
        self._all_conns: list[FakeDBConnection] = []
        self._lock = threading.Lock()
        self._initialize()

    def _initialize(self):
        for _ in range(self.pool_size):
            conn = FakeDBConnection(self.dsn)
            self._all_conns.append(conn)
            self._available.put(conn)

    @contextmanager
    def get_connection(self, timeout: float = 10.0):
        """Get a connection from the pool."""
        try:
            conn = self._available.get(timeout=timeout)
        except queue.Empty:
            raise TimeoutError("No connection available")

        conn._in_use = True
        try:
            yield conn
        except Exception:
            # Could implement reconnect here
            raise
        finally:
            conn._in_use = False
            self._available.put(conn)

    def close_all(self):
        while not self._available.empty():
            conn = self._available.get_nowait()
            conn.close()

    def stats(self) -> dict:
        return {
            "pool_size": self.pool_size,
            "available": self._available.qsize(),
            "in_use": sum(1 for c in self._all_conns if c._in_use),
        }

# ═══════════════════════════════════════════
# 3. Reentrant + Counted resource
# ═══════════════════════════════════════════
class ReusableBuffer:
    """A byte buffer that resets state when returned to pool."""
    def __init__(self, size: int = 4096):
        self._buf = bytearray(size)
        self._pos = 0

    def write(self, data: bytes) -> int:
        end = self._pos + len(data)
        self._buf[self._pos:end] = data
        self._pos = end
        return len(data)

    def read(self) -> bytes:
        return bytes(self._buf[:self._pos])

    def reset(self):
        self._pos = 0

    def __len__(self):
        return self._pos

@contextmanager
def pooled_buffer(pool: ObjectPool[ReusableBuffer]):
    """Acquire buffer, reset on return."""
    with pool.acquire() as buf:
        buf.reset()
        yield buf
        # buf is reset before returning (or leave for pool to reset)

# ═══════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════
if __name__ == "__main__":
    print("=== Generic Object Pool ===")
    counter = [0]
    def make_item():
        counter[0] += 1
        return {"id": counter[0], "data": []}

    pool = ObjectPool(make_item, max_size=3)

    # Sequential borrows
    with pool.acquire() as item:
        item["data"].append("x")
        print(f"  Got: {item}")

    print(f"  Pool stats: {pool.stats()}")

    # Concurrent borrows
    results = []
    def worker(n):
        with pool.acquire() as item:
            time.sleep(0.01)
            results.append(item["id"])

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(5)]
    for t in threads: t.start()
    for t in threads: t.join()
    print(f"  Concurrent workers got conn IDs: {sorted(results)}")
    print(f"  Max created: {pool._created} (max_size=3)")

    print("\n=== Connection Pool ===")
    cp = ConnectionPool("postgresql://localhost/testdb", pool_size=3)
    print(f"  Init stats: {cp.stats()}")

    def db_worker(query):
        with cp.get_connection() as conn:
            result = conn.execute(query)
            return result

    threads = [threading.Thread(target=db_worker, args=(f"SELECT {i}",)) for i in range(5)]
    for t in threads: t.start()
    for t in threads: t.join()

    print(f"  Final stats: {cp.stats()}")
    cp.close_all()

    print("\n=== Buffer Pool ===")
    buf_pool = ObjectPool(lambda: ReusableBuffer(1024), max_size=5)

    with pooled_buffer(buf_pool) as buf:
        buf.write(b"Hello, ")
        buf.write(b"World!")
        print(f"  Buffer content: {buf.read()!r} ({len(buf)} bytes)")

    with pooled_buffer(buf_pool) as buf:
        # Buffer was reset
        print(f"  Reused buffer is empty: {len(buf) == 0}")
        buf.write(b"Next use!")
        print(f"  New content: {buf.read()!r}")
