# Core Python Concepts

## Core Themes
- Threading, multiprocessing, and asyncio concurrency models.
- Comparing CPU-bound, I O-bound, and cooperative execution.
- Synchronization, executors, and task orchestration basics.

## Core Theme Examples
- Example 1: Spawning worker threads with Thread and join.
- Example 2: CPU-bound tasks with Process and multiprocessing pools.
- Example 3: Task synchronization using locks and ThreadPoolExecutor.

## Files and Concepts
- 1.py: asyncio coroutines, await, event-loop basics
- 2.py: asyncio tasks, sleeping, iterative async flow
- 3.py: multiprocessing, process spawning, process IDs
- asyncio_comprehensive.py: coroutines, gather, concurrent tasks, task management
- asyncio_example.py: producer-consumer patterns, gather, asyncio queues
- concurrency_examples.py: threading, multiprocessing, asyncio comparison
- multiprocessing_example.py: process pools, parallel execution
- threading_comprehensive.py: threads, locks, thread safety, ThreadPoolExecutor
- threading_example.py: thread creation, worker targets, join

## Core Example
This example starts a few threads and waits for them to finish.

```python
import threading

def worker(name):
	print(f"working:{name}")

threads = [threading.Thread(target=worker, args=(index,)) for index in range(3)]
for thread in threads:
	thread.start()
for thread in threads:
	thread.join()
```
