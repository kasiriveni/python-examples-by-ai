# Example: Async Generators and Async For
# Demonstrates how to use async generators and async for

import asyncio

async def async_generator():
    for i in range(5):
        await asyncio.sleep(1)
        yield i

async def main():
    async for value in async_generator():
        print(f"Received: {value}")

asyncio.run(main())
