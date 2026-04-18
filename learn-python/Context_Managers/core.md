# Core Python Concepts

## Core Themes
- Resource acquisition and cleanup around with blocks.
- Custom synchronous and asynchronous context managers.
- Transactions, file locks, and pooled resources.

## Core Theme Examples
- Example 1: File-context manager with open() for automatic resource cleanup.
- Example 2: Custom context manager class with __enter__ returning resource and __exit__ closing.
- Example 3: Database transaction savepoint or thread-safe resource pool acquire/release.

## Files and Concepts
- async_context_managers.py: async enter and exit methods, async with, async resource cleanup
- context_managers.py: contextmanager decorator, try and finally, class-based managers
- context_managers_comprehensive.py: file managers, timers, temporary workspaces, transaction patterns
- database_transactions.py: SQLite transaction managers, savepoints, pooled connections
- file_locking_and_utils.py: exception suppression, stdout redirection, temporary files, file-lock helpers
- resource_pools.py: generic object pools, thread-safe acquire and release, factory-based resource creation

## Core Example
This example implements a small context manager for temporary messages.

```python
class MessageContext:
	def __enter__(self):
		print("opening")
		return "resource"

	def __exit__(self, exc_type, exc, traceback):
		print("closing")

with MessageContext() as resource:
	print(resource)
```
