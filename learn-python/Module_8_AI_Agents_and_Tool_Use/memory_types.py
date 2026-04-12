"""
This script demonstrates different memory types for agents.
Topics covered:
1. In-context memory.
2. External (vector) memory.
3. Episodic memory.
"""

class AgentMemory:
    def __init__(self):
        self.in_context_memory = []  # Temporary memory for current session
        self.external_memory = {}  # Persistent memory (e.g., vector database)
        self.episodic_memory = []  # Memory of past events

    def add_to_in_context(self, data):
        self.in_context_memory.append(data)

    def add_to_external(self, key, vector):
        self.external_memory[key] = vector

    def add_to_episodic(self, event):
        self.episodic_memory.append(event)

    def retrieve_from_external(self, key):
        return self.external_memory.get(key, "Not found")

# Example usage
agent_memory = AgentMemory()

# In-context memory
agent_memory.add_to_in_context("Current task: Analyze data")
print("In-context Memory:", agent_memory.in_context_memory)

# External memory
agent_memory.add_to_external("task1", [0.1, 0.2, 0.3])
print("External Memory:", agent_memory.retrieve_from_external("task1"))

# Episodic memory
agent_memory.add_to_episodic("Completed task: Analyze data")
print("Episodic Memory:", agent_memory.episodic_memory)
