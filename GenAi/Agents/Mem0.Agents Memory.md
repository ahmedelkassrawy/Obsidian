```python
pip install mem0ai
```

#### Intialize Memory
```python
from mem0 import Memory
from dotenv import load_dotenv
load_dotenv()
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
from langchain_chroma import Chroma

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash",
                             google_api_key = os.getenv("GOOGLE_API_KEY"))
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001",
                                          google_api_key = os.getenv("GOOGLE_API_KEY"))
vector_store = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings,
    collection_name="mem0"  # Required collection name
)

config = {
    "llm": {
        "provider": "langchain",
        "config": {
            "model": llm
        }
    },
    "embedder": {
        "provider": "langchain",
        "config": {
            "model": embeddings
        }
    },
    "vector_store": {
        "provider": "langchain",
        "config": {
            "client": vector_store
        }
    }
}

mem = Memory.from_config(config)
```

#### Add Memory
```python
messages = [
    {"role":"user","content":"Hi Omar Khaled but feel free to call me Kassra.  I love football and gaming."},
    {"role": "assistant", "content": "Hey OKAI! I'll remember your interests."}
]

mem.add(messages,user_id = "kassra")
```

#### Search Memories
```python
results = mem.search("What do you knwo about me?",user_id = "kassra")
print(results)
```

#### Get All Memories
```python
mem.get_all(user_id = "kassra")
```
---
#### Langchain integration
```python
prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content="""You are a helpful travel agent AI. Use the provided context to personalize your responses and remember user preferences and past interactions. 
    Provide travel recommendations, itinerary suggestions, and answer questions about destinations. 
    If you don't have specific information, you can make general suggestions based on common travel knowledge."""),
    MessagesPlaceholder(variable_name="context"),
    HumanMessage(content="{input}")
])
```

```python
def retrieve_context(query:str,user_id: str) -> List[Dict]:
  """Retrieve relevant context from Mem0"""
  try:
    memories = mem.search(query,user_id = user_id)
    memory_list = memories["results"]

    serialized_memories = " ".join([mem["memory"] for mem in memory_list])
    context = [
        {
            "role":"system",
                "content": f"Relevant information: {serialized_memories}"
        },
        {
            "role": "user",
            "content": query
        }
    ]

    return context
  except Exception as e:
    return [{"role":"user","content":query}]
```

```python
def generate_response(input: str, context: List[Dict]) -> str:
    """Generate a response using the language model"""
    chain = prompt | llm
    response = chain.invoke({
        "context": context,
        "input": input
    })
    return response.content
```

```python
def save_interaction(user_id: str, user_input: str, assistant_response: str):
    """Save the interaction to Mem0"""
    try:
        interaction = [
            {
              "role": "user",
              "content": user_input
            },
            {
                "role": "assistant",
                "content": assistant_response
            }
        ]
        result = mem.add(interaction, user_id=user_id)
        print(f"Memory saved successfully: {len(result.get('results', []))} memories added")
    except Exception as e:
        print(f"Error saving interaction: {e}")
```

```python
def chat_turn(user_input: str, user_id: str) -> str:
    # Retrieve context
    context = retrieve_context(user_input, user_id)
    
    # Generate response
    response = generate_response(user_input, context)
    
    # Save interaction
    save_interaction(user_id, user_input, response)
    
    return response
```

---
#### Langgraph
```python
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from typing import Annotated,TypedDict,List

class State(TypedDict):
  messages : Annotated[List[HumanMessage | AIMessage], add_messages]
  mem_user_id:str

graph = StateGraph(State)
```

```python
def chatbot(state:State):
  messages = state["messages"]
  user_id = state["mem_user_id"]

  try:
    memories = mem.search(messages[-1].content,user_id = user_id)
    memory_list = memories["results"]

    context = "Relevant information from previous conversations:\n"
    for memory in memory_list:
        context += f"- {memory['memory']}\n"

    system_message = SystemMessage(content=f"""You are a helpful customer support assistant. Use the provided context to personalize your responses and remember user preferences and past interactions.
{context}""")

    full_messages = [system_message] + messages
    response = llm.invoke(full_messages)

    try:
      interaction = [
          {
              "role":"user",
              "content":messages[-1].content
          },
          {
              "role":"assistant",
              "content":response.content
          }
      ]
      result = mem.add(interaction,user_id = user_id)
      print(f"Memory saved: {len(result.get('results', []))} memories added")
    except Exception as e:
        print(f"Error saving memory: {e}")
        
    return {"messages": [response]}
  
  except Exception as e:
    print(f"Error in chatbot: {e}")
    # Fallback response without memory context
    response = llm.invoke(messages)
    return {"messages": [response]}
```

```python
graph.add_node("chatbot", chatbot)
graph.add_edge(START, "chatbot")
graph.add_edge("chatbot", "chatbot")

compiled_graph = graph.compile()
```

```python
def run_conversation(user_input: str, mem_user_id: str):
    config = {"configurable": {"thread_id": mem_user_id}}
    initial_state = {"messages": [HumanMessage(content=user_input)], "mem_user_id": mem_user_id}

    for event in compiled_graph.stream(initial_state, config):
        for value in event.values():
            if value.get("messages"):
                print("Customer Support:", value["messages"][-1].content)
                return
```

----
#### CrewAI
```python
def store_user_preferences(user_id: str, conversation: list):
	"""Store user preferences from conversation history"""      
	mem.add(conversation, user_id=user_id)
```

```python
def create_travel_agent():
    """Create a travel planning agent with search capabilities"""
    search_tool = SerperDevTool()

    return Agent(
        role="Personalized Travel Planner Agent",
        goal="Plan personalized travel itineraries",
        backstory="""You are a seasoned travel planner, known for your meticulous attention to detail.""",
        allow_delegation=False,
        memory=True,
        tools=[search_tool],
    )
```

```python
def create_planning_task(agent, destination: str):
    """Create a travel planning task"""
    return Task(
        description=f"""Find places to live, eat, and visit in {destination}.""",
        expected_output=f"A detailed list of places to live, eat, and visit in {destination}.",
        agent=agent,
    )
```

```python
def plan_trip(destination: str, user_id: str):
    # Create agent
    travel_agent = create_travel_agent()

    # Create task
    planning_task = create_planning_task(travel_agent, destination)

    # Setup crew
    crew = Crew(
	    agents=[travel_agent],
        tasks=[planning_task],
        process=Process.sequential,
        memory=True,
        memory_config={
            "provider": "mem0",
            "config": {"user_id": user_id},
        }
    )
    
    return crew.kickoff()
    
if __name__ == "__main__":
    result = plan_trip("Cairo", "kassra")
    print(result)
```