"""Example runner for Module 3: Async Python"""
import asyncio


async def async_count(n):
    for i in range(1, n + 1):
        print("async step", i)
        await asyncio.sleep(0.05)


def main():
    print("Module 3 - Async example")
    asyncio.run(async_count(3))


if __name__ == "__main__":
    main()
