"""
This script demonstrates prompt versioning and management for LLMs.
Topics covered:
1. Storing and retrieving prompt versions.
2. Managing prompt metadata.
"""

import json

# Define a prompt versioning system
class PromptManager:
    def __init__(self):
        self.prompts = {}

    def add_prompt(self, version, prompt, metadata=None):
        self.prompts[version] = {"prompt": prompt, "metadata": metadata or {}}

    def get_prompt(self, version):
        return self.prompts.get(version, "Prompt version not found.")

# Example usage
manager = PromptManager()
manager.add_prompt("v1", "What is the capital of France?", {"author": "user1", "date": "2026-04-12"})
manager.add_prompt("v2", "Name the capital city of France.", {"author": "user2", "date": "2026-04-13"})

print(json.dumps(manager.get_prompt("v1"), indent=2))
print(json.dumps(manager.get_prompt("v2"), indent=2))
