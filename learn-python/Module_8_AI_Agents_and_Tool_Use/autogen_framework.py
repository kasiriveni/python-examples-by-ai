"""
This script demonstrates the use of AutoGen for multi-agent frameworks.
Topics covered:
1. Creating multiple agents.
2. Collaboration between agents.
"""

class AutoGenAgent:
    def __init__(self, name):
        self.name = name

    def collaborate(self, task):
        return f"{self.name} is collaborating on task: {task}"

# Example usage
agent1 = AutoGenAgent("Agent1")
agent2 = AutoGenAgent("Agent2")

print(agent1.collaborate("Data Analysis"))
print(agent2.collaborate("Report Generation"))
