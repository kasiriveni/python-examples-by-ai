"""
This script demonstrates the use of LangGraph for stateful agent workflows.
Topics covered:
1. Defining states and transitions.
2. Stateful workflows for agents.
"""

class LangGraph:
    def __init__(self):
        self.state = "start"
        self.transitions = {
            "start": "process",
            "process": "end",
            "end": None
        }

    def next_state(self):
        if self.state in self.transitions:
            self.state = self.transitions[self.state]
        return self.state

# Example usage
workflow = LangGraph()

print("Initial State:", workflow.state)
while workflow.state:
    print("Transitioning to:", workflow.next_state())
