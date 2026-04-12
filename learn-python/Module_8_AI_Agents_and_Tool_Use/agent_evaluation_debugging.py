"""
This script demonstrates agent evaluation and debugging.
Topics covered:
1. Logging agent actions and decisions.
2. Evaluating agent performance.
"""

class DebuggableAgent:
    def __init__(self):
        self.log = []

    def decide(self, observation):
        if "error" in observation:
            decision = "debug"
        elif "task" in observation:
            decision = "execute_task"
        else:
            decision = "explore"
        self.log_action(observation, decision)
        return decision

    def log_action(self, observation, decision):
        self.log.append({"observation": observation, "decision": decision})

    def evaluate(self):
        return f"Log: {self.log}"

# Example usage
agent = DebuggableAgent()
agent.decide("task received")
agent.decide("error encountered")
agent.decide("idle state")

print(agent.evaluate())
