# Asyncio Example
import asyncio

async def say_hello():
    print("Hello")
    await asyncio.sleep(1)
    print("World")

async def main():
    await asyncio.gather(say_hello(), say_hello())

asyncio.run(main())

# Producer-Consumer Example
import asyncio

async def producer(queue):
    for i in range(5):
        await asyncio.sleep(1)
        item = f"item-{i}"
        await queue.put(item)
        print(f"Produced: {item}")

async def consumer(queue):
    while True:
        item = await queue.get()
        if item is None:
            break
        print(f"Consumed: {item}")
        await asyncio.sleep(2)

async def main():
    queue = asyncio.Queue()
    producer_task = asyncio.create_task(producer(queue))
    consumer_task = asyncio.create_task(consumer(queue))

    await producer_task
    await queue.put(None)  # Signal the consumer to exit
    await consumer_task

asyncio.run(main())
