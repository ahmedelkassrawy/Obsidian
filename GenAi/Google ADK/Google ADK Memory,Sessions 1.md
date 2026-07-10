```python
import asyncio
from google.adk.agents.llm_agent import LlmAgent
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.adk import Runner
from google.genai import types
from google import genai
from google.adk.agents import Agent, SequentialAgent, ParallelAgent, LoopAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import AgentTool, FunctionTool, google_search
from google.genai import types
import os
import uuid
from google.genai import types

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams

from google.adk.apps.app import App, ResumabilityConfig
from google.adk.tools.function_tool import FunctionTool
from google.adk.runners import InMemoryRunner
import base64
from typing import Any, Dict

from google.adk.agents import Agent, LlmAgent
from google.adk.apps.app import App, EventsCompactionConfig
from google.adk.models.google_llm import Gemini
from google.adk.sessions import DatabaseSessionService
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.adk.tools.tool_context import ToolContext
from google.genai import types

# Configure the API key
os.environ["GOOGLE_API_KEY"] = "AIzaSyDalL1UUklJWiwjg4npoVOYhAuZU13EVP4"

# Initialize the Google GenAI client with API key
client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

retry_config = types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504], # Retry on these HTTP errors
)

async def run_session(runner_instance:Runner, user_queries:list[str] | str = None,
                      session_name:str = "default"):
    print(f"\n ### Session: {session_name}")

    #get app name from runner
    app_name = runner_instance.app_name

    #attempt to create a new session or retrieve existing one
    try:
        session = await session_service.create_session(
            app_name = app_name,
            user_id = USER_ID,
            session_id = session_name
        )
    except:
        session = await session_service.get_session(
            app_name = app_name,
            user_id = USER_ID,
            session_id = session_name
        )

    #process queries if provided
    if user_queries:
        #Convert single query to list for uniform processing
        if type(user_queries) == str:
            user_queries = [user_queries]

        #Process each user query in list sequentially
        for query in user_queries:
            print(f"\nUser > {query}")

            #Convert the query string to ADK Content format
            query = types.Content(
                role = "user",
                parts = [types.Part(text = query)]
            )

            #Stream the agent's response async
            async for event in runner_instance.run_async(
                user_id = USER_ID,
                session_id= session_name,
                new_message= query,
            ):
                #Check if the event contains valid content
                if event.content and event.content.parts:
                    #Filter out empty or None 
                    if (event.content.parts[0].text != "None" 
                        and event.content.parts[0].text):
                        print(f"{MODEL_NAME} > ",event.content.parts[0].text)
                    else:
                        print("NO QUERIES!")              
```

#### Sessions
- A session is a container for conversations
- It encapsulates the conversation history in a chronological manner and also records all tool interactions and responses for a **single, continuous conversation**.
- A session is tied to a user and agent , its is not shared with other users.

**Session.Events**:

> While a session is a container for conversations, `Events` are the building blocks of a conversation.
> 
> Example of Events:
> 
> - _User Input_: A message from the user (text, audio, image, etc.)
> - _Agent Response_: The agent's reply to the user
> - _Tool Call_: The agent's decision to use an external tool or API
> - _Tool Output_: The data returned from a tool call, which the agent uses to continue its reasoning

**{} Session.State**:

> `session.state` is the Agent's scratchpad, where it stores and updates dynamic details needed during the conversation. Think of it as a global `{key,`value} pair storage which is available to all subagents and tools.

##### How to manage sessions?
An agentic application can have multiple users and each user may have multiple sessions with the application. To manage these sessions and events, ADK offers a **Session Manager** and **Runner**.

1. **`SessionService`**: The storage layer
    - Manages creation, storage, and retrieval of session data
    - Different implementations for different needs (memory, database, cloud)

2. **`Runner`**: The orchestration layer
    - Manages the flow of information between user and agent
    - Automatically maintains conversation history
    - Handles the Context Engineering behind the scenes

Think of it like this:
- **Session** = A notebook 
- **Events** = Individual entries in a single page 
- **SessionService** = The filing cabinet storing notebooks 
- **Runner** = The assistant managing the conversation 

```python
#Step 1: setup the agent
root_agent = Agent(
    model = Gemini(
        model = MODEL_NAME,
        retry_options= retry_config,
        name = "text_chat",
        description = "A text chatbot",
    )
)       

#step 2: setup session management
session_service = InMemorySessionService()

#setup the runner
runner = Runner(agent = root_agent,
                app_name = APP_NAME,
                session_service= session_service)

print("✅ Stateful agent initialized!")
print(f"   - Application: {APP_NAME}")
print(f"   - User: {USER_ID}")
print(f"   - Using: {session_service.__class__.__name__}")

await run_session(
    runner,
    [
        "Hi,I am Sam! What is the captial of France?",
        "Hello! What is my name?",
    ],
    "stateful-agentic-session"
)

await run_session(
    runner,
    ["What did I ask you about earlier?", 
     "And remind me, what's my name?"],
    "stateful-agentic-session",
)
```

#### ## Persistent Sessions with `DatabaseSessionService`
ADK provides different SessionService implementations for different needs:

ADK provides different SessionService implementations for different needs:

				Service	  Use Case	Persistence	Best For
	InMemorySessionService	Development & Testing	❌     Lost on restart	Quick prototypes
	DatabaseSessionService	Self-managed apps	✅ Survives restarts	Small to medium apps
	Agent Engine Sessions	Production on GCP	✅ Fully managed	Enterprise scale

### Implementing Persistent Sessions
Let's upgrade to `DatabaseSessionService` using SQLite. This gives us persistence without needing a separate database server for this demo.

Let's create a `chatbot_agent` capable of having a conversation with the user.
```python
chatbot_agent = LlmAgent(
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    name="text_chat_bot",
    description="A text chatbot with persistent memory",
)
#steup 2: Switch to DatabaseSessionService
db_url = "sqlite:///my_agent_data.db"
session_service = DatabaseSessionService(db_url = db_url)

#setup 3: create runner
runner = Runner(
    agent = chatbot_agent,
    app_name=APP_NAME,
    session_service= session_service,
)

print("✅ Upgraded to persistent sessions!")
print(f"   - Database: my_agent_data.db")
print(f"   - Sessions will survive restarts!")

await run_session(
    runner,
    [
        "Hi, I am Sam! What is the capital of the United States?", 
        "Hello! What is my name?"
    ],
    "test-db-session-01",
)

await run_session(
    runner,
    [
        "What is the capital of India?", 
        "Hello! What is my name?"
    ],
    "test-db-session-01",
)

await run_session(
    runner, 
    ["Hello! What is my name?"], 
    "test-db-session-02"
)  # Note, we are using new session name
```

## Context Compaction
As you can see, all the events are stored in full in the session Database, and this quickly adds up. For a long, complex task, this list of events can become very large, leading to slower performance and higher costs.

But what if we could automatically summarize the past? Let's use ADK's **Context Compaction** feature to see **how to automatically reduce the context that's stored in the Session.**

We'll also create a new config to do the Context Compaction. This **`EventsCompactionConfig`** defines two key variables:

- **compaction_interval**: Asks the Runner to compact the history after every `n` conversations
- **overlap_size**: Defines the number of previous conversations to retain for overlap

We'll then provide this app to the Runner.
```python
research_app_compacting = App(
    name="research_app_compacting",
    root_agent=chatbot_agent,
    # This is the new part!
    events_compaction_config=EventsCompactionConfig(
        compaction_interval=3,  # Trigger compaction every 3 invocations
        overlap_size=1,  # Keep 1 previous turn for context
    ),
)

db_url = "sqlite:///my_agent_data.db"  # Local SQLite file
session_service = DatabaseSessionService(db_url=db_url)

# Create a new runner for our upgraded app
research_runner_compacting = Runner(
    app=research_app_compacting, 
    session_service=session_service
)


print("✅ Research App upgraded with Events Compaction!")
```

## Working with Session State
### 5.1 Creating custom tools for Session state management[](https://www.kaggle.com/code/kaggle5daysofai/day-3a-agent-sessions#5.1-Creating-custom-tools-for-Session-state-management)

Let's explore how to manually manage session state through custom tools. In this example, we'll identify a **transferable characteristic**, like a user's name and their country, and create tools to capture and save it.

**Why This Example?**

The username is a perfect example of information that:

- Is introduced once but referenced multiple times
- Should persist throughout a conversation
- Represents a user-specific characteristic that enhances personalization
```python
# Define scope levels for state keys (following best practices)
USER_NAME_SCOPE_LEVELS = ("temp", "user", "app")

# This demonstrates how tools can write to session state using tool_context.
# The 'user:' prefix indicates this is user-specific data.
def save_userinfo(
    tool_context: ToolContext, user_name: str, country: str
) -> Dict[str, Any]:
    """Tool to record and save user name and country in session state."""
    # Write to session state using the 'user:' prefix for user data
    tool_context.state["user:name"] = user_name
    tool_context.state["user:country"] = country

    return {"status": "success"}

#how tools can read from session state 
def retrieve_userinfo(tool_context: ToolContext) -> Dict[str,any]:
    """Tool to retrieve username and country from session state"""

    user_name = tool_context.state.get("user:name", "Unknown")
    country = tool_context.state.get("user:country", "Unknown")

    return {
        "status":"success",
        "user_name": user_name,
        "country": country
    }
```

**Key Concepts:**
- Tools can access `tool_context.state` to read/write session state
- Use descriptive key prefixes (`user:`, `app:`, `temp:`) for organization
- State persists across conversation turns within the same session

```python
APP_NAME = "default"
USER_ID = "default"
MODEL_NAME  = "gemini-2.5-flash-lite"

root_agent = LlmAgent(
    name = "text_chatbot",
    model = Gemini(
        model = MODEL_NAME,
        retry_options= retry_config,
    ),
    description = """A text chatot.
    * To record username and country when provided use `save_userinfo` tool. 
    * To fetch username and country when required use `retrieve_userinfo` tool.
    """,
    tools = [save_userinfo, retrieve_userinfo]
)

session_service = InMemorySessionService()
runner = Runner(agent=root_agent,
                session_service=session_service, 
                app_name="default")

await run_session(
    runner,
    [
        "Hi there, how are you doing today? What is my name?",  # Agent shouldn't know the name yet
        "My name is Sam. I'm from Poland.",  # Provide name - agent should save it
        "What is my name? Which country am I from?",  # Agent should recall from session state
    ],
    "state-demo-session",
)
```
---
### Why Memory?
Memory provides capabilities that Sessions alone cannot:

|Capability|What It Means|Example|
|---|---|---|
|**Cross-Conversation Recall**|Access information from any past conversation|"What preferences has this user mentioned across all chats?"|
|**Intelligent Extraction**|LLM-powered consolidation extracts key facts|Stores "allergic to peanuts" instead of 50 raw messages|
|**Semantic Search**|Meaning-based retrieval, not just keyword matching|Query "preferred hue" matches "favorite color is blue"|
|**Persistent Storage**|Survives application restarts|Build knowledge that grows over time|

**Example:** Imagine talking to a personal assistant:
- 🗣️ **Session**: They remember what you said 10 minutes ago in THIS conversation
- 🧠 **Memory**: They remember your preferences from conversations LAST WEEK

```python
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.memory import InMemoryMemoryService
from google.adk.tools import load_memory, preload_memory
from google.genai import types
```
#### Memory Workflow
There are **three high-level steps.**
**Three-step integration process:**

1. **Initialize** → Create a `MemoryService` and provide it to your agent via the `Runner`
2. **Ingest** → Transfer session data to memory using `add_session_to_memory()`
3. **Retrieve** → Search stored memories using `search_memory()`

## Initialize MemoryService
### 3.1 Initialize Memory
ADK provides multiple `MemoryService` implementations through the `BaseMemoryService` interface:

- **`InMemoryMemoryService`** - Built-in service for prototyping and testing (keyword matching, no persistence)
- **`VertexAiMemoryBankService`** - Managed cloud service with LLM-powered consolidation and semantic search
- **Custom implementations** - You can build your own using databases, though managed services are recommended

For this notebook, we'll use `InMemoryMemoryService` to learn the core mechanics. The same methods work identically with production-ready services like Vertex AI Memory Bank.

```python
memory_service = (
    InMemoryMemoryService()
)  # ADK's built-in Memory Service for development and testing
```

##### Add Memory to agent
```python
APP_NAME = "MemoryDemoApp"
USER_ID = "demo_user"

# Create agent
user_agent = LlmAgent(
    model=Gemini(model="gemini-2.5-flash-lite", 
                 retry_options=retry_config),
    name="MemoryDemoAgent",
    instruction="Answer user questions in simple words.",
)
```

Create Runner
Now provide both Session and Memory services to the Runner.

Key configuration:
The Runner requires both services to enable memory functionality:
- session_service → Manages conversation threads and events
- memory_service → Provides long-term knowledge storage
Both services work together: Sessions capture conversations, Memory stores knowledge for retrieval across sessions.
```python
session_service = InMemorySessionService()

runner = Runner(
    agent = user_agent,
    app_name = "MemoryDemoApp",
    session_service = session_service,
    memory_service = memory_service,
)
```

### Important
**💡 Configuration vs. Usage:** Adding `memory_service` to the `Runner` makes memory _available_ to your agent, but doesn't automatically use it. You must explicitly:

1. **Ingest data** using `add_session_to_memory()`
2. **Enable retrieval** by giving your agent memory tools (`load_memory` or `preload_memory`)

### MemoryService Implementation Options
**This notebook: `InMemoryMemoryService`**

- Stores raw conversation events without consolidation
- Keyword-based search (simple word matching)
- In-memory storage (resets on restart)
- Ideal for learning and local development

**Production: `VertexAiMemoryBankService` (You'll learn this on Day 5)**

- LLM-powered extraction of key facts
- Semantic search (meaning-based retrieval)
- Persistent cloud storage
- Integrates external knowledge sources

**💡 API Consistency:** Both implementations use identical methods (`add_session_to_memory()`, `search_memory()`). The workflow you learn here applies to all memory services!

#### Ingest Session Data into Memory
**Why should you transfer Session data to Memory?**

Now that memory is initialized, you need to populate it with knowledge. When you initialize a MemoryService, it starts completely empty. All your conversations are stored in Sessions, which contain raw events including every message, tool call, and metadata. To make this information available for long-term recall, you explicitly transfer it to memory using `add_session_to_memory()`.

Here's where managed memory services like Vertex AI Memory Bank shine. **During transfer, they perform intelligent consolidation - extracting key facts while discarding conversational noise.** The `InMemoryMemoryService` we're using stores everything without consolidation, which is sufficient for learning the mechanics.

Before we can transfer anything, we need data. Let's have a conversation with our agent to populate the session.
```python 
await run_session(
    runner,
    "My favorite color is blue-green. Can you write a Haiku about it?",
    "conversation-01",  # Session ID
)
```

The session contains our conversation. Now we're ready to transfer it to memory. Call `add_session_to_memory()` and pass the session object. This ingests the conversation into the memory store, making it available for future searches.
```python
await memory_service.add_session_to_memory(session)
```

####  Enable Memory Retrieval in Your Agent
You've successfully transferred session data to memory, but there's one crucial step remaining. **Agents can't directly access the MemoryService - they need tools to search it.**

### Memory Retrieval in ADK
ADK provides two built-in tools for memory retrieval:

**`load_memory` (Reactive)**

- Agent decides when to search memory
- Only retrieves when the agent thinks it's needed
- More efficient (saves tokens)
- Risk: Agent might forget to search

**`preload_memory` (Proactive)**

- Automatically searches before every turn
- Memory always available to the agent
- Guaranteed context, but less efficient
- Searches even when not needed

`load_memory` is looking things up only when you need them, while `preload_memory` is reading all your notes before answering each question.
```python
# Create agent
user_agent = LlmAgent(
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    name="MemoryDemoAgent",
    instruction="Answer user questions in simple words. Use load_memory tool if you need to recall past conversations.",
    tools=[
        load_memory
    ],  # Agent now has access to Memory and can search it whenever it decides to!
)

# Create a new runner with the updated agent
runner = Runner(
    agent=user_agent,
    app_name=APP_NAME,
    session_service=session_service,
    memory_service=memory_service,
)

await run_session(runner, "My birthday is on March 15th.", "birthday-session-01")
```

```python
birthday_session = await session_service.get_session(
    app_name=APP_NAME, user_id=USER_ID, session_id="birthday-session-01"
)

await memory_service.add_session_to_memory(birthday_session)

print("✅ Birthday session saved to memory!")
```

**What happens:**
1. Agent receives: "When is my birthday?"
2. Agent recognizes: This requires past conversation context
3. Agent calls: `load_memory("birthday")`
4. Memory returns: Previous conversation containing "March 15th"
5. Agent responds: "Your birthday is on March 15th"

The memory retrieval worked even though this is a completely different session!

**What changes:**

- `load_memory` (reactive): Agent decides when to search
- `preload_memory` (proactive): Automatically loads memory before every turn

**Test it:**

1. Ask "What is my favorite color?" in a new session
2. Ask "Tell me a joke" - notice that `preload_memory` still searches memory even though it's unnecessary
3. Which pattern is better for different use cases?

#### Searching
```python
# Search for color preferences
search_response = await memory_service.search_memory(
    app_name=APP_NAME, user_id=USER_ID, query="What is the user's favorite color?"
)

print("🔍 Search Results:")
print(f"  Found {len(search_response.memories)} relevant memories")
print()

for memory in search_response.memories:
    if memory.content and memory.content.parts:
        text = memory.content.parts[0].text[:80]
        print(f"  [{memory.author}]: {text}...")
```

### How Search Works
**InMemoryMemoryService (this notebook):**

- **Method:** Keyword matching
- **Example:** "favorite color" matches because those exact words exist
- **Limitation:** "preferred hue" won't match

**VertexAiMemoryBankService (Day 5):**

- **Method:** Semantic search via embeddings
- **Example:** "preferred hue" WILL match "favorite color"
- **Advantage:** Understands meaning, not just keywords

#### Automating Memory Storage
##### Callbacks
ADK's callback system lets you hook into key execution moments. Callbacks are **Python functions** you define and attach to agents - ADK automatically calls them at specific stages, acting like checkpoints during the agent's execution flow.

**Think of callbacks as event listeners in your agent's lifecycle.** When an agent processes a request, it goes through multiple stages: receiving the input, calling the LLM, invoking tools, and generating the response. Callbacks let you insert custom logic at each of these stages without modifying the core agent code.

**Available callback types:**

- `before_agent_callback` → Runs before agent starts processing a request
- `after_agent_callback` → Runs after agent completes its turn
- `before_tool_callback` / `after_tool_callback` → Around tool invocations
- `before_model_callback` / `after_model_callback` → Around LLM calls
- `on_model_error_callback` → When errors occur
![[Pasted image 20251123175344.png]]

### Automatic Memory Storage with Callbacks
For automatic memory storage, we'll use `after_agent_callback`. This function triggers every time the agent finishes a turn, then calls `add_session_to_memory()` to persist the conversation automatically.

But here's the challenge: how does our callback function actually access the memory service and current session? That's where `callback_context` comes in.

When you define a callback function, ADK automatically passes a special parameter called `callback_context` to it. The `callback_context` provides access to the Memory Service and other runtime components.

**How we'll use it:** In our callback, we'll access the memory service and current session to automatically save conversation data after each turn.

**💡 Important:** You don't create this context - ADK creates it and passes it to your callback automatically when the callback runs.

```python
async def auto_save_to_memory(callback_context):
	"""Automatically save session to memory after each agent turn."""
	await callback_context._invocation_cotext.memory_service.add_session_to_memory(
		callback_context._invocation_context,session
	)
```

### Create an Agent: Callback and PreLoad Memory Tool
Now create an agent that combines:

- **Automatic storage:** `after_agent_callback` saves conversations
- **Automatic retrieval:** `preload_memory` loads memories

This creates a fully automated memory system with zero manual intervention
```python
# Agent with automatic memory saving
auto_memory_agent = LlmAgent(
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    name="AutoMemoryAgent",
    instruction="Answer user questions.",
    tools=[preload_memory],
    after_agent_callback=auto_save_to_memory,  # Saves after each turn!
)
```

**What happens automatically:**
- After every agent response → callback triggers
- Session data → transferred to memory
- No manual `add_session_to_memory()` calls needed

```python
# Create a runner for the auto-save agent
# This connects our automated agent to the session and memory services
auto_runner = Runner(
    agent=auto_memory_agent,  # Use the agent with callback + preload_memory
    app_name=APP_NAME,
    session_service=session_service,  # Same services from Section 3
    memory_service=memory_service,
)
```

```python
# Test 1: Tell the agent about a gift (first conversation)
# The callback will automatically save this to memory when the turn completes
await run_session(
    auto_runner,
    "I gifted a new toy to my nephew on his 1st birthday!",
    "auto-save-test",
)

# Test 2: Ask about the gift in a NEW session (second conversation)
# The agent should retrieve the memory using preload_memory and answer correctly
await run_session(
    auto_runner,
    "What did I gift my nephew?",
    "auto-save-test-2",  # Different session ID - proves memory works across sessions!
)
```

**What just happened:**
1. **First conversation:** Mentioned gift to nephew
    - Callback automatically saved to memory ✅
2. **Second conversation (new session):** Asked about the gift
    - `preload_memory` automatically retrieved the memory ✅
    - Agent answered correctly ✅

**Zero manual memory calls!** This is automated memory management in action.

### How often should you save Sessions to Memory?
**Options:**

|Timing|Implementation|Best For|
|---|---|---|
|**After every turn**|`after_agent_callback`|Real-time memory updates|
|**End of conversation**|Manual call when session ends|Batch processing, reduce API calls|
|**Periodic intervals**|Timer-based background job|Long-running conversations|

---
### Section 7: Memory Consolidation
### The Limitation of Raw Storage
**What we've stored so far:**

- Every user message
- Every agent response
- Every tool call

**The problem:**

```
Session: 50 messages = 10,000 tokens
Memory:  All 50 messages stored
Search:  Returns all 50 messages → Agent must process 10,000 tokens
```

This doesn't scale. We need **consolidation**.
### What is Memory Consolidation?
**Memory Consolidation** = Extracting **only important facts** while discarding conversational noise.

**Before (Raw Storage):**

```
User: "My favorite color is BlueGreen. I also like purple. 
       Actually, I prefer BlueGreen most of the time."
Agent: "Great! I'll remember that."
User: "Thanks!"
Agent: "You're welcome!"

→ Stores ALL 4 messages (redundant, verbose)
```

**After (Consolidation):**

```
Extracted Memory: "User's favorite color: BlueGreen"

→ Stores 1 concise fact
```

### How Consolidation Works (Conceptual)
**The pipeline:**
```
1. Raw Session Events
   ↓
2. LLM analyzes conversation
   ↓
3. Extracts key facts
   ↓
4. Stores concise memories
   ↓
5. Merges with existing memories (deduplication)
```

**Example transformation:**

```
Input:  "I'm allergic to peanuts. I can't eat anything with nuts."

Output: Memory {
  allergy: "peanuts, tree nuts"
  severity: "avoid completely"
}
```

**Key Point:** Managed Memory Services handle consolidation **automatically**.
**You use the same API:**

- `add_session_to_memory()` ← Same method
- `search_memory()` ← Same method

**The difference:** What happens behind the scenes.
- **InMemoryMemoryService:** Stores raw events
- **VertexAiMemoryBankService:** Intelligently consolidates before storing