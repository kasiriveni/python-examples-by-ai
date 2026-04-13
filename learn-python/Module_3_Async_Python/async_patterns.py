"""
Module 3: Async Python - asyncio, coroutines, and concurrent patterns.
"""
import asyncio
import time

# === Basic coroutines ===
async def say_hello(name, delay):
    await asyncio.sleep(delay)
    print(f"  Hello, {name}! (waited {delay}s)")

async def basic_demo():
    print("=== Basic Coroutines ===")
    # Sequential
    start = time.perf_counter()
    await say_hello("Alice", 0.1)
    await say_hello("Bob", 0.1)
    print(f"  Sequential: {time.perf_counter() - start:.2f}s")

    # Concurrent
    start = time.perf_counter()
    await asyncio.gather(
        say_hello("Alice", 0.1),
        say_hello("Bob", 0.1),
    )
    print(f"  Concurrent: {time.perf_counter() - start:.2f}s")

# === Async generators ===
async def async_range(start, stop, delay=0.01):
    for i in range(start, stop):
        await asyncio.sleep(delay)
        yield i

async def generator_demo():
    print("\n=== Async Generators ===")
    values = []
    async for val in async_range(0, 5):
        values.append(val)
    print(f"  Values: {values}")

# === Task management ===
async def fetch_data(url, delay):
    await asyncio.sleep(delay)
    return {"url": url, "status": 200, "data": f"Response from {url}"}

async def task_demo():
    print("\n=== Task Management ===")

    # Create tasks
    tasks = [
        asyncio.create_task(fetch_data("api/users", 0.1)),
        asyncio.create_task(fetch_data("api/posts", 0.15)),
        asyncio.create_task(fetch_data("api/comments", 0.05)),
    ]

    # Wait for all
    results = await asyncio.gather(*tasks)
    for r in results:
        print(f"  {r['url']}: {r['status']}")

    # as_completed - process results as they finish
    print("\n  As completed:")
    tasks = [
        asyncio.create_task(fetch_data("slow", 0.2)),
        asyncio.create_task(fetch_data("fast", 0.05)),
        asyncio.create_task(fetch_data("medium", 0.1)),
    ]
    for coro in asyncio.as_completed(tasks):
        result = await coro
        print(f"    Completed: {result['url']}")

# === Async context managers ===
class AsyncResource:
    def __init__(self, name):
        self.name = name

    async def __aenter__(self):
        print(f"  Acquiring {self.name}")
        await asyncio.sleep(0.01)
        return self

    async def __aexit__(self, *args):
        print(f"  Releasing {self.name}")
        await asyncio.sleep(0.01)

async def context_demo():
    print("\n=== Async Context Manager ===")
    async with AsyncResource("database") as db:
        print(f"  Using {db.name}")

# === Semaphore for concurrency control ===
async def limited_fetch(sem, url, delay):
    async with sem:
        await asyncio.sleep(delay)
        return f"Done: {url}"

async def semaphore_demo():
    print("\n=== Semaphore (max 2 concurrent) ===")
    sem = asyncio.Semaphore(2)
    start = time.perf_counter()
    results = await asyncio.gather(*[
        limited_fetch(sem, f"url_{i}", 0.1) for i in range(6)
    ])
    elapsed = time.perf_counter() - start
    print(f"  {len(results)} requests in {elapsed:.2f}s (limited to 2 concurrent)")

# === Event and Queue ===
async def producer(queue, n):
    for i in range(n):
        await asyncio.sleep(0.01)
        await queue.put(f"item_{i}")
    await queue.put(None)  # Sentinel

async def consumer(queue, name):
    while True:
        item = await queue.get()
        if item is None:
            queue.task_done()
            break
        print(f"  {name} processed {item}")
        queue.task_done()

async def queue_demo():
    print("\n=== Async Queue ===")
    queue = asyncio.Queue(maxsize=5)
    await asyncio.gather(
        producer(queue, 4),
        consumer(queue, "Worker"),
    )

# === Main ===
async def main():
    await basic_demo()
    await generator_demo()
    await task_demo()
    await context_demo()
    await semaphore_demo()
    await queue_demo()

if __name__ == "__main__":
    asyncio.run(main())
