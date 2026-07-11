```python
pip install bedrock-agentcore bedrock-agentcore-starter-toolkit langgraph-checkpoint-aws
```

```python
agentcore --help
```

```python
agentcore configure -e D:\me\PS\agent_bedrock\agentcore-crash-course-main\00_langgraph_agent.py
```

```python
agentcore launch --env GROQ_API_KEY=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 
```

```python
agentcore invoke "{'prompt': 'How do i check my balance???'}"
```

```python
from bedrock_agentcore.runtime import BedrockAgentCoreApp

# Create the AgentCore app instance
app = BedrockAgentCoreApp()
```

```python
# AgentCore Entrypoint
@app.entrypoint
def agent_invocation(payload, context):
    """Handler for agent invocation in AgentCore runtime"""
    print("Received payload:", payload)
    print("Context:", context)
    
    # Extract query from payload
    query = payload.get("prompt", "No prompt found in input")
    
    # Invoke the graph
    result = agent.invoke({"messages": [("human", query)]})
    
    print("Result:", result)
    
    # Return the answer
    return {"result": result['messages'][-1].content}


if __name__ == "__main__":
    app.run()
```

#### Adding Memory
```python
# Import AgentCore runtime and memory integrations
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from langgraph_checkpoint_aws import AgentCoreMemorySaver, AgentCoreMemoryStore
from langchain.agents.middleware import AgentMiddleware, AgentState, ModelRequest, ModelResponse

app = BedrockAgentCoreApp()
# AgentCore Memory Configuration
REGION = "ap-southeast-2"
MEMORY_ID = "lauki_agent_memory-Yrm3JrG0Vz"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize memory components
checkpointer = AgentCoreMemorySaver(memory_id=MEMORY_ID)
store = AgentCoreMemoryStore(memory_id=MEMORY_ID)
```

```python
class MemoryMiddleware(AgentMiddleware):
    # Pre-model hook: saves messages and retrieves long-term memories
    def pre_model_hook(self, state: AgentState, config: RunnableConfig, *, store: BaseStore):
        """
        Hook that runs before LLM invocation to:
        1. Save the latest human message to long-term memory
        2. Retrieve relevant user preferences and memories
        3. Append memories to the context
        """
        actor_id = config["configurable"]["actor_id"]
        thread_id = config["configurable"]["thread_id"]
        
        # Namespace for this specific session
        namespace = (actor_id, thread_id)
        messages = state.get("messages", [])
        
        # Save the last human message to long-term memory
        for msg in reversed(messages):
            if isinstance(msg, HumanMessage):
                store.put(namespace, str(uuid.uuid4()), {"message": msg})
                
                # OPTIONAL: Retrieve user preferences from long-term memory
                # Search across all sessions for this actor
                user_preferences_namespace = ("preferences", actor_id)
                try:
                    preferences = store.search(
                        user_preferences_namespace, 
                        query=msg.content, 
                        limit=5
                    )
                    
                    # If we found relevant memories, add them to the context
                    if preferences:
                        memory_context = "\n".join([
                            f"Memory: {item.value.get('message', '')}" 
                            for item in preferences
                        ])
                        # You can append this to the messages or use it another way
                        print(f"Retrieved memories: {memory_context}")
                except Exception as e:
                    print(f"Memory retrieval error: {e}")
                break
        
        return {"messages": messages}


    # OPTIONAL: Post-model hook to save AI responses
    def post_model_hook(state, config: RunnableConfig, *, store: BaseStore):
        """
        Hook that runs after LLM invocation to save AI messages to long-term memory
        """
        actor_id = config["configurable"]["actor_id"]
        thread_id = config["configurable"]["thread_id"]
        namespace = (actor_id, thread_id)
        
        messages = state.get("messages", [])
        
        # Save the last AI message
        for msg in reversed(messages):
            if isinstance(msg, AIMessage):
                store.put(namespace, str(uuid.uuid4()), {"message": msg})
                break
        
        return state
```

```python
# Create the agent with memory configurations
agent = create_agent(
    model=llm,
    tools=tools,
    checkpointer=checkpointer,
    store=store,
    middleware=[MemoryMiddleware()],
    system_prompt=system_prompt,
)


# AgentCore Entrypoint
@app.entrypoint
def agent_invocation(payload, context):
    """Handler for agent invocation in AgentCore runtime with memory support"""
    print("Received payload:", payload)
    print("Context:", context)
    
    # Extract query from payload
    query = payload.get("prompt", "No prompt found in input")
    
    # Extract or generate actor_id and thread_id
    actor_id = payload.get("actor_id", "default-user")
    thread_id = payload.get("thread_id", payload.get("session_id", "default-session"))
    
    # Configure memory context
    config = {
        "configurable": {
            "thread_id": thread_id,  # Maps to AgentCore session_id
            "actor_id": actor_id     # Maps to AgentCore actor_id
        }
    }
    
    # Invoke the agent with memory
    result = agent.invoke(
        {"messages": [("human", query)]},
        config=config
    )
    
    print("Result:", result)
    
    # Extract the final answer from the result
    messages = result.get("messages", [])
    answer = messages[-1].content if messages else "No response generated"
    
    # Return the answer
    return {
        "result": answer,
        "actor_id": actor_id,
        "thread_id": thread_id
    }


if __name__ == "__main__":
    app.run()
```