"""
Module 8: AI Agents and Tool Use patterns.
"""
import json
from dataclasses import dataclass, field
from typing import Callable, Any
from datetime import datetime

# === Tool Definition ===
@dataclass
class Tool:
    name: str
    description: str
    parameters: dict
    function: Callable

    def to_schema(self):
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            }
        }

# === Define Tools ===
def calculator(expression: str) -> str:
    """Safely evaluate a math expression."""
    allowed = set('0123456789+-*/.() ')
    if not all(c in allowed for c in expression):
        return "Error: Invalid characters in expression"
    try:
        result = eval(expression)  # In production, use a proper math parser
        return str(result)
    except Exception as e:
        return f"Error: {e}"

def get_current_time() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def search_knowledge_base(query: str) -> str:
    knowledge = {
        "python": "Python is a high-level programming language created by Guido van Rossum.",
        "flask": "Flask is a lightweight WSGI web application framework.",
        "fastapi": "FastAPI is a modern web framework for building APIs with Python 3.7+.",
    }
    query_lower = query.lower()
    results = [v for k, v in knowledge.items() if k in query_lower]
    return results[0] if results else f"No results found for: {query}"

# Create tool registry
TOOLS = {
    "calculator": Tool(
        name="calculator",
        description="Evaluate a mathematical expression",
        parameters={
            "type": "object",
            "properties": {"expression": {"type": "string", "description": "Math expression"}},
            "required": ["expression"],
        },
        function=calculator,
    ),
    "get_current_time": Tool(
        name="get_current_time",
        description="Get the current date and time",
        parameters={"type": "object", "properties": {}},
        function=get_current_time,
    ),
    "search": Tool(
        name="search",
        description="Search the knowledge base",
        parameters={
            "type": "object",
            "properties": {"query": {"type": "string", "description": "Search query"}},
            "required": ["query"],
        },
        function=search_knowledge_base,
    ),
}

# === Agent ===
@dataclass
class AgentMessage:
    role: str
    content: str
    tool_calls: list = field(default_factory=list)
    tool_results: list = field(default_factory=list)

class SimpleAgent:
    def __init__(self, tools: dict[str, Tool], max_iterations=5):
        self.tools = tools
        self.max_iterations = max_iterations
        self.conversation = []

    def execute_tool(self, tool_name, arguments):
        if tool_name not in self.tools:
            return f"Error: Unknown tool '{tool_name}'"
        tool = self.tools[tool_name]
        try:
            result = tool.function(**arguments)
            return result
        except Exception as e:
            return f"Error: {e}"

    def process_query(self, query):
        """Simple agent loop: analyze query -> decide tool -> execute -> respond."""
        print(f"\n[Agent] Processing: {query}")
        self.conversation.append(AgentMessage("user", query))

        # Simple keyword-based tool selection (in production, LLM decides)
        tool_name, args = self._select_tool(query)

        if tool_name:
            print(f"[Agent] Using tool: {tool_name}({args})")
            result = self.execute_tool(tool_name, args)
            print(f"[Agent] Tool result: {result}")

            response = f"Based on using the {tool_name} tool: {result}"
        else:
            response = f"I'll try to answer directly: {query}"

        self.conversation.append(AgentMessage("assistant", response))
        return response

    def _select_tool(self, query):
        """Simple heuristic tool selection."""
        query_lower = query.lower()

        if any(op in query for op in ['+', '-', '*', '/', 'calculate', 'compute']):
            # Extract expression
            import re
            expr = re.findall(r'[\d+\-*/().]+', query)
            if expr:
                return "calculator", {"expression": expr[0]}

        if any(w in query_lower for w in ['time', 'date', 'now']):
            return "get_current_time", {}

        if any(w in query_lower for w in ['what is', 'search', 'find', 'tell me about']):
            return "search", {"query": query}

        return None, {}

# === ReAct Pattern (Reasoning + Acting) ===
class ReActAgent(SimpleAgent):
    def process_query(self, query):
        print(f"\n{'='*50}")
        print(f"[ReAct] Query: {query}")

        for step in range(self.max_iterations):
            # Think
            thought = f"Step {step + 1}: Analyzing '{query}'"
            print(f"[Think] {thought}")

            # Act
            tool_name, args = self._select_tool(query)
            if tool_name:
                print(f"[Act] {tool_name}({args})")
                result = self.execute_tool(tool_name, args)
                print(f"[Observe] {result}")

                # Check if we have enough info
                return f"Answer: {result}"

        return "Could not find an answer within the iteration limit."

# === Demo ===
if __name__ == "__main__":
    print("=== Simple Agent ===")
    agent = SimpleAgent(TOOLS)

    queries = [
        "What is the result of 15 * 7 + 3?",
        "What time is it?",
        "What is Python?",
        "Tell me about Flask",
    ]

    for q in queries:
        result = agent.process_query(q)
        print(f"  -> {result}\n")

    print("\n=== Available Tools ===")
    for name, tool in TOOLS.items():
        schema = tool.to_schema()
        print(f"  {name}: {tool.description}")

    print("\n=== ReAct Agent ===")
    react = ReActAgent(TOOLS)
    react.process_query("Calculate 2**10")
