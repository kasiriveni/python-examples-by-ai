"""
This script demonstrates a multi-agent system with an orchestrator and specialist agents.
Topics covered:
1. Orchestrator agent delegating tasks.
2. Specialist agents handling specific tasks.
"""

class SpecialistAgent:
    def __init__(self, name):
        self.name = name

    def handle_task(self, task):
        return f"{self.name} handled task: {task}"

class OrchestratorAgent:
    def __init__(self):
        self.agents = {}

    def register_agent(self, name, agent):
        self.agents[name] = agent

    def delegate_task(self, task, agent_name):
        if agent_name in self.agents:
            return self.agents[agent_name].handle_task(task)
        else:
            return f"No agent named {agent_name} found."

# Example usage
orchestrator = OrchestratorAgent()
agent1 = SpecialistAgent("Agent1")
agent2 = SpecialistAgent("Agent2")

orchestrator.register_agent("agent1", agent1)
orchestrator.register_agent("agent2", agent2)

print(orchestrator.delegate_task("Analyze data", "agent1"))
print(orchestrator.delegate_task("Generate report", "agent2"))
