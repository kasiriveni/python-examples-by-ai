# Core Python Concepts

## Core Themes
- Git fundamentals and local history operations.
- Branching, merging, and remote repository workflows.
- Team-oriented source-control conventions.

## Core Theme Examples
- Example 1: Using git add and git commit to track local history.
- Example 2: Creating feature branch, pushing to origin, merging via PR.
- Example 3: Following commit message conventions and branch naming standards.

## Files and Concepts
- GitHub_GitLab_Bitbucket.py: remote setup, push and pull, clone, revert, reset, rebase, tagging
- Git_Basics.py: git init, add, commit, status, history viewing
- Git_Branching_Merging.py: branch creation, checkout, merge, branch deletion

## Core Example
This example runs a simple git command and prints the output safely.

```python
import subprocess

result = subprocess.run(
	["git", "--version"],
	capture_output=True,
	text=True,
	check=False,
)

print(result.stdout.strip())
```
