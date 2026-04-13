"""
Context Managers: Async context managers and async with patterns.
"""
import asyncio
import time
from contextlib import asynccontextmanager, AsyncExitStack
from typing import AsyncIterator

# ═══════════════════════════════════════════
# 1. Class-based async context manager
# ═══════════════════════════════════════════
class AsyncTimer:
    """Measures execution time of an async block."""

    def __init__(self, name: str = "block"):
        self.name = name
        self._start: float = 0

    async def __aenter__(self):
        self._start = time.perf_counter()
        print(f"[{self.name}] Starting...")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        elapsed = time.perf_counter() - self._start
        status = "ERROR" if exc_type else "OK"
        print(f"[{self.name}] Done in {elapsed:.3f}s [{status}]")
        return False  # don't suppress exceptions

class AsyncDatabase:
    """Simulated async database connection."""

    def __init__(self, url: str):
        self.url = url
        self._connected = False

    async def __aenter__(self):
        await asyncio.sleep(0.01)  # simulate connect latency
        self._connected = True
        print(f"  DB connected: {self.url}")
        return self

    async def __aexit__(self, *args):
        await asyncio.sleep(0.002)  # simulate close
        self._connected = False
        print(f"  DB disconnected: {self.url}")

    async def query(self, sql: str) -> list[dict]:
        if not self._connected:
            raise RuntimeError("Not connected")
        await asyncio.sleep(0.005)  # simulate query
        return [{"id": 1, "sql": sql}]

# ═══════════════════════════════════════════
# 2. @asynccontextmanager decorator
# ═══════════════════════════════════════════
@asynccontextmanager
async def managed_resource(name: str) -> AsyncIterator[dict]:
    """Acquire and release a resource using generator syntax."""
    resource = {"name": name, "data": [], "active": True}
    print(f"  Acquired: {name}")
    try:
        yield resource
    except Exception as e:
        print(f"  Error in {name}: {e}")
        raise
    finally:
        resource["active"] = False
        print(f"  Released: {name}")

@asynccontextmanager
async def rate_limiter(calls_per_sec: float) -> AsyncIterator[None]:
    """Async rate limiter context."""
    min_interval = 1.0 / calls_per_sec
    last_call = [0.0]

    async def throttle():
        elapsed = time.perf_counter() - last_call[0]
        wait = min_interval - elapsed
        if wait > 0:
            await asyncio.sleep(wait)
        last_call[0] = time.perf_counter()

    # Inject throttle into a simple namespace
    class Throttler:
        async def __call__(self): await throttle()

    yield Throttler()

# ═══════════════════════════════════════════
# 3. AsyncExitStack
# ═══════════════════════════════════════════
async def open_multiple_connections(urls: list[str]):
    """Open several DB connections, cleaning up all on exit."""
    dbs = []
    async with AsyncExitStack() as stack:
        for url in urls:
            db = await stack.enter_async_context(AsyncDatabase(url))
            dbs.append(db)
        # All connections available here
        print(f"  All {len(dbs)} connections open")
        results = await asyncio.gather(*[db.query("SELECT 1") for db in dbs])
    # All connections closed
    print(f"  Got {len(results)} result sets")
    return results

# ═══════════════════════════════════════════
# 4. Context manager for transaction
# ═══════════════════════════════════════════
@asynccontextmanager
async def transaction(db: AsyncDatabase):
    """Wraps DB operations in a transaction."""
    await asyncio.sleep(0.002)  # BEGIN
    print("  BEGIN TRANSACTION")
    try:
        yield db
        await asyncio.sleep(0.002)  # COMMIT
        print("  COMMIT")
    except Exception:
        await asyncio.sleep(0.001)  # ROLLBACK
        print("  ROLLBACK")
        raise

# ═══════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════
async def main():
    print("=== Async Timer ===")
    async with AsyncTimer("computation"):
        await asyncio.sleep(0.05)
        print("  Working...")

    print("\n=== Async Database ===")
    async with AsyncDatabase("postgresql://localhost/app") as db:
        rows = await db.query("SELECT * FROM users LIMIT 5")
        print(f"  Rows: {rows}")

    print("\n=== @asynccontextmanager ===")
    async with managed_resource("cache") as cache:
        cache["data"].append("item1")
        print(f"  Cache active: {cache['active']}, items: {cache['data']}")
    print(f"  Cache after: active={cache['active']}")

    print("\n=== AsyncExitStack ===")
    await open_multiple_connections([
        "db://host/db1", "db://host/db2", "db://host/db3"
    ])

    print("\n=== Transaction ===")
    async with AsyncDatabase("db://host/app") as db:
        async with transaction(db):
            result = await db.query("INSERT INTO users VALUES (1, 'Alice')")
            print(f"  Insert result: {result}")

    print("\n=== Rate Limiter ===")
    async with rate_limiter(calls_per_sec=10) as throttle:
        for i in range(3):
            await throttle()
            print(f"  Call {i+1} at {time.perf_counter():.3f}s")

if __name__ == "__main__":
    asyncio.run(main())
