# Core Python Concepts

## Core Themes
- Standard and third-party logging libraries.
- Structured log formatting and persistent log sinks.
- Error tracking and rotation-oriented logging setups.

## Core Theme Examples
- Example 1: Configuring logging.basicConfig with level filters.
- Example 2: Writing JSON logs to file with RotatingFileHandler.
- Example 3: Setting up Sentry SDK for exception tracking.

## Files and Concepts
- Logging_Module.py: basicConfig, logging levels, log formatting
- Loguru.py: Loguru sinks, rotation, retention policies
- Sentry.py: Sentry SDK setup, exception capture, external error tracking
- structured_logging.py: JSON formatting, extra fields, rotating handlers

## Core Example
This example configures a simple logger with a readable format.

```python
import logging

logging.basicConfig(
	level=logging.INFO,
	format="%(levelname)s:%(name)s:%(message)s",
)

logger = logging.getLogger("demo")
logger.info("application started")
```
