# Concurrency & Parallelism: threading, multiprocessing, asyncio
import threading
import multiprocessing
import asyncio

# threading
def tfunc():
    print('thread running')

thr = threading.Thread(target=tfunc)
thr.start()
thr.join()

# multiprocessing
def pfunc():
    print('process running')

p = multiprocessing.Process(target=pfunc)
p.start()
p.join()

# asyncio
async def async_main():
    print('async start')
    await asyncio.sleep(0.1)
    print('async end')

asyncio.run(async_main())
