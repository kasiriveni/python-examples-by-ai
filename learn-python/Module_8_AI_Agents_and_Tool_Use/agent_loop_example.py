# Example: AI Agent Loop
# Demonstrates a simple ReAct agent loop

from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI

# Define tools
def calculator_tool(input):
    return eval(input)

tools = [Tool(name="Calculator", func=calculator_tool)]

# Initialize the agent
llm = OpenAI(temperature=0)
agent = initialize_agent(tools, llm, agent="zero-shot-react-description")

# Run the agent
response = agent.run("What is 5 + 3?")
print(response)