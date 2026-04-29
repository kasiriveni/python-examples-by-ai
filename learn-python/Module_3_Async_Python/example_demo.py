"""Async demo: simple producer/consumer with asyncio.Queue"""
import asyncio


async def producer(q):
    for i in range(3):
        await q.put(i)
        print("produced", i)
        await asyncio.sleep(0.02)
    await q.put(None)


async def consumer(q):
    while True:
        item = await q.get()
        if item is None:
            break
        print("consumed", item)


async def main_async():
    q = asyncio.Queue()
    await asyncio.gather(producer(q), consumer(q))


def main():
    print("Async demo")
    asyncio.run(main_async())


if __name__ == '__main__':
    main()
