```python
structured_llm = llm.with_structured_output(SearchQuery)
llm_with_tools = llm.bind_tools([multiply])
msg = llm_with_tools.invoke("What is 2 times 3?") # Get the tool call msg.tool_calls
```

The routing 
```python
def check_punchline(state: State): """Gate function to check if the joke has a punchline""" # Simple check - does the joke contain "?" or "!" 
	if "?" in state["joke"] or "!" in state["joke"]: 
		return "Pass" 
	return "Fail"

workflow.add_conditional_edges("generate_joke", 
	check_punchline, 
	{"Fail": "improve_joke", 
	"Pass": END} 
)
```

Parrelization
![[Pasted image 20260310003418.png]]
```python
parallel_builder.add_edge(START, "call_llm_1") parallel_builder.add_edge(START, "call_llm_2") parallel_builder.add_edge(START, "call_llm_3") parallel_builder.add_edge("call_llm_1", "aggregator") parallel_builder.add_edge("call_llm_2", "aggregator") parallel_builder.add_edge("call_llm_3", "aggregator") parallel_builder.add_edge("aggregator", END)
```

Routing
```python
class Route(BaseModel): 
	step: Literal["poem", "story", "joke"] = Field( None, description="The next step in the routing process" )
	
router = llm.with_structured_output(Route)

class State(TypedDict): 
	input: str 
	decision: str 
	output: str
	
  
# Conditional edge function to route to the appropriate node 
def route_decision(state: State): 
	# Return the node name you want to visit next 
	if state["decision"] == "story": 
		return "llm_call_1" 
	elif state["decision"] == "joke": 
		return "llm_call_2" 
	elif state["decision"] == "poem": 
		return "llm_call_3"
		
router_builder.add_conditional_edges("llm_call_router",
	route_decision, { # Name returned by route_decision : Name of next node to visit 
	"llm_call_1": "llm_call_1", 
	"llm_call_2": "llm_call_2", 
	"llm_call_3": "llm_call_3", 
	}, 
)
```

Orchestrator-worker :
 This is common with workflows that write code or need to update content across multiple files
 
- Breaks down tasks into subtasks
- Delegates subtasks to workers
- Synthesizes worker outputs into a final result

Creating Workers in Langgraph
- The `Send` API lets you dynamically create worker nodes and send them specific inputs. 
- Each worker has its own state, and all worker outputs are written to a shared state key that is accessible to the orchestrator graph. 
- This gives the orchestrator access to all worker output and allows it to synthesize them into a final output. 
- The example below iterates over a list of sections and uses the `Send` API to send a section to each worker.

Agents
```python
from langchain.tools import tool

@tool
def func

tools = [add, multiply, divide] 
tools_by_name = {tool.name: tool for tool in tools} llm_with_tools = llm.bind_tools(tools)

def tool_node(state: dict):
    """Performs the tool call"""

    result = []
    for tool_call in state["messages"][-1].tool_calls:
        tool = tools_by_name[tool_call["name"]]
        observation = tool.invoke(tool_call["args"])
        result.append(ToolMessage(content=observation, tool_call_id=tool_call["id"]))
    return {"messages": result}
    
def should_continue(state: MessagesState) -> Literal["tool_node", END]:
    """Decide if we should continue the loop or stop based upon whether the LLM made a tool call"""

    messages = state["messages"]
    last_message = messages[-1]

    # If the LLM makes a tool call, then perform an action
    if last_message.tool_calls:
        return "tool_node"

    return END
    
agent_builder.add_node("llm_call", llm_call)
agent_builder.add_node("tool_node", tool_node)

agent_builder.add_edge(START, "llm_call")
agent_builder.add_conditional_edges(
    "llm_call",
    should_continue,
    ["tool_node", END]
)
agent_builder.add_edge("tool_node", "llm_call")
```