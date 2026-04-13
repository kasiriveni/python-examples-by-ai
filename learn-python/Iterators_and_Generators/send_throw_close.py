"""
Iterators and Generators: Coroutine send/throw/close and async iteration.
"""
import asyncio
from typing import Generator, AsyncIterator

# ═══════════════════════════════════════════
# 1. Generator .send() — two-way communication
# ═══════════════════════════════════════════
def echo_generator() -> Generator[str, str, str]:
    """Yields incoming values back to the caller."""
    received = yield "ready"
    while received is not None:
        received = yield f"echo: {received!r}"
    return "done"

def counter_coro(start: int = 0, step: int = 1):
    """Generator that accepts new step values via .send()."""
    count = start
    while True:
        new_step = yield count
        count += step if new_step is None else new_step

print("=== send() ===")
gen = echo_generator()
first = next(gen)       # prime the generator
print(f"Initial: {first!r}")
for msg in ["hello", "world", "42"]:
    reply = gen.send(msg)
    print(f"sent {msg!r} → {reply!r}")

print("\n=== counter with dynamic step ===")
c = counter_coro(10, 5)
print(next(c), next(c), next(c))     # 10, 15, 20
print(c.send(100))                    # jump by 100 → 120
print(next(c), next(c))              # 125, 130

# ═══════════════════════════════════════════
# 2. Generator .throw() — inject exceptions
# ═══════════════════════════════════════════
def resilient_generator():
    """Generator that handles injected exceptions."""
    while True:
        try:
            value = yield
        except ValueError as e:
            yield f"handled ValueError: {e}"
        except RuntimeError as e:
            yield f"handled RuntimeError: {e}"

print("\n=== throw() ===")
rg = resilient_generator()
next(rg)       # prime
result = rg.throw(ValueError, "bad input")
print(f"throw ValueError → {result!r}")
next(rg)      # move past the yield in the except block
result = rg.throw(RuntimeError, "unexpected state")
print(f"throw RuntimeError → {result!r}")

# ═══════════════════════════════════════════
# 3. Generator .close() — GeneratorExit
# ═══════════════════════════════════════════
def resource_generator():
    print("  [resource] opened")
    try:
        for i in range(1000):
            yield i
    except GeneratorExit:
        print("  [resource] GeneratorExit caught — cleaning up")
    finally:
        print("  [resource] closed (finally)")

print("\n=== close() ===")
gen = resource_generator()
for val in itertools.islice(gen, 3):
    print(f"  got {val}")
gen.close()   # sends GeneratorExit
print("  after close()")

import itertools

# ═══════════════════════════════════════════
# 4. yield from — delegation
# ═══════════════════════════════════════════
def inner():
    print("  [inner] start")
    a = yield "inner-1"
    print(f"  [inner] received: {a!r}")
    b = yield "inner-2"
    print(f"  [inner] received: {b!r}")
    return "inner-return"

def outer():
    print("  [outer] before delegation")
    result = yield from inner()   # transparent delegation
    print(f"  [outer] inner returned: {result!r}")
    yield "outer-final"

print("\n=== yield from (delegation) ===")
gen = outer()
print(next(gen))             # inner-1
print(gen.send("A"))         # inner-2
print(gen.send("B"))         # outer-final after inner returns

# ═══════════════════════════════════════════
# 5. Async generators
# ═══════════════════════════════════════════
async def async_count(start: int, stop: int, delay: float = 0.01) -> AsyncIterator[int]:
    for i in range(start, stop):
        await asyncio.sleep(delay)
        yield i

async def async_take(n: int, agen) -> list:
    result = []
    async for item in agen:
        result.append(item)
        if len(result) >= n:
            break
    return result

async def async_filter(pred, agen) -> AsyncIterator:
    async for item in agen:
        if pred(item):
            yield item

async def async_map(fn, agen) -> AsyncIterator:
    async for item in agen:
        yield fn(item)

async def pipeline_demo():
    print("\n=== Async Generator Pipeline ===")

    # Lazy async pipeline
    source  = async_count(0, 100, delay=0)
    evens   = async_filter(lambda x: x % 2 == 0, source)
    squared = async_map(lambda x: x**2, evens)

    result = await async_take(10, squared)
    print(f"  First 10 even squares: {result}")

    # Async comprehension
    squares = [x async for x in async_count(1, 6, delay=0)]
    print(f"  Async listcomp 1-5: {squares}")

    # aiter / anext (Python 3.10+)
    gen = async_count(10, 20, delay=0)
    first = await anext(gen)
    second = await anext(gen)
    print(f"  First two from async_count(10): {first}, {second}")

# ═══════════════════════════════════════════
# 6. Async context manager with async generator
# ═══════════════════════════════════════════
import contextlib

@contextlib.asynccontextmanager
async def async_timer(name: str):
    import time
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = (time.perf_counter() - start) * 1000
        print(f"  [{name}] {elapsed:.2f}ms")

async def main():
    await pipeline_demo()

    print("\n=== Async Context Manager ===")
    async with async_timer("async work"):
        result = [x async for x in async_count(0, 50, delay=0)]
    print(f"  Got {len(result)} items")

if __name__ == "__main__":
    asyncio.run(main())
