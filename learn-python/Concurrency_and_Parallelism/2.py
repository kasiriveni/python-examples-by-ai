


# asynchronous programming
import asyncio
async def main():
    print('Hello ...')
    await asyncio.sleep(1)
    print('... World!')

asyncio.run(main())


# want iterateo 100 times
for i in range(100):
    print(i)
