# Example: Asyncio Basics
# Demonstrates event loop, async def, and await

import asyncio

async def say_hello():
    print("Hello")
    await asyncio.sleep(1)
    print("World")

async def main():
    print("Starting...")
    await say_hello()
    print("Finished")

asyncio.run(main())