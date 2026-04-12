# Example: Async Context Managers
# Demonstrates how to use async context managers

import asyncio

class AsyncContextManager:
    async def __aenter__(self):
        print("Entering async context")
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        print("Exiting async context")

async def main():
    async with AsyncContextManager() as manager:
        print("Inside async context")

asyncio.run(main())
