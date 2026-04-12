# Example: asyncio.create_task()
# Demonstrates how to create and run multiple tasks concurrently

import asyncio

async def task(name, delay):
    print(f"Task {name} started")
    await asyncio.sleep(delay)
    print(f"Task {name} finished")

async def main():
    task1 = asyncio.create_task(task("A", 2))
    task2 = asyncio.create_task(task("B", 1))

    print("Waiting for tasks to complete...")
    await task1
    await task2
    print("All tasks completed")

asyncio.run(main())
