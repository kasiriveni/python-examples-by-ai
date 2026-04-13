"""
Advanced Python: Coroutines, async/await, and asyncio patterns.
"""
import asyncio
import time
import random
from dataclasses import dataclass
from typing import AsyncIterator, AsyncGenerator

# ═══════════════════════════════════════════
# 1. Basic async/await
# ═══════════════════════════════════════════
async def fetch_page(url: str, delay: float) -> str:
    """Simulate an async HTTP GET."""
    await asyncio.sleep(delay)
    return f"<html>{url} — {delay:.1f}s</html>"

async def demo_basic():
    print("=== Basic async/await ===")
    # Sequential (slow — adds up delays)
    start = time.monotonic()
    r1 = await fetch_page("https://example.com", 0.1)
    r2 = await fetch_page("https://python.org",  0.1)
    elapsed = time.monotonic() - start
    print(f"  Sequential: {elapsed:.2f}s")

    # Concurrent with gather (fast — parallel)
    start = time.monotonic()
    r1, r2, r3 = await asyncio.gather(
        fetch_page("https://a.com", 0.1),
        fetch_page("https://b.com", 0.1),
        fetch_page("https://c.com", 0.1),
    )
    elapsed = time.monotonic() - start
    print(f"  Concurrent (gather): {elapsed:.2f}s — {r1[:20]!r}")

# ═══════════════════════════════════════════
# 2. Tasks and cancellation
# ═══════════════════════════════════════════
async def long_running(name: str, seconds: float):
    print(f"  [{name}] starting")
    try:
        await asyncio.sleep(seconds)
        print(f"  [{name}] done after {seconds}s")
        return f"{name}=ok"
    except asyncio.CancelledError:
        print(f"  [{name}] CANCELLED")
        raise

async def demo_tasks():
    print("\n=== Tasks and Cancellation ===")
    t1 = asyncio.create_task(long_running("alpha", 0.2), name="alpha")
    t2 = asyncio.create_task(long_running("beta",  2.0), name="beta")
    t3 = asyncio.create_task(long_running("gamma", 0.1), name="gamma")

    await asyncio.sleep(0.15)
    t2.cancel()          # cancel before it finishes

    results = await asyncio.gather(t1, t2, t3, return_exceptions=True)
    for name, res in zip(["alpha", "beta", "gamma"], results):
        if isinstance(res, BaseException):
            print(f"  {name}: {type(res).__name__}")
        else:
            print(f"  {name}: {res!r}")

# ═══════════════════════════════════════════
# 3. wait_for with timeout
# ═══════════════════════════════════════════
async def demo_timeout():
    print("\n=== wait_for (timeout) ===")
    try:
        result = await asyncio.wait_for(long_running("slow", 1.0), timeout=0.1)
    except asyncio.TimeoutError:
        print("  Timed out as expected!")

# ═══════════════════════════════════════════
# 4. Async generators
# ═══════════════════════════════════════════
async def async_range(start: int, stop: int, step: int = 1, delay: float = 0.0) -> AsyncGenerator[int, None]:
    n = start
    while n < stop:
        if delay: await asyncio.sleep(delay)
        yield n
        n += step

async def paginate(total: int, page_size: int = 5) -> AsyncGenerator[list[int], None]:
    """Simulate paginated API responses."""
    for offset in range(0, total, page_size):
        await asyncio.sleep(0.01)  # simulate network
        page = list(range(offset, min(offset + page_size, total)))
        yield page

async def demo_async_generators():
    print("\n=== Async Generators ===")
    squares = [x**2 async for x in async_range(0, 6)]
    print(f"  Squares: {squares}")

    all_items: list[int] = []
    async for page in paginate(18, 5):
        print(f"  Page: {page}")
        all_items.extend(page)
    print(f"  Total items fetched: {len(all_items)}")

# ═══════════════════════════════════════════
# 5. Semaphore — limit concurrency
# ═══════════════════════════════════════════
async def download(url: str, sem: asyncio.Semaphore, delay: float) -> str:
    async with sem:
        await asyncio.sleep(delay)
        return f"downloaded {url}"

async def demo_semaphore():
    print("\n=== Semaphore (max 3 concurrent) ===")
    sem = asyncio.Semaphore(3)
    urls = [f"https://cdn.example.com/file{i}.zip" for i in range(8)]
    delays = [random.uniform(0.05, 0.15) for _ in urls]

    start = time.monotonic()
    tasks = [download(url, sem, d) for url, d in zip(urls, delays)]
    results = await asyncio.gather(*tasks)
    elapsed = time.monotonic() - start
    print(f"  Downloaded {len(results)} files in {elapsed:.2f}s (max 3 concurrent)")

# ═══════════════════════════════════════════
# 6. Queue-based producer/consumer
# ═══════════════════════════════════════════
async def producer(queue: asyncio.Queue, n: int):
    for i in range(n):
        item = f"item_{i}"
        await queue.put(item)
        print(f"  Producer: pushed {item!r} (qsize={queue.qsize()})")
        await asyncio.sleep(0.02)
    await queue.put(None)           # sentinel

async def consumer(queue: asyncio.Queue, name: str, results: list):
    processed = 0
    while True:
        item = await queue.get()
        if item is None:
            await queue.put(None)   # re-post sentinel for other consumers
            break
        await asyncio.sleep(0.03)  # simulate work
        processed += 1
        results.append(f"{name}: {item}")
        queue.task_done()
    print(f"  Consumer {name}: processed {processed} items")

async def demo_producer_consumer():
    print("\n=== Producer / Consumer ===")
    queue: asyncio.Queue[str | None] = asyncio.Queue(maxsize=3)
    results: list[str] = []
    await asyncio.gather(
        producer(queue, 6),
        consumer(queue, "C1", results),
    )
    print(f"  Results: {results}")

# ═══════════════════════════════════════════
# 7. Async context manager and class
# ═══════════════════════════════════════════
class AsyncDatabase:
    def __init__(self, dsn: str):
        self._dsn = dsn
        self._connected = False

    async def __aenter__(self):
        await asyncio.sleep(0.01)  # simulate connect
        self._connected = True
        print(f"  [DB] Connected to {self._dsn}")
        return self

    async def __aexit__(self, *_):
        await asyncio.sleep(0.005)
        self._connected = False
        print("  [DB] Connection closed")

    async def query(self, sql: str) -> list[dict]:
        if not self._connected:
            raise RuntimeError("Not connected")
        await asyncio.sleep(0.01)
        return [{"col": sql[:20]}]

async def demo_async_cm():
    print("\n=== Async Context Manager ===")
    async with AsyncDatabase("postgresql://localhost/mydb") as db:
        rows = await db.query("SELECT * FROM users LIMIT 10")
        print(f"  Rows: {rows}")

# ═══════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════
async def main():
    await demo_basic()
    await demo_tasks()
    await demo_timeout()
    await demo_async_generators()
    await demo_semaphore()
    await demo_producer_consumer()
    await demo_async_cm()

if __name__ == "__main__":
    asyncio.run(main())
