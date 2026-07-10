Tools -> dont use state as a paramter
always use tool node,bind the llm with tools

```python
tools = [categorize_transaction, analyze_budget]
llm_with_tools = llm.bind_tools(tools)

def should_continue(state:State):
    last_msg = state["messages"][-1]

    if last_msg.tool_calls:
        return "tools"
    return END

def call_model(state:State):
    response = llm_with_tools.invoke(state["messages"])
    
    # Return response with preserved state values
    return {
        "messages": [response],
        "budget": state.get("budget", 0.0),
        "status": state.get("status", "active"),
        "income": state.get("income", 0.0),
        "expense": state.get("expense", 0.0)
    }

workflow = StateGraph(State)

workflow.add_node("call_model", call_model)
workflow.add_node("tools", tools_node)

workflow.add_edge(START, "call_model")
workflow.add_conditional_edges("call_model",
                               should_continue,
                               ["tools", END])
workflow.add_edge("tools", "call_model")
```