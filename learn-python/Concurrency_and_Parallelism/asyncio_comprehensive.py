"""
Asyncio comprehensive examples.
"""
import asyncio
import time

# === Basic coroutine ===
async def hello():
    print("Hello...")
    await asyncio.sleep(1)
    print("...World!")

# === Running multiple tasks concurrently ===
async def fetch_data(name, delay):
    print(f"  [{name}] Starting (will take {delay}s)")
    await asyncio.sleep(delay)
    print(f"  [{name}] Done!")
    return f"{name}_result"

async def concurrent_tasks():
    print("=== Concurrent Tasks ===")
    start = time.perf_counter()

    results = await asyncio.gather(
        fetch_data("API", 2),
        fetch_data("DB", 1),
        fetch_data("Cache", 0.5),
    )

    elapsed = time.perf_counter() - start
    print(f"All done in {elapsed:.1f}s (not {2+1+0.5}s)")
    print(f"Results: {results}")

# === Task management ===
async def task_management():
    print("\n=== Task Management ===")

    async def worker(n):
        await asyncio.sleep(n * 0.1)
        return n * 10

    # Create tasks
    tasks = [asyncio.create_task(worker(i)) for i in range(5)]

    # Wait for all
    results = await asyncio.gather(*tasks)
    print(f"Results: {results}")

# === as_completed (process results as they arrive) ===
async def as_completed_example():
    print("\n=== as_completed ===")

    async def job(name, delay):
        await asyncio.sleep(delay)
        return f"{name} finished"

    tasks = [
        asyncio.create_task(job("Slow", 0.3)),
        asyncio.create_task(job("Fast", 0.1)),
        asyncio.create_task(job("Medium", 0.2)),
    ]

    for coro in asyncio.as_completed(tasks):
        result = await coro
        print(f"  Completed: {result}")

# === Timeout ===
async def timeout_example():
    print("\n=== Timeout ===")

    async def slow_operation():
        await asyncio.sleep(10)
        return "done"

    try:
        result = await asyncio.wait_for(slow_operation(), timeout=1.0)
    except asyncio.TimeoutError:
        print("  Operation timed out!")

# === Async generator ===
async def async_range(start, stop):
    for i in range(start, stop):
        await asyncio.sleep(0.1)
        yield i

async def async_generator_example():
    print("\n=== Async Generator ===")
    async for num in async_range(0, 5):
        print(f"  Got: {num}")

# === Async context manager ===
class AsyncResource:
    def __init__(self, name):
        self.name = name

    async def __aenter__(self):
        print(f"  Acquiring {self.name}")
        await asyncio.sleep(0.1)
        return self

    async def __aexit__(self, *args):
        print(f"  Releasing {self.name}")
        await asyncio.sleep(0.1)

async def async_context_example():
    print("\n=== Async Context Manager ===")
    async with AsyncResource("Database") as db:
        print(f"  Using {db.name}")

# === Semaphore (limit concurrency) ===
async def semaphore_example():
    print("\n=== Semaphore (max 2 concurrent) ===")
    sem = asyncio.Semaphore(2)

    async def limited_task(n):
        async with sem:
            print(f"  Task {n} running")
            await asyncio.sleep(0.5)
            print(f"  Task {n} done")

    await asyncio.gather(*[limited_task(i) for i in range(5)])

# === Queue ===
async def queue_example():
    print("\n=== Async Queue ===")
    queue = asyncio.Queue(maxsize=5)

    async def producer():
        for i in range(5):
            await queue.put(f"item-{i}")
            print(f"  Produced: item-{i}")

    async def consumer():
        while True:
            item = await queue.get()
            print(f"  Consumed: {item}")
            queue.task_done()

    producer_task = asyncio.create_task(producer())
    consumer_task = asyncio.create_task(consumer())

    await producer_task
    await queue.join()
    consumer_task.cancel()

# === Main ===
async def main():
    await hello()
    await concurrent_tasks()
    await task_management()
    await as_completed_example()
    await timeout_example()
    await async_generator_example()
    await async_context_example()
    await semaphore_example()
    await queue_example()

if __name__ == "__main__":
    asyncio.run(main())
