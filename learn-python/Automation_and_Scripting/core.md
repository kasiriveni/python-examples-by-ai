# Core Python Concepts

## Core Themes
- Command-line tooling and subprocess automation.
- Filesystem operations, retries, and scheduled task patterns.
- Text processing, regex, and basic web scraping.

## Core Theme Examples
- Example 1: Run CLI commands with subprocess and argparse parsing.
- Example 2: Create and traverse directory structures with retry logic.
- Example 3: Extract and normalize text with regex patterns.

## Files and Concepts
- cli_and_subprocess.py: argparse-based CLIs, subprocess execution, deployment scripting
- cli_arguments.py: argument parsing, subcommands, positional and optional arguments
- file_system_automation.py: directory traversal, globbing, tree visualization
- task_automation.py: task scheduling, retry decorators, exponential backoff
- text_processing.py: regex parsing, log filtering, text normalization
- web_scraping_basics.py: HTML parsing, link extraction, urlopen-based scraping

## Core Example
This example uses pathlib and subprocess to automate a small task.

```python
from pathlib import Path
import subprocess

log_file = Path("example.log")
log_file.write_text("done\n", encoding="utf-8")

result = subprocess.run(["python", "--version"], capture_output=True, text=True)
print(log_file.read_text(encoding="utf-8").strip())
print(result.stdout.strip() or result.stderr.strip())
```
