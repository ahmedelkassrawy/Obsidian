# Google ADK Agent Tutorial

This document is a compiled tutorial on building agents using the Google Agent Development Kit (ADK). It covers creating agent projects, updating them, running agents, building multi-tool agents, the first agent setup, agent teams, and adding memory with session state.
![[Pasted image 20251121164808.png]]

- Agents
	- Root Agent: The primary controlling agent for a workflow. All other agents in an ADK agent workflow are considered Sub Agents.
	- LLM Agent: An agent powered by a generative AI model.
	- Sequential Agent: A workflow agent that executes a series of sub-agents in a sequence.
	- Loop Agent: A workflow agent that repeatedly executes a sub-agent until a certain condition is met.
	- Parallel Agent: A workflow agent that executes multiple sub-agents concurrently.

- Tools
	- Prebuilt tools: A limited set of ADK-provided tools can be added to agents.
	- Custom tools: You can build and add custom tools to your workflow.
	
- Components
	- Callbacks A flow control component that lets you modify the behavior of agents at the start and end of agent workflow events.

| Feature              | LLM Agent (`LlmAgent`)            | Workflow Agent                              | Custom Agent (`BaseAgent` subclass)       |
| -------------------- | --------------------------------- | ------------------------------------------- | ----------------------------------------- |
| **Primary Function** | Reasoning, Generation, Tool Use   | Controlling Agent Execution Flow            | Implementing Unique Logic/Integrations    |
| **Core Engine**      | Large Language Model (LLM)        | Predefined Logic (Sequence, Parallel, Loop) | Custom Code                               |
| **Determinism**      | Non-deterministic (Flexible)      | Deterministic (Predictable)                 | Can be either, based on implementation    |
| **Primary Use**      | Language tasks, Dynamic decisions | Structured processes, Orchestration         | Tailored requirements, Specific workflows |
## Safety Instructions Note
*These instructions are referenced but not directly used in the response. Always adhere to core guidelines.*

## Installation
```python
pip install google-adk
```

## Create an Agent Project
```python
adk create my_agent
```

The created agent project has the following structure, with the `agent.py` file containing the main control code for the agent.

```text
my_agent/
    agent.py # main agent code
    .env # API keys or project IDs
    __init__.py
```

## Update Agent Project
- The `agent.py` file contains a `root_agent` definition which is the only required element of an ADK agent.
- You can also define tools for the agent to use.
- Update the generated `agent.py` code to include a `get_current_time` tool for use by the agent, as shown in the following code:

```python
from google.adk.agents.llm_agent import Agent

# Mock tool implementation
def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city."""
    return {"status": "success",
    "city": city,
    "time": "10:30 AM"}

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description="Tells the current time in a specified city.",
    instruction="You are a helpful assistant that tells the current time in cities. Use the 'get_current_time' tool for this purpose.",
    tools=[get_current_time],
)
```

## Run Your Agent
In CLI:
```python
adk run my_agent
```

In web interface:
```python
adk web --port 8000
```

---

## Build Multi-Tool Agent

### 1. Create Agent Project
```python
mkdir multi_tool_agent/
```

### 2. Create __init__.py File in the Folder
`multi_tool_agent/__init__.py`
```python
from . import agent
```

### 3. Create agent.py
```python
import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent

def get_weather(city:str) -> dict:
    """Retrieve current weather report"""
    if city.lower() == "new york":
        return {
            "status":"success",
            "report": ("The weather in New York is sunny with a temperature of 25 degrees"),
        }
    else:
        return {
            "status":"error",
            "error_message": f"Weather information for '{city}' is not available.",
        }
```

```python
def get_current_time(city:str) -> dict:
    """Returns the current time in a speciified city"""
    if city.lower() == "new york":
        tz_identifier = "America/New_York"
    else:
        return {
            "status": "error",
            "error_message": (f"Sorry, I don't have timezone information for {city}."),
        }
    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = (f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}')
    return {"status": "success", "report": report}
```

```python
root_agent = Agent(
    name = "weather_time_agent",
    model = "gemini-2.0-flash",
    description = ("Agent to answer questions about the time and weather in a city"),
    instruction = ("You are a helpful agent who can answer user questions about the time and weather in a city."),
    tools = [get_weather,get_current_time],
)
```

### 4. Create .env
```python
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=PASTE_YOUR_ACTUAL_API_KEY_HERE
```

### 5. Run Agent
Web:
```
adk web
```

CLI:
```
adk run multi_tool_agent
```

API:
```
adk api_server
```

---

## Building First Agent

### 1. Tools
```python
def get_weather(city:str) -> dict:
  """Retrieves the current weather report for a specified city."""
  print(f"--- Tool: get_weather called for city: {city} ---")
  city = city.lower().replace(" ","")
  mock_weather_db = {
        "newyork": {"status": "success", "report": "The weather in New York is sunny with a temperature of 25°C."},
        "london": {"status": "success", "report": "It's cloudy in London with a temperature of 15°C."},
        "tokyo": {"status": "success", "report": "Tokyo is experiencing light rain and a temperature of 18°C."},
    }
  if city in mock_weather_db:
    return mock_weather_db[city]
  else:
    return {
        "status":"error",
        "error_message": f"The city {city} is not supported."
    }
```

### 2. Agent
```python
weather_agent = Agent(
    name = "weather_agent",
    model = "gemini-2.0-flash",
    description = "Provides weather information for specified cities",
    instruction = "You are a helpful weather assistant"
                  "When the user asks for the weather in a specific city"
                  "use the 'get_weather' tool to get the weather report"
                  "If the tool returns an error, inform the user politely"
                  "If the tool is successful, present the weather report clearly",
    tools = [get_weather],
)
print(f"Agent '{weather_agent.name}' created using model")
```

### 3. Setup Runner and Session Service
To manage conversations and execute the agent:
- **SessionService**: Responsible for managing conversation history and state for different users and sessions. The `InMemorySessionService` is a simple implementation that stores everything in memory, suitable for testing and simple applications. It keeps track of the messages exchanged.
- **Runner**: The engine that orchestrates the interaction flow. It takes user input, routes it to the appropriate agent, manages calls to LLM and tools based on the agent's logic, handle session updates via SessionService, and yields events representing the progress of the interaction.

```python
#Session management
#### SessionService -> stores convo history and state
#### InMemorySessionService -> simple , non persistent storage
session_service = InMemorySessionService()
APP_NAME = "weather_tutorial_app"
USER_ID = "user1"
SESSION_ID = "session_001" ###use a fixed id for simplicity
#create session where convo will happen
session = await session_service.create_session(
    app_name = APP_NAME,
    user_id = USER_ID,
    session_id = SESSION_ID
)
print(f"Session created: App='{APP_NAME}', User='{USER_ID}', Session='{SESSION_ID}'")
#---Runner
runner = Runner(
    agent = weather_agent,
    app_name = APP_NAME,
    session_service=session_service
)
print(f"Runner created ofr agent '{runner.agent.name}")
```

### 4. Interact Agent
ADK Runner operates async. We'll define an async helper function (call_agent_async):
1. Take user query string
2. Package that into **ADK Content**
3. Calls **runner.run_async**, providing the user/session context and new messages.
4. Iterates through **Events** yielded by the runner.
5. Identifies and prints the final response event using **event.is_final_response()**

```python
#### Interact with the agent
#will define an async helper function call_agent_async:
from google.genai import types
async def call_agent_async(query:str,runner,user_id,session_id):
  """Sends query to the agent and prints the final response"""
  print(f"\n>>> User Query: {query}")
  #prepare message in ADK Format
  content = types.Content(role = "user",
                          parts = [types.Part(text = query)])
  final_response_text = "Agent didn't produce a final response"
  #key concept: run_async executes the agent logic and yields events
  #we iterate through events to final answer
  async for event in runner.run_async(user_id = user_id, session_id = session_id, new_message = content):
    # You can uncomment the line below to see *all* events during execution
    # print(f" [Event] Author: {event.author}, Type: {type(event).__name__}, Final: {event.is_final_response()}, Content: {event.content}")
    #key concept: is_final_response() marks concluding message
    if event.is_final_response():
      if event.content and event.content.parts:
        #asume text response in the 1st part
        final_response_text = event.content.parts[0].text
      elif event.actions and event.actions.escalate: #handle potential errors
        final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
      break
  print(f"<<< Agent Response: {final_response_text}")
```

### 5. Run Conversation
Finally, lets test our setup by sending few queries to the agent.
We wrap our async calls in a main async function and run it using await
Watch the output:
- See the user queries.
- Notice the `--- Tool: get_weather called... ---` logs when the agent uses the tool.
- Observe the agent's final responses, including how it handles the case where weather data isn't available (for Paris).

```python
# We need an async function to await our interaction helper
async def run_conversation():
    await call_agent_async("What is the weather like in London?",
                                       runner=runner,
                                       user_id=USER_ID,
                                       session_id=SESSION_ID)
    await call_agent_async("How about Paris?",
                                       runner=runner,
                                       user_id=USER_ID,
                                       session_id=SESSION_ID) # Expecting the tool's error message
    await call_agent_async("Tell me the weather in New York",
                                       runner=runner,
                                       user_id=USER_ID,
                                       session_id=SESSION_ID)
# Execute the conversation using await in an async context (like Colab/Jupyter)
await run_conversation()
# --- OR ---
# Uncomment the following lines if running as a standard Python script (.py file):
# import asyncio
# if __name__ == "__main__":
# try:
# asyncio.run(run_conversation())
# except Exception as e:
# print(f"An error occurred: {e}")
```

---

## Agent Team
A more robust approach is to build an **Agent Team**. This involves:
1. Creating multiple, **specialized agents**, each designed for a specific capability (e.g., one for weather, one for greetings, one for calculations).
2. Designating a **root agent** (or orchestrator) that receives the initial user request.
3. Enabling the root agent to **delegate** the request to the most appropriate specialized sub-agent based on the user's intent.

```python
greeting_agent = Agent(
    model = MODEL_GEMINI_2_0_FLASH,
    name = "greeting_agent",
    description = "Provides a simple greeting and hellos using say_hello",
    instruction = "You are the Greeting Agent. Your ONLY task is to provide a friendly greeting to the user. "
                  "Use the 'say_hello' tool to generate the greeting. "
                  "If the user provides their name, make sure to pass it to the tool. "
                  "Do not engage in any other conversation or tasks.",
    tools = [say_hello],
)
farewell_agent = Agent(
    model = MODEL_GEMINI_2_0_FLASH,
    name = "farewell_agent",
    description = "Provides a simple farewell message to conclude the conversation",
    instruction = "You are the Farewell Agent. Your ONLY task is to provide a polite goodbye message. "
                  "Use the 'say_goodbye' tool when the user indicates they are leaving or ending the conversation "
                  "(e.g., using words like 'bye', 'goodbye', 'thanks bye', 'see you'). "
                  "Do not perform any other actions.",
    tools = [say_goodbye],
)
```

```python
root_agent = None
runner_root = None
if greeting_agent and farewell_agent and "get_weather" in globals():
  root_agent_model = MODEL_GEMINI_2_0_FLASH
  weather_agent_team = Agent(
      name = "weather_agent_v2",
      model = root_agent_model,
      description = ("The main coordinator agent. Handles weather requests and delegates greetings/farewells to specialists."),
      instruction = "You are the main Weather Agent coordinating a team. Your primary responsibility is to provide weather information. "
                    "Use the 'get_weather' tool ONLY for specific weather requests (e.g., 'weather in London'). "
                    "You have specialized sub-agents: "
                    "1. 'greeting_agent': Handles simple greetings like 'Hi', 'Hello'. Delegate to it for these. "
                    "2. 'farewell_agent': Handles simple farewells like 'Bye', 'See you'. Delegate to it for these. "
                    "Analyze the user's query. If it's a greeting, delegate to 'greeting_agent'. If it's a farewell, delegate to 'farewell_agent'. "
                    "If it's a weather request, handle it yourself using 'get_weather'. "
                    "For anything else, respond appropriately or state you cannot handle it.",
      tools = [get_weather],
      sub_agents = [greeting_agent,farewell_agent]
  )
 
```

### Interact with the Agent Team
```python
# @title Interact with the Agent Team
import asyncio # Ensure asyncio is imported
# Ensure the root agent (e.g., 'weather_agent_team' or 'root_agent' from the previous cell) is defined.
# Ensure the call_agent_async function is defined.
# Check if the root agent variable exists before defining the conversation function
root_agent_var_name = 'root_agent' # Default name from Step 3 guide
if 'weather_agent_team' in globals(): # Check if user used this name instead
    root_agent_var_name = 'weather_agent_team'
elif 'root_agent' not in globals():
    print("⚠️ Root agent ('root_agent' or 'weather_agent_team') not found. Cannot define run_team_conversation.")
    # Assign a dummy value to prevent NameError later if the code block runs anyway
    root_agent = None # Or set a flag to prevent execution
# Only define and run if the root agent exists
if root_agent_var_name in globals() and globals()[root_agent_var_name]:
    # Define the main async function for the conversation logic.
    # The 'await' keywords INSIDE this function are necessary for async operations.
    async def run_team_conversation():
        print("\n--- Testing Agent Team Delegation ---")
        session_service = InMemorySessionService()
        APP_NAME = "weather_tutorial_agent_team"
        USER_ID = "user_1_agent_team"
        SESSION_ID = "session_001_agent_team"
        session = await session_service.create_session(
            app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
        )
        print(f"Session created: App='{APP_NAME}', User='{USER_ID}', Session='{SESSION_ID}'")
        actual_root_agent = globals()[root_agent_var_name]
        runner_agent_team = Runner( # Or use InMemoryRunner
            agent=actual_root_agent,
            app_name=APP_NAME,
            session_service=session_service
        )
        print(f"Runner created for agent '{actual_root_agent.name}'.")
        # --- Interactions using await (correct within async def) ---
        await call_agent_async(query = "Hello there!",
                               runner=runner_agent_team,
                               user_id=USER_ID,
                               session_id=SESSION_ID)
        await call_agent_async(query = "What is the weather in New York?",
                               runner=runner_agent_team,
                               user_id=USER_ID,
                               session_id=SESSION_ID)
        await call_agent_async(query = "Thanks, bye!",
                               runner=runner_agent_team,
                               user_id=USER_ID,
                               session_id=SESSION_ID)
    # --- Execute the `run_team_conversation` async function ---
    # Choose ONE of the methods below based on your environment.
    # Note: This may require API keys for the models used!
    # METHOD 1: Direct await (Default for Notebooks/Async REPLs)
    # If your environment supports top-level await (like Colab/Jupyter notebooks),
    # it means an event loop is already running, so you can directly await the function.
    print("Attempting execution using 'await' (default for notebooks)...")
    await run_team_conversation()
    # METHOD 2: asyncio.run (For Standard Python Scripts [.py])
    # If running this code as a standard Python script from your terminal,
    # the script context is synchronous. `asyncio.run()` is needed to
    # create and manage an event loop to execute your async function.
    # To use this method:
    # 1. Comment out the `await run_team_conversation()` line above.
    # 2. Uncomment the following block:
    """
    import asyncio
    if __name__ == "__main__": # Ensures this runs only when script is executed directly
        print("Executing using 'asyncio.run()' (for standard Python scripts)...")
        try:
            # This creates an event loop, runs your async function, and closes the loop.
            asyncio.run(run_team_conversation())
        except Exception as e:
            print(f"An error occurred: {e}")
    """
else:
    # This message prints if the root agent variable wasn't found earlier
    print("\n⚠️ Skipping agent team conversation execution as the root agent was not successfully defined in a previous step.")
```

---
## Adding Memory and Personalization with Session State

**What is Session State?**
- It's a Python dictionary (`session.state`) tied to a specific user session (identified by `APP_NAME`, `USER_ID`, `SESSION_ID`).
- It persists information _across multiple conversational turns_ within that session.
- Agents and Tools can read from and write to this state, allowing them to remember details, adapt behavior, and personalize responses.

**How Agents Interact with State:**
1. **`ToolContext` (Primary Method):** Tools can accept a `ToolContext` object (automatically provided by ADK if declared as the last argument). This object gives direct access to the session state via `tool_context.state`, allowing tools to read preferences or save results _during_ execution.
2. **`output_key` (Auto-Save Agent Response):** An `Agent` can be configured with an `output_key="your_key"`. ADK will then automatically save the agent's final textual response for a turn into `session.state["your_key"]`.

**In this step, we will enhance our Weather Bot team by:**
1. Using a **new** `InMemorySessionService` to demonstrate state in isolation.
2. Initializing session state with a user preference for `temperature_unit`.
3. Creating a state-aware version of the weather tool (`get_weather_stateful`) that reads this preference via `ToolContext` and adjusts its output format (Celsius/Fahrenheit).
4. Updating the root agent to use this stateful tool and configuring it with an `output_key` to automatically save its final weather report to the session state.
5. Running a conversation to observe how the initial state affects the tool, how manual state changes alter subsequent behavior, and how `output_key` persists the agent's response.

### 1. Initialize New Session Service and State
```python
from google.adk.sessions import InMemorySessionService
session_service_stateful = InMemorySessionService()
print("✅ New InMemorySessionService created for state demonstration.")
#define new session
SESSION_ID_STATEFUL = "session_state_demo_001"
USER_ID_STATEFUL = "user_state_demo"
initial_state = {
    "user_preference_temperature_unit": "Celsius"
}
session_stateful = await session_service_stateful.create_session(
    app_name = APP_NAME,
    user_id = USER_ID_STATEFUL,
    session_id = SESSION_ID_STATEFUL,
    state = initial_state
)
print(f"✅ Session '{SESSION_ID_STATEFUL}' created for user '{USER_ID_STATEFUL}'.")
#verify initial state
retrieved_session = await session_service_stateful.get_session(
    app_name = APP_NAME,
    user_id = USER_ID_STATEFUL,
    session_id = SESSION_ID_STATEFUL,
)
print("\n--- Initial Session State ---")
if retrieved_session:
    print(retrieved_session.state)
else:
    print("Error: Could not retrieve session.")
```

### 2. Create State-Aware Weather Tool (`get_weather_stateful`)
Now, we create a new version of the weather tool. Its key feature is accepting `tool_context: ToolContext` which allows it to access `tool_context.state`. It will read the `user_preference_temperature_unit` and format the temperature accordingly.
- **Key Concept: `ToolContext`** This object is the bridge allowing your tool logic to interact with the session's context, including reading and writing state variables. ADK injects it automatically if defined as the last parameter of your tool function.
   
- **Best Practice:** When reading from state, use `dictionary.get('key', default_value)` to handle cases where the key might not exist yet, ensuring your tool doesn't crash.

```python
from google.adk.tools.tool_context import ToolContext
def get_weather_stateful(city:str, tool_context: ToolContext) -> dict:
  """Retrieves weather, converts temp unit based on session state."""
  print(f"--- Tool: get_weather_stateful called for {city} ---")
  preferred_unit = tool_context.state.get("user_preference_temperature_unit", "Celsius")
  print(f"--- Tool: Reading state 'user_preference_temperature_unit': {preferred_unit} ---")
  city = city.lower().replace(" ", "")
  mock_weather_db = {
        "newyork": {"temp_c": 25, "condition": "sunny"},
        "london": {"temp_c": 15, "condition": "cloudy"},
        "tokyo": {"temp_c": 18, "condition": "light rain"},
  }
  if city in mock_weather_db:
    data = mock_weather_db[city]
    temp_c = data["temp_c"]
    condition = data["condition"]
    if preferred_unit == "Fahrenheit":
      temp_f = (temp_c * 9/5) + 32
      temp_value = temp_f # Assign temp_f to temp_value
      temp_unit = "F"
    else:
      temp_value = temp_c
      temp_unit = "C"
    report = f"The weather in {city.capitalize()} is {condition} with a temperature of {temp_value:.0f}{temp_unit}."
    result = {"status": "success", "report": report}
    print(f"--- Tool: Generated report in {preferred_unit}. Result: {result} ---")
    # Example of writing back to state (optional for this tool)
    tool_context.state["last_city_checked_stateful"] = city
    print(f"--- Tool: Updated state 'last_city_checked_stateful': {city} ---")
    return result
  else:
    error_msg = f"Sorry, I don't have weather information for '{city}'."
    print(f"--- Tool: City '{city}' not found. ---")
    return {"status": "error", "error_message": error_msg}
print("✅ State-aware 'get_weather_stateful' tool defined.")
```

### 3. Redefine Sub-Agents and Update Root Agent
To ensure this step is self-contained and builds correctly, we first redefine the `greeting_agent` and `farewell_agent` exactly as they were in Step 3. Then, we define our new root agent (`weather_agent_v4_stateful`):
- It uses the new `get_weather_stateful` tool.
- It includes the greeting and farewell sub-agents for delegation.
- **Crucially**, it sets `output_key="last_weather_report"` which automatically saves its final weather response to the session state.

```python
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
greeting_agent = Agent(
    model = MODEL_GEMINI_2_0_FLASH,
    name = "greeting_agent",
    instruction="You are the Greeting Agent. Your ONLY task is to provide a friendly greeting using the 'say_hello' tool. Do nothing else.",
    description="Handles simple greetings and hellos using the 'say_hello' tool.",
    tools=[say_hello],
)
farewell_agent = Agent(
    model=MODEL_GEMINI_2_0_FLASH,
    name="farewell_agent",
    instruction="You are the Farewell Agent. Your ONLY task is to provide a polite goodbye message using the 'say_goodbye' tool. Do not perform any other actions.",
    description="Handles simple farewells and goodbyes using the 'say_goodbye' tool.",
    tools=[say_goodbye],
)
root_agent_stateful = None
runner_root_stateful = None # Initialize runner
if greeting_agent and farewell_agent and 'get_weather_stateful' in globals():
    root_agent_model = MODEL_GEMINI_2_0_FLASH # Choose orchestration model
    root_agent_stateful = Agent(
        name="weather_agent_v4_stateful", # New version name
        model=root_agent_model,
        description="Main agent: Provides weather (state-aware unit), delegates greetings/farewells, saves report to state.",
        instruction="You are the main Weather Agent. Your job is to provide weather using 'get_weather_stateful'. "
                    "The tool will format the temperature based on user preference stored in state. "
                    "Delegate simple greetings to 'greeting_agent' and farewells to 'farewell_agent'. "
                    "Handle only weather requests, greetings, and farewells.",
        tools=[get_weather_stateful], # Use the state-aware tool
        sub_agents=[greeting_agent, farewell_agent], # Include sub-agents
        output_key="last_weather_report" # <<< Auto-save agent's final weather response
    )
    print(f"✅ Root Agent '{root_agent_stateful.name}' created using stateful tool and output_key.")
    # --- Create Runner for this Root Agent & NEW Session Service ---
    runner_root_stateful = Runner(
        agent=root_agent_stateful,
        app_name=APP_NAME,
        session_service=session_service_stateful # Use the NEW stateful session service
    )
    print(f"✅ Runner created for stateful root agent '{runner_root_stateful.agent.name}' using stateful session service.")
```

### 4. Interact and Test State Flow
Now, let's execute a conversation designed to test the state interactions using the `runner_root_stateful` (associated with our stateful agent and the `session_service_stateful`). We'll use the `call_agent_async` function defined earlier, ensuring we pass the correct runner, user ID (`USER_ID_STATEFUL`), and session ID (`SESSION_ID_STATEFUL`).

The conversation flow will be:
1. **Check weather (London):** The `get_weather_stateful` tool should read the initial "Celsius" preference from the session state initialized in Section 1. The root agent's final response (the weather report in Celsius) should get saved to `state['last_weather_report']` via the `output_key` configuration.
2. **Manually update state:** We will _directly modify_ the state stored within the `InMemorySessionService` instance (`session_service_stateful`).
    - **Why direct modification?** The `session_service.get_session()` method returns a _copy_ of the session. Modifying that copy wouldn't affect the state used in subsequent agent runs. For this testing scenario with `InMemorySessionService`, we access the internal `sessions` dictionary to change the _actual_ stored state value for `user_preference_temperature_unit` to "Fahrenheit". _Note: In real applications, state changes are typically triggered by tools or agent logic returning `EventActions(state_delta=...)`, not direct manual updates._
3. **Check weather again (New York):** The `get_weather_stateful` tool should now read the updated "Fahrenheit" preference from the state and convert the temperature accordingly. The root agent's _new_ response (weather in Fahrenheit) will overwrite the previous value in `state['last_weather_report']` due to the `output_key`.
4. **Greet the agent:** Verify that delegation to the `greeting_agent` still works correctly alongside the stateful operations. This interaction will become the _last_ response saved by `output_key` in this specific sequence.
5. **Inspect final state:** After the conversation, we retrieve the session one last time (getting a copy) and print its state to confirm the `user_preference_temperature_unit` is indeed "Fahrenheit", observe the final value saved by `output_key` (which will be the greeting in this run), and see the `last_city_checked_stateful` value written by the tool.

```python
# @title 4. Interact to Test State Flow and output_key
import asyncio # Ensure asyncio is imported
# Ensure the stateful runner (runner_root_stateful) is available from the previous cell
# Ensure call_agent_async, USER_ID_STATEFUL, SESSION_ID_STATEFUL, APP_NAME are defined
if 'runner_root_stateful' in globals() and runner_root_stateful:
    # Define the main async function for the stateful conversation logic.
    # The 'await' keywords INSIDE this function are necessary for async operations.
    async def run_stateful_conversation():
        print("\n--- Testing State: Temp Unit Conversion & output_key ---")
        # 1. Check weather (Uses initial state: Celsius)
        print("--- Turn 1: Requesting weather in London (expect Celsius) ---")
        await call_agent_async(query= "What's the weather in London?",
                               runner=runner_root_stateful,
                               user_id=USER_ID_STATEFUL,
                               session_id=SESSION_ID_STATEFUL
                              )
        # 2. Manually update state preference to Fahrenheit - DIRECTLY MODIFY STORAGE
        print("\n--- Manually Updating State: Setting unit to Fahrenheit ---")
        try:
            # Access the internal storage directly - THIS IS SPECIFIC TO InMemorySessionService for testing
            # NOTE: In production with persistent services (Database, VertexAI), you would
            # typically update state via agent actions or specific service APIs if available,
            # not by direct manipulation of internal storage.
            stored_session = session_service_stateful.sessions[APP_NAME][USER_ID_STATEFUL][SESSION_ID_STATEFUL]
            stored_session.state["user_preference_temperature_unit"] = "Fahrenheit"
            # Optional: You might want to update the timestamp as well if any logic depends on it
            # import time
            # stored_session.last_update_time = time.time()
            print(f"--- Stored session state updated. Current 'user_preference_temperature_unit': {stored_session.state.get('user_preference_temperature_unit', 'Not Set')} ---") # Added .get for safety
        except KeyError:
            print(f"--- Error: Could not retrieve session '{SESSION_ID_STATEFUL}' from internal storage for user '{USER_ID_STATEFUL}' in app '{APP_NAME}' to update state. Check IDs and if session was created. ---")
        except Exception as e:
             print(f"--- Error updating internal session state: {e} ---")
        # 3. Check weather again (Tool should now use Fahrenheit)
        # This will also update 'last_weather_report' via output_key
        print("\n--- Turn 2: Requesting weather in New York (expect Fahrenheit) ---")
        await call_agent_async(query= "Tell me the weather in New York.",
                               runner=runner_root_stateful,
                               user_id=USER_ID_STATEFUL,
                               session_id=SESSION_ID_STATEFUL
                              )
        # 4. Test basic delegation (should still work)
        # This will update 'last_weather_report' again, overwriting the NY weather report
        print("\n--- Turn 3: Sending a greeting ---")
        await call_agent_async(query= "Hi!",
                               runner=runner_root_stateful,
                               user_id=USER_ID_STATEFUL,
                               session_id=SESSION_ID_STATEFUL
                              )
    # --- Execute the `run_stateful_conversation` async function ---
    # Choose ONE of the methods below based on your environment.
    # METHOD 1: Direct await (Default for Notebooks/Async REPLs)
    # If your environment supports top-level await (like Colab/Jupyter notebooks),
    # it means an event loop is already running, so you can directly await the function.
    print("Attempting execution using 'await' (default for notebooks)...")
    await run_stateful_conversation()
    # METHOD 2: asyncio.run (For Standard Python Scripts [.py])
    # If running this code as a standard Python script from your terminal,
    # the script context is synchronous. `asyncio.run()` is needed to
    # create and manage an event loop to execute your async function.
    # To use this method:
    # 1. Comment out the `await run_stateful_conversation()` line above.
    # 2. Uncomment the following block:
    """
    import asyncio
    if __name__ == "__main__": # Ensures this runs only when script is executed directly
        print("Executing using 'asyncio.run()' (for standard Python scripts)...")
        try:
            # This creates an event loop, runs your async function, and closes the loop.
            asyncio.run(run_stateful_conversation())
        except Exception as e:
            print(f"An error occurred: {e}")
    """
    # --- Inspect final session state after the conversation ---
    # This block runs after either execution method completes.
    print("\n--- Inspecting Final Session State ---")
    final_session = await session_service_stateful.get_session(app_name=APP_NAME,
                                                         user_id= USER_ID_STATEFUL,
                                                         session_id=SESSION_ID_STATEFUL)
    if final_session:
        # Use .get() for safer access to potentially missing keys
        print(f"Final Preference: {final_session.state.get('user_preference_temperature_unit', 'Not Set')}")
        print(f"Final Last Weather Report (from output_key): {final_session.state.get('last_weather_report', 'Not Set')}")
        print(f"Final Last City Checked (by tool): {final_session.state.get('last_city_checked_stateful', 'Not Set')}")
        # Print full state for detailed view
        # print(f"Full State Dict: {final_session.state.as_dict()}") # Use as_dict() for clarity
    else:
        print("\n❌ Error: Could not retrieve final session state.")
else:
    print("\n⚠️ Skipping state test conversation. Stateful root agent runner ('runner_root_stateful') is not available.")
```

By reviewing the conversation flow and the final session state printout, you can confirm:
- **State Read:** The weather tool (`get_weather_stateful`) correctly read `user_preference_temperature_unit` from state, initially using "Celsius" for London.
- **State Update:** The direct modification successfully changed the stored preference to "Fahrenheit".
- **State Read (Updated):** The tool subsequently read "Fahrenheit" when asked for New York's weather and performed the conversion.
- **Tool State Write:** The tool successfully wrote the `last_city_checked_stateful` ("New York" after the second weather check) into the state via `tool_context.state`.
- **Delegation:** The delegation to the `greeting_agent` for "Hi!" functioned correctly even after state modifications.
- **`output_key`:** The `output_key="last_weather_report"` successfully saved the root agent's _final_ response for _each turn_ where the root agent was the one ultimately responding. In this sequence, the last response was the greeting ("Hello, there!"), so that overwrote the weather report in the state key.
- **Final State:** The final check confirms the preference persisted as "Fahrenheit".

You've now successfully integrated session state to personalize agent behavior using `ToolContext`, manually manipulated state for testing `InMemorySessionService`, and observed how `output_key` provides a simple mechanism for saving the agent's last response to state. This foundational understanding of state management is key as we proceed to implement safety guardrails using callbacks in the next steps.

---
## Adding Safety - Input Guardrail with `before_model_callback`

Our agent team is becoming more capable, remembering preferences and using tools effectively. However, in real-world scenarios, we often need safety mechanisms to control the agent's behavior _before_ potentially problematic requests even reach the core Large Language Model (LLM).

ADK provides **Callbacks** – functions that allow you to hook into specific points in the agent's execution lifecycle. The `before_model_callback` is particularly useful for input safety.

**What is `before_model_callback`?**

- It's a Python function you define that ADK executes _just before_ an agent sends its compiled request (including conversation history, instructions, and the latest user message) to the underlying LLM.
- **Purpose:** Inspect the request, modify it if necessary, or block it entirely based on predefined rules.

**Common Use Cases:**

- **Input Validation/Filtering:** Check if user input meets criteria or contains disallowed content (like PII or keywords).
- **Guardrails:** Prevent harmful, off-topic, or policy-violating requests from being processed by the LLM.
- **Dynamic Prompt Modification:** Add timely information (e.g., from session state) to the LLM request context just before sending.

**How it Works:**

1. Define a function accepting `callback_context: CallbackContext` and `llm_request: LlmRequest`.
    - `callback_context`: Provides access to agent info, session state (`callback_context.state`), etc.
    - `llm_request`: Contains the full payload intended for the LLM (`contents`, `config`).
2. Inside the function:
    - **Inspect:** Examine `llm_request.contents` (especially the last user message).
    - **Modify (Use Caution):** You _can_ change parts of `llm_request`.
    - **Block (Guardrail):** Return an `LlmResponse` object. ADK will send this response back immediately, _skipping_ the LLM call for that turn.
    - **Allow:** Return `None`. ADK proceeds to call the LLM with the (potentially modified) request.

**In this step, we will:**

1. Define a `before_model_callback` function (`block_keyword_guardrail`) that checks the user's input for a specific keyword ("BLOCK").
2. Update our stateful root agent (`weather_agent_v4_stateful` from Step 4) to use this callback.
3. Create a new runner associated with this updated agent but using the _same stateful session service_ to maintain state continuity.
4. Test the guardrail by sending both normal and keyword-containing requests.

**1. Define the Guardrail Callback Function**

This function will inspect the last user message within the `llm_request` content. If it finds "BLOCK" (case-insensitive), it constructs and returns an `LlmResponse` to block the flow; otherwise, it returns `None`.
```python
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.genai import types # For creating response content
from typing import Optional

def block_keyword_guardrail(
    callback_context: CallbackContext, llm_request:LlmRequest
) -> Optional[LlmResponse]:
  """Inspects the latest usewr message for 'BLOCK'. If found, block the llm call and returns a predefined LlmResponse otherwise , returns None to proceed"""
  agent_name = callback_context.agent_name
  print(f"--- Callback: block_keyword_guardrail running for agent: {agent_name} ---")

  last_user_message_text = ""
  if llm_request.contents:
    #find most recent mesage with role user
    for content in reversed(llm_request.contents):
      if content.role == "user" and content.parts:
        if content.parts[0].text:
          last_user_message_text = content.parts[0].text
          break
  
  print(f"--- Callback: Inspecting last user message: '{last_user_message_text[:100]}...' ---") # Log first 100 chars

  #### Guardrail logic
  keyword_to_block = "BLOCK"
  if keyword_to_block in last_user_message_text.upper():
    print(f"--- Callback: Found '{keyword_to_block}'. Blocking LLM call! ---")

    #optionally set a flag in state 
    callback_context.state["guardrail_block_keyword_triggered"] = True
    print(f"--- Callback: Set state 'guardrail_block_keyword_triggered': True ---")

    return LlmResponse(
        content = types.Content(
            role = "model",
            parts = [types.Part(text = f"I cannot process this request because it contains the blocked keyword '{keyword_to_block}'.")],
        )
    )
  else:
    print(f"--- Callback: Keyword not found. Allowing LLM call for {agent_name}. ---")
    return None

print("✅ block_keyword_guardrail function defined.")
```

**2. Update Root Agent to Use the Callback**
We redefine the root agent, adding the `before_model_callback` parameter and pointing it to our new guardrail function. We'll give it a new version name for clarity.

_Important:_ We need to redefine the sub-agents (`greeting_agent`, `farewell_agent`) and the stateful tool (`get_weather_stateful`) within this context if they are not already available from previous steps, ensuring the root agent definition has access to all its components.
```python
greeting_agent = Agent(
    model=MODEL_GEMINI_2_0_FLASH,
    name="greeting_agent", # Keep original name for consistency
    instruction="You are the Greeting Agent. Your ONLY task is to provide a friendly greeting using the 'say_hello' tool. Do nothing else.",
    description="Handles simple greetings and hellos using the 'say_hello' tool.",
    tools=[say_hello],
)

farewell_agent = Agent(
    model=MODEL_GEMINI_2_0_FLASH,
    name="farewell_agent", # Keep original name
    instruction="You are the Farewell Agent. Your ONLY task is to provide a polite goodbye message using the 'say_goodbye' tool. Do not perform any other actions.",
    description="Handles simple farewells and goodbyes using the 'say_goodbye' tool.",
    tools=[say_goodbye],
)

# --- Define the Root Agent with the Callback ---
root_agent_model_guardrail = None
runner_root_model_guardrail = None

# Check all components before proceeding
if greeting_agent and farewell_agent and 'get_weather_stateful' in globals() and 'block_keyword_guardrail' in globals():

    # Use a defined model constant
    root_agent_model = MODEL_GEMINI_2_0_FLASH

    root_agent_model_guardrail = Agent(
        name="weather_agent_v5_model_guardrail", # New version name for clarity
        model=root_agent_model,
        description="Main agent: Handles weather, delegates greetings/farewells, includes input keyword guardrail.",
        instruction="You are the main Weather Agent. Provide weather using 'get_weather_stateful'. "
                    "Delegate simple greetings to 'greeting_agent' and farewells to 'farewell_agent'. "
                    "Handle only weather requests, greetings, and farewells.",
        tools=[get_weather],
        sub_agents=[greeting_agent, farewell_agent], # Reference the redefined sub-agents
        output_key="last_weather_report", # Keep output_key from Step 4
        before_model_callback=block_keyword_guardrail # <<< Assign the guardrail callback
    )
    print(f"✅ Root Agent '{root_agent_model_guardrail.name}' created with before_model_callback.")

    # --- Create Runner for this Agent, Using SAME Stateful Session Service ---
    # Ensure session_service_stateful exists from Step 4
    if 'session_service_stateful' in globals():
        runner_root_model_guardrail = Runner(
            agent=root_agent_model_guardrail,
            app_name=APP_NAME, # Use consistent APP_NAME
            session_service=session_service_stateful # <<< Use the service from Step 4
        )
        print(f"✅ Runner created for guardrail agent '{runner_root_model_guardrail.agent.name}', using stateful session service.")
    else:
        print("❌ Cannot create runner. 'session_service_stateful' from Step 4 is missing.")
```

**3. Interact to Test the Guardrail**
Let's test the guardrail's behavior. We'll use the _same session_ (`SESSION_ID_STATEFUL`) as in Step 4 to show that state persists across these changes.

1. Send a normal weather request (should pass the guardrail and execute).
2. Send a request containing "BLOCK" (should be intercepted by the callback).
3. Send a greeting (should pass the root agent's guardrail, be delegated, and execute normally).
```python
# @title 3. Interact to Test the Model Input Guardrail
import asyncio # Ensure asyncio is imported

# Ensure the runner for the guardrail agent is available
if 'runner_root_model_guardrail' in globals() and runner_root_model_guardrail:
    # Define the main async function for the guardrail test conversation.
    # The 'await' keywords INSIDE this function are necessary for async operations.
    async def run_guardrail_test_conversation():
        print("\n--- Testing Model Input Guardrail ---")

        # Use the runner for the agent with the callback and the existing stateful session ID
        # Define a helper lambda for cleaner interaction calls
        interaction_func = lambda query: call_agent_async(query,
                                                         runner_root_model_guardrail,
                                                         USER_ID_STATEFUL, # Use existing user ID
                                                         SESSION_ID_STATEFUL # Use existing session ID
                                                        )
        # 1. Normal request (Callback allows, should use Fahrenheit from previous state change)
        print("--- Turn 1: Requesting weather in London (expect allowed, Fahrenheit) ---")
        await interaction_func("What is the weather in London?")

        # 2. Request containing the blocked keyword (Callback intercepts)
        print("\n--- Turn 2: Requesting with blocked keyword (expect blocked) ---")
        await interaction_func("BLOCK the request for weather in Tokyo") # Callback should catch "BLOCK"

        # 3. Normal greeting (Callback allows root agent, delegation happens)
        print("\n--- Turn 3: Sending a greeting (expect allowed) ---")
        await interaction_func("Hello again")

    # --- Execute the `run_guardrail_test_conversation` async function ---
    # Choose ONE of the methods below based on your environment.

    # METHOD 1: Direct await (Default for Notebooks/Async REPLs)
    # If your environment supports top-level await (like Colab/Jupyter notebooks),
    # it means an event loop is already running, so you can directly await the function.
    print("Attempting execution using 'await' (default for notebooks)...")
    await run_guardrail_test_conversation()

    # METHOD 2: asyncio.run (For Standard Python Scripts [.py])
    # If running this code as a standard Python script from your terminal,
    # the script context is synchronous. `asyncio.run()` is needed to
    # create and manage an event loop to execute your async function.
    # To use this method:
    # 1. Comment out the `await run_guardrail_test_conversation()` line above.
    # 2. Uncomment the following block:
    """
    import asyncio
    if __name__ == "__main__": # Ensures this runs only when script is executed directly
        print("Executing using 'asyncio.run()' (for standard Python scripts)...")
        try:
            # This creates an event loop, runs your async function, and closes the loop.
            asyncio.run(run_guardrail_test_conversation())
        except Exception as e:
            print(f"An error occurred: {e}")
    """

    # --- Inspect final session state after the conversation ---
    # This block runs after either execution method completes.
    # Optional: Check state for the trigger flag set by the callback
    print("\n--- Inspecting Final Session State (After Guardrail Test) ---")
    # Use the session service instance associated with this stateful session
    final_session = await session_service_stateful.get_session(app_name=APP_NAME,
                                                         user_id=USER_ID_STATEFUL,
                                                         session_id=SESSION_ID_STATEFUL)
    if final_session:
        # Use .get() for safer access
        print(f"Guardrail Triggered Flag: {final_session.state.get('guardrail_block_keyword_triggered', 'Not Set (or False)')}")
        print(f"Last Weather Report: {final_session.state.get('last_weather_report', 'Not Set')}") # Should be London weather if successful
        print(f"Temperature Unit: {final_session.state.get('user_preference_temperature_unit', 'Not Set')}") # Should be Fahrenheit
        # print(f"Full State Dict: {final_session.state.as_dict()}") # For detailed view
    else:
        print("\n❌ Error: Could not retrieve final session state.")

else:
    print("\n⚠️ Skipping model guardrail test. Runner ('runner_root_model_guardrail') is not available.")
```

Observe the execution flow:

1. **London Weather:** The callback runs for `weather_agent_v5_model_guardrail`, inspects the message, prints "Keyword not found. Allowing LLM call.", and returns `None`. The agent proceeds, calls the `get_weather_stateful` tool (which uses the "Fahrenheit" preference from Step 4's state change), and returns the weather. This response updates `last_weather_report` via `output_key`.
2. **BLOCK Request:** The callback runs again for `weather_agent_v5_model_guardrail`, inspects the message, finds "BLOCK", prints "Blocking LLM call!", sets the state flag, and returns the predefined `LlmResponse`. The agent's underlying LLM is _never called_ for this turn. The user sees the callback's blocking message.
3. **Hello Again:** The callback runs for `weather_agent_v5_model_guardrail`, allows the request. The root agent then delegates to `greeting_agent`. _Note: The `before_model_callback` defined on the root agent does NOT automatically apply to sub-agents._ The `greeting_agent` proceeds normally, calls its `say_hello` tool, and returns the greeting.

You have successfully implemented an input safety layer! The `before_model_callback` provides a powerful mechanism to enforce rules and control agent behavior _before_ expensive or potentially risky LLM calls are made. Next, we'll apply a similar concept to add guardrails around tool usage itself.

---
## Adding Safety - Tool Argument Guardrail (`before_tool_callback`)

In Step 5, we added a guardrail to inspect and potentially block user input _before_ it reached the LLM. Now, we'll add another layer of control _after_ the LLM has decided to use a tool but _before_ that tool actually executes. This is useful for validating the _arguments_ the LLM wants to pass to the tool.

ADK provides the `before_tool_callback` for this precise purpose.

**What is `before_tool_callback`?**

- It's a Python function executed just _before_ a specific tool function runs, after the LLM has requested its use and decided on the arguments.
- **Purpose:** Validate tool arguments, prevent tool execution based on specific inputs, modify arguments dynamically, or enforce resource usage policies.

**Common Use Cases:**

- **Argument Validation:** Check if arguments provided by the LLM are valid, within allowed ranges, or conform to expected formats.
- **Resource Protection:** Prevent tools from being called with inputs that might be costly, access restricted data, or cause unwanted side effects (e.g., blocking API calls for certain parameters).
- **Dynamic Argument Modification:** Adjust arguments based on session state or other contextual information before the tool runs.

**How it Works:**

1. Define a function accepting `tool: BaseTool`, `args: Dict[str, Any]`, and `tool_context: ToolContext`.
    - `tool`: The tool object about to be called (inspect `tool.name`).
    - `args`: The dictionary of arguments the LLM generated for the tool.
    - `tool_context`: Provides access to session state (`tool_context.state`), agent info, etc.
2. Inside the function:
    - **Inspect:** Examine the `tool.name` and the `args` dictionary.
    - **Modify:** Change values within the `args` dictionary _directly_. If you return `None`, the tool runs with these modified args.
    - **Block/Override (Guardrail):** Return a **dictionary**. ADK treats this dictionary as the _result_ of the tool call, completely _skipping_ the execution of the original tool function. The dictionary should ideally match the expected return format of the tool it's blocking.
    - **Allow:** Return `None`. ADK proceeds to execute the actual tool function with the (potentially modified) arguments.

**In this step, we will:**

1. Define a `before_tool_callback` function (`block_paris_tool_guardrail`) that specifically checks if the `get_weather_stateful` tool is called with the city "Paris".
2. If "Paris" is detected, the callback will block the tool and return a custom error dictionary.
3. Update our root agent (`weather_agent_v6_tool_guardrail`) to include _both_ the `before_model_callback` and this new `before_tool_callback`.
4. Create a new runner for this agent, using the same stateful session service.
5. Test the flow by requesting weather for allowed cities and the blocked city ("Paris").

**1. Define the Tool Guardrail Callback Function**
This function targets the `get_weather_stateful` tool. It checks the `city` argument. If it's "Paris", it returns an error dictionary that looks like the tool's own error response. Otherwise, it allows the tool to run by returning `None`.
```python
from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext
from typing import Optional, Dict, Any # For type hints

def block_paris_tool_guardrail(
    tool:BaseTool, args: Dict[str,Any], tool_context: ToolContext
) -> Optional[Dict]:
  """
  Checks if 'get_weather_stateful' is called for 'Paris'.
  If so, blocks the tool execution and returns a specific error dictionary.
  Otherwise, allows the tool call to proceed by returning None.
  """
  tool_name = tool.name
  agent_name = tool_context.agent_name
  print(f"--- Callback: block_paris_tool_guardrail running for tool '{tool_name}' in agent '{agent_name}' ---")
  print(f"--- Callback: Inspecting args: {args} ---")

  #guardlogic 
  target_tool_name = "get_weather_stateful"
  blocked_city = "paris"

  if tool_name == target_tool_name:
    city_arg = args.get("city","")
    if city_arg and city_arg.lower() == blocked_city:
      print(f"--- Callback: Detected blocked city '{city_arg}'. Blocking tool execution! ---")
      # Optionally update state
      tool_context.state["guardrail_tool_block_triggered"] = True
      print(f"--- Callback: Set state 'guardrail_tool_block_triggered': True ---")

      return {
                "status": "error",
                "error_message": f"Policy restriction: Weather checks for '{city_arg.capitalize()}' are currently disabled by a tool guardrail."
            }
    else:
        print(f"--- Callback: City '{city_arg}' is allowed for tool '{tool_name}'. ---")
  else:
      print(f"--- Callback: Tool '{tool_name}' is not the target tool. Allowing. ---")


  # If the checks above didn't return a dictionary, allow the tool to execute
  print(f"--- Callback: Allowing tool '{tool_name}' to proceed. ---")
  return None # Returning None allows the actual tool function to run

print("✅ block_paris_tool_guardrail function defined.")
```

**2. Update Root Agent to Use Both Callbacks**
We redefine the root agent again (`weather_agent_v6_tool_guardrail`), this time adding the `before_tool_callback` parameter alongside the `before_model_callback` from Step 5.

_Self-Contained Execution Note:_ Similar to Step 5, ensure all prerequisites (sub-agents, tools, `before_model_callback`) are defined or available in the execution context before defining this agent.
```python
greeting_agent = Agent(
    model=MODEL_GEMINI_2_0_FLASH,
    name="greeting_agent", # Keep original name for consistency
    instruction="You are the Greeting Agent. Your ONLY task is to provide a friendly greeting using the 'say_hello' tool. Do nothing else.",
    description="Handles simple greetings and hellos using the 'say_hello' tool.",
    tools=[say_hello],
)

farewell_agent = Agent(
    model=MODEL_GEMINI_2_0_FLASH,
    name="farewell_agent", # Keep original name
    instruction="You are the Farewell Agent. Your ONLY task is to provide a polite goodbye message using the 'say_goodbye' tool. Do not perform any other actions.",
    description="Handles simple farewells and goodbyes using the 'say_goodbye' tool.",
    tools=[say_goodbye],
)

# --- Define the Root Agent with Both Callbacks ---
root_agent_tool_guardrail = None
runner_root_tool_guardrail = None

if ('greeting_agent' in globals() and greeting_agent and
    'farewell_agent' in globals() and farewell_agent and
    'get_weather_stateful' in globals() and
    'block_keyword_guardrail' in globals() and
    'block_paris_tool_guardrail' in globals()):

    root_agent_model = MODEL_GEMINI_2_0_FLASH

    root_agent_tool_guardrail = Agent(
        name="weather_agent_v6_tool_guardrail", # New version name
        model=root_agent_model,
        description="Main agent: Handles weather, delegates, includes input AND tool guardrails.",
        instruction="You are the main Weather Agent. Provide weather using 'get_weather_stateful'. "
                    "Delegate greetings to 'greeting_agent' and farewells to 'farewell_agent'. "
                    "Handle only weather, greetings, and farewells.",
        tools=[get_weather_stateful],
        sub_agents=[greeting_agent, farewell_agent],
        output_key="last_weather_report",
        before_model_callback=block_keyword_guardrail, # Keep model guardrail
        before_tool_callback=block_paris_tool_guardrail # <<< Add tool guardrail
    )
    print(f"✅ Root Agent '{root_agent_tool_guardrail.name}' created with BOTH callbacks.")

    # --- Create Runner, Using SAME Stateful Session Service ---
    if 'session_service_stateful' in globals():
        runner_root_tool_guardrail = Runner(
            agent=root_agent_tool_guardrail,
            app_name=APP_NAME,
            session_service=session_service_stateful # <<< Use the service from Step 4/5
        )
        print(f"✅ Runner created for tool guardrail agent '{runner_root_tool_guardrail.agent.name}', using stateful session service.")
    else:
        print("❌ Cannot create runner. 'session_service_stateful' from Step 4/5 is missing.")

else:
    print("❌ Cannot create root agent with tool guardrail. Prerequisites missing.")
```

**3. Interact to Test the Tool Guardrail**
Let's test the interaction flow, again using the same stateful session (`SESSION_ID_STATEFUL`) from the previous steps.

1. Request weather for "New York": Passes both callbacks, tool executes (using Fahrenheit preference from state).
2. Request weather for "Paris": Passes `before_model_callback`. LLM decides to call `get_weather_stateful(city='Paris')`. `before_tool_callback` intercepts, blocks the tool, and returns the error dictionary. Agent relays this error.
3. Request weather for "London": Passes both callbacks, tool executes normally.

```python
# @title 3. Interact to Test the Tool Argument Guardrail
import asyncio # Ensure asyncio is imported

# Ensure the runner for the tool guardrail agent is available
if 'runner_root_tool_guardrail' in globals() and runner_root_tool_guardrail:
    # Define the main async function for the tool guardrail test conversation.
    # The 'await' keywords INSIDE this function are necessary for async operations.
    async def run_tool_guardrail_test():
        print("\n--- Testing Tool Argument Guardrail ('Paris' blocked) ---")

        # Use the runner for the agent with both callbacks and the existing stateful session
        # Define a helper lambda for cleaner interaction calls
        interaction_func = lambda query: call_agent_async(query,
                                                         runner_root_tool_guardrail,
                                                         USER_ID_STATEFUL, # Use existing user ID
                                                         SESSION_ID_STATEFUL # Use existing session ID
                                                        )
        # 1. Allowed city (Should pass both callbacks, use Fahrenheit state)
        print("--- Turn 1: Requesting weather in New York (expect allowed) ---")
        await interaction_func("What's the weather in New York?")

        # 2. Blocked city (Should pass model callback, but be blocked by tool callback)
        print("\n--- Turn 2: Requesting weather in Paris (expect blocked by tool guardrail) ---")
        await interaction_func("How about Paris?") # Tool callback should intercept this

        # 3. Another allowed city (Should work normally again)
        print("\n--- Turn 3: Requesting weather in London (expect allowed) ---")
        await interaction_func("Tell me the weather in London.")

    # --- Execute the `run_tool_guardrail_test` async function ---
    # Choose ONE of the methods below based on your environment.

    # METHOD 1: Direct await (Default for Notebooks/Async REPLs)
    # If your environment supports top-level await (like Colab/Jupyter notebooks),
    # it means an event loop is already running, so you can directly await the function.
    print("Attempting execution using 'await' (default for notebooks)...")
    await run_tool_guardrail_test()

    # METHOD 2: asyncio.run (For Standard Python Scripts [.py])
    # If running this code as a standard Python script from your terminal,
    # the script context is synchronous. `asyncio.run()` is needed to
    # create and manage an event loop to execute your async function.
    # To use this method:
    # 1. Comment out the `await run_tool_guardrail_test()` line above.
    # 2. Uncomment the following block:
    """
    import asyncio
    if __name__ == "__main__": # Ensures this runs only when script is executed directly
        print("Executing using 'asyncio.run()' (for standard Python scripts)...")
        try:
            # This creates an event loop, runs your async function, and closes the loop.
            asyncio.run(run_tool_guardrail_test())
        except Exception as e:
            print(f"An error occurred: {e}")
    """

    # --- Inspect final session state after the conversation ---
    # This block runs after either execution method completes.
    # Optional: Check state for the tool block trigger flag
    print("\n--- Inspecting Final Session State (After Tool Guardrail Test) ---")
    # Use the session service instance associated with this stateful session
    final_session = await session_service_stateful.get_session(app_name=APP_NAME,
                                                         user_id=USER_ID_STATEFUL,
                                                         session_id= SESSION_ID_STATEFUL)
    if final_session:
        # Use .get() for safer access
        print(f"Tool Guardrail Triggered Flag: {final_session.state.get('guardrail_tool_block_triggered', 'Not Set (or False)')}")
        print(f"Last Weather Report: {final_session.state.get('last_weather_report', 'Not Set')}") # Should be London weather if successful
        print(f"Temperature Unit: {final_session.state.get('user_preference_temperature_unit', 'Not Set')}") # Should be Fahrenheit
        # print(f"Full State Dict: {final_session.state.as_dict()}") # For detailed view
    else:
        print("\n❌ Error: Could not retrieve final session state.")

else:
    print("\n⚠️ Skipping tool guardrail test. Runner ('runner_root_tool_guardrail') is not available.")
```

Analyze the output:

1. **New York:** The `before_model_callback` allows the request. The LLM requests `get_weather_stateful`. The `before_tool_callback` runs, inspects the args (`{'city': 'New York'}`), sees it's not "Paris", prints "Allowing tool..." and returns `None`. The actual `get_weather_stateful` function executes, reads "Fahrenheit" from state, and returns the weather report. The agent relays this, and it gets saved via `output_key`.
2. **Paris:** The `before_model_callback` allows the request. The LLM requests `get_weather_stateful(city='Paris')`. The `before_tool_callback` runs, inspects the args, detects "Paris", prints "Blocking tool execution!", sets the state flag, and returns the error dictionary `{'status': 'error', 'error_message': 'Policy restriction...'}`. The actual `get_weather_stateful` function is **never executed**. The agent receives the error dictionary _as if it were the tool's output_ and formulates a response based on that error message.
3. **London:** Behaves like New York, passing both callbacks and executing the tool successfully. The new London weather report overwrites the `last_weather_report` in the state.

You've now added a crucial safety layer controlling not just _what_ reaches the LLM, but also _how_ the agent's tools can be used based on the specific arguments generated by the LLM. Callbacks like `before_model_callback` and `before_tool_callback` are essential for building robust, safe, and policy-compliant agent applications.