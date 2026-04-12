"""
This script demonstrates human-in-the-loop patterns for agent workflows.
Topics covered:
1. Integrating human feedback into agent decision-making.
2. Allowing humans to override agent actions.
"""

class HumanInTheLoopAgent:
    def __init__(self):
        self.memory = []

    def propose_action(self, observation):
        if "error" in observation:
            return "debug"
        elif "task" in observation:
            return "execute_task"
        else:
            return "explore"

    def act(self, action):
        return f"Agent proposes to: {action}"

    def human_override(self, proposed_action, human_feedback):
        if human_feedback:
            return f"Human overrides to: {human_feedback}"
        return f"Action confirmed: {proposed_action}"

# Example usage
agent = HumanInTheLoopAgent()
observation = "task received"
proposed_action = agent.propose_action(observation)
print(agent.act(proposed_action))

# Human feedback
human_feedback = "review_task"
print(agent.human_override(proposed_action, human_feedback))
