- Cordinator + Router 
- Agent State should contain `next_step`
- add_conditional_edges takes either path_map or Literal
Path Map:
```python
def route(state):
    """Routing function - returns node name or uses path_map"""
    if state.get("needs_tool"):
        return "tools" 
	
    return END
    
graph = StateGraph(State)

graph.add_node("agent", agent_node)
graph.add_node("tools", tools_node)

graph.add_conditional_edges("agent", 
							route, 
							{
								"tools": "tools", 
								END: END
							})  # path_map required for non-string keys like END
```

Literal:
```python
def route_typed(state) -> Literal["tools", "__end__"]: 
    if state["needs_tool"]:
	    return "tools"
    else "__end__"

graph.add_conditional_edges("agent", route_typed)
```

- If using a Parent agent and sub-graphs -> compile the sub-graphs in their files -> and then use agent in the parent graph
```python
parent_builder = StateGraph(AgentState)
parent_builder.add_node("coordinator", coordinator)
parent_builder.add_node("note_writer_agent", note_writer_subgraph)
parent_builder.add_node("planner_agent", planner_subgraph)

parent_builder.add_edge(START, "coordinator")
parent_builder.add_conditional_edges(
    "coordinator",
    should_continue,
    {
        "coordinator": "coordinator",
        "note_writer_agent": "note_writer_agent", 
        "planner_agent": "planner_agent",
        "end": END
    }
)
parent_builder.add_edge("note_writer_agent", "coordinator")
parent_builder.add_edge("planner_agent", "coordinator")

parent_app = parent_builder.compile(checkpointer=memory)
```

In the subgraph files:
```python
note_writer_builder = StateGraph(AgentState)

note_writer_builder.add_node("analyze_before_notes", analyze_before_notes)
note_writer_builder.add_node("generate_notes", generate_notes)

note_writer_builder.add_edge(START, "analyze_before_notes")
note_writer_builder.add_edge("analyze_before_notes", "generate_notes")
note_writer_builder.add_edge("generate_notes", END)

note_writer_subgraph = note_writer_builder.compile()
```

- If we want input for a node or a new phase, you can add interrupts in the cordinator:
```python
async def coordinator(state: AgentState):
	...
	if any(word in last_user_msg for word in ["note", "summarize", "write"]):
        if not state.get("subject"):
            subject = interrupt("Please provide the subject for which you want to write notes: ")
            
            state["subject"] = subject
            state["next_step"] = "note_writer_agent"
```

The function of the run_agent function to deal with the interrupt:
```python
async def run_agent(thread_id:str = "default"):
	state = await parent_app.ainvoke(initial_state, config)
	
	while True:
        try:
            # 1. Use aget_state (async) to check for interrupts
            snapshot = await parent_app.aget_state(config) # Corrected to aget_state
            
            if snapshot.tasks and snapshot.tasks[0].interrupts:
                # Get the first active interrupt
                irq = snapshot.tasks[0].interrupts[0]
                
                # Request the specific input required by the node
                user_answer = input(f"\n📝 {irq.value} ").strip()
                
                print("🤔 Thinking...")
                # Resume using Command(resume=...)
                state = await parent_app.ainvoke(Command(resume=user_answer), config)
                
                # Display the AI's response after resuming
                if state.get("messages"):
                    last_msg = state["messages"][-1]
                    
                    if isinstance(last_msg, AIMessage):
                        print(f"🤖 {last_msg.content}")
                continue
             
```

```python   
			# 2. Standard user input flow
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 Goodbye!")
                break
            
            if not user_input:
                continue

            print("🤔 Thinking...")
            # We only send the new message; LangGraph handles history via the thread_id
            state = await parent_app.ainvoke(
                {
	                "messages": [HumanMessage(content=user_input)]
				}, 
                config
            )
            
            # Print the latest response
            if state.get("messages"):
                last_msg = state["messages"][-1]
                
                if isinstance(last_msg, AIMessage):
                    print(f"🤖 {last_msg.content}")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ {e}")
```

- Saving records based on the model_class from pydantic
```python
 async def _save_record(self, model_class, data_dict: dict):
        """Generic helper to save a record."""
        async with self.db() as session:
            try:
                record = model_class(**data_dict)
                
                session.add(record)
                
                await session.commit()
                await session.refresh(record)
                
                logger.info(f"Saved {model_class.__name__} ID: {record.id}")
                
                return True
            except Exception as e:
                logger.error(f"Error saving {model_class.__name__}: {e}")
                await session.rollback()
                
                return False
```

- parse datetime
```python
def parse_datetime(self, datetime_str: str) -> datetime:
        """Parse datetime string or return now."""
        return dateparser.parse(datetime_str) or datetime.now()
```

- get upcoming events
```python
async def get_upcoming_events(self, days: int = 7) -> List[Dict]:
        """Get events for the next X days."""
        now = datetime.now()
        future_date = now + timedelta(days=days)
```
