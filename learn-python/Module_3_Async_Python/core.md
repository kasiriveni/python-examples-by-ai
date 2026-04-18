# Core Python Concepts

## Core Themes
- Asyncio primitives and coroutine workflows.
- Async HTTP, streaming, generators, and context managers.
- Connections between async code, threads, and processes.

## Core Theme Examples
- Example 1: Running concurrent coroutines with asyncio.gather.
- Example 2: Concurrent HTTP requests with aiohttp.
- Example 3: Comparing async versus threading execution models.

## Files and Concepts
- asyncio_basics.py: event loop, async def, await, coroutine basics
- asyncio_create_task.py: task creation, concurrent execution, awaiting tasks
- asyncio_gather.py: running many tasks concurrently with gather
- async_context_managers.py: async enter and exit methods, async with
- async_generators.py: async generators, async for iteration
- async_http_calls.py: aiohttp sessions, concurrent HTTP requests
- async_patterns.py: async generators, coroutine patterns, concurrent flows
- concurrent_futures_example.py: ThreadPoolExecutor, Future objects, executor mapping
- httpx_example.py: HTTPX async client, async context management, concurrent fetches
- multiprocessing_example.py: process creation, spawned workers, process IDs
- streaming_responses.py: streamed content, async chunk iteration
- threading_example.py: thread basics and joins alongside async comparisons

## Core Example
This example runs two coroutines concurrently with asyncio.

```python
import asyncio

async def fetch(name, delay):
	await asyncio.sleep(delay)
	return f"done:{name}"

async def main():
	results = await asyncio.gather(fetch("a", 0.1), fetch("b", 0.1))
	print(results)

asyncio.run(main())
```
