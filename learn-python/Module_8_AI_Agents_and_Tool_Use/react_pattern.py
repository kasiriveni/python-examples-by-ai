"""
This script demonstrates the ReAct pattern (Reasoning + Acting) for an agent loop.
Topics covered:
1. Plan → Act → Observe → Repeat loop.
2. Integration of reasoning and acting in decision-making.
"""

class ReActAgent:
    def __init__(self):
        self.memory = []

    def plan(self, observation):
        # Reasoning based on observation and memory
        if "error" in observation:
            return "debug"
        elif "task" in observation:
            return "execute_task"
        else:
            return "explore"

    def act(self, action):
        # Acting based on the plan
        if action == "debug":
            return "Attempting to debug the issue."
        elif action == "execute_task":
            return "Executing the assigned task."
        elif action == "explore":
            return "Exploring new possibilities."

    def observe(self, result):
        # Observing the result and updating memory
        self.memory.append(result)
        return f"Observed: {result}"

    def loop(self, observation):
        action = self.plan(observation)
        result = self.act(action)
        observation = self.observe(result)
        return observation

# Example usage
agent = ReActAgent()
observation = "task received"
for _ in range(3):
    print(agent.loop(observation))
