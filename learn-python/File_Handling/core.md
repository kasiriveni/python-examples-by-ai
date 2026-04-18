# Core Python Concepts

## Core Themes
- Text and binary file input and output.
- Working with JSON, CSV, and pathlib-based paths.
- Streaming, chunked reading, and filesystem patterns.

## Core Theme Examples
- Example 1: Reading text file with open() context manager.
- Example 2: JSON dump to file using pathlib.Path.
- Example 3: pathlib glob pattern to find matching files.

## Files and Concepts
- csv_files.py: CSV reading and writing, DictReader, DictWriter
- file_handling.py: text files, binary files, CSV, JSON, context managers
- file_patterns.py: pathlib paths, globbing, path parts, file and directory checks
- io_examples.py: file streaming, chunked reads, binary writes
- json_files.py: JSON serialization, pretty printing, custom encoders
- pathlib_examples.py: path construction, glob patterns, temporary directories, file creation
- reading_and_writing.py: full-file reads, line iteration, appending, binary operations

## Core Example
This example writes and reads a text file with a context manager and pathlib.

```python
from pathlib import Path

path = Path("notes.txt")
path.write_text("alpha\nbeta\n", encoding="utf-8")

with path.open("r", encoding="utf-8") as handle:
	lines = [line.strip() for line in handle]

print(lines)
```
