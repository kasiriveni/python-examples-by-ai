# Core Python Concepts

## Core Themes
- Debugging workflows and runtime inspection techniques.
- Logging configuration, structured logging, and tracing.
- Profiling and performance-oriented troubleshooting.

## Core Theme Examples
- Example 1: Using pdb breakpoint() in exception handlers.
- Example 2: Setting up logger with handlers and formatters for structured output.
- Example 3: Running cProfile to identify performance bottlenecks.

## Files and Concepts
- debugging_profiling.py: pdb debugging, cProfile profiling, logging setup
- debugging_strategies.py: exception inspection, traceback formatting, warnings, debug context managers
- debugging_techniques.py: print debugging, logging levels, traceback reading, assertions, introspection
- logging_comprehensive.py: basicConfig, handlers, filters, LoggerAdapter context, exception logging
- structured_logging.py: JSON logs, contextual fields, decorators for tracing, duration measurement

## Core Example
This example logs a value before and after a calculation.

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def square(value):
	logger.info("input=%s", value)
	result = value * value
	logger.info("result=%s", result)
	return result

square(5)
```
