# Core Python Concepts

## Core Themes
- Agent loops, tool invocation, and reasoning patterns.
- Memory, workflows, multi-agent orchestration, and human review.
- Debugging and evaluating agent behavior.

## Core Theme Examples
- Example 1: Agent selecting and executing tools from a registry.
- Example 2: In-context memory and episodic state management.
- Example 3: Multi-agent orchestration with specialist collaboration.

## Files and Concepts
- agent_evaluation_debugging.py: agent logging, behavior evaluation, debugging traces
- agent_loop_example.py: agent setup, tool integration, stepwise execution
- agent_patterns.py: tool schemas, calculator-style tools, reusable agent patterns
- autogen_framework.py: multi-agent collaboration and delegated execution
- custom_tools.py: tool definitions, metadata, callable tool wrappers
- human_in_the_loop.py: human overrides, approvals, feedback integration
- langgraph_workflow.py: state-machine workflows, node transitions
- memory_types.py: in-context, episodic, and external memory types
- multi_agent_systems.py: orchestrators, specialist agents, collaboration patterns
- react_pattern.py: plan-act-observe reasoning cycle
- tool_function_calling.py: function selection, tool execution driven by model output

## Core Example
This example models a tiny agent loop that chooses and runs a tool.

```python
tools = {
	"sum": lambda values: sum(values),
	"echo": lambda text: text,
}

plan = {"tool": "sum", "input": [1, 2, 3]}
result = tools[plan["tool"]](plan["input"])

print(result)
```
