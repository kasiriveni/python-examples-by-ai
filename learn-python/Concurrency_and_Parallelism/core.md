# Core Python Concepts

- Use threading for concurrent I/O-bound tasks that share memory.
- Use multiprocessing when CPU-bound work needs true parallel execution.
- Use `asyncio` for cooperative concurrency around many waiting operations.
- Coordinate workers with queues, locks, events, and semaphores when needed.
- Understand the tradeoffs between shared state, process isolation, and scheduling overhead.
- Choose the model that matches the workload instead of forcing one pattern everywhere.
