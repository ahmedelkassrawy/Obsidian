#### Basic Agent
```python
import os
import asyncio
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.llms.google_genai import GoogleGenAI
import os
os.environ["GOOGLE_API_KEY"] = "AIzaSyD7uibWj-CX1j7ljL_jTI1ZkpRniROzk1o"


llm = GoogleGenAI( # Use the new class name
    model="models/gemini-2.0-flash",
    api_key = os.getenv("GOOGLE_API_KEY")
)

def multiply(a:float,b:float) -> float:
  """Useful for multiplying two numbers."""
  return a * b

agent = FunctionAgent(
    tools = [multiply],
    llm = llm,
    system_prompt = "You are a helpful assistant that can multiply two numbers",
    streaming=False # Disable streaming
)

async def main():
    response = await agent.run("What is 1234 * 4567?")
    print(str(response))


# Run the agent
if __name__ == "__main__":
    asyncio.run(main())
```

#### Adding Chat History
The `AgentWorkflow` is also able to remember previous messages. This is contained inside the `Context` of the `AgentWorkflow`.

If the `Context` is passed in, the agent will use it to continue the conversation.
```python
from llama_index.core.workflow import Context

# create context
ctx = Context(agent)

# run agent with context
response = await agent.run("My name is Logan", ctx=ctx)
response = await agent.run("What is my name?", ctx=ctx)
```

```python
import os
import asyncio
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.core.workflow import Context
import os
os.environ["GOOGLE_API_KEY"] = "AIzaSyD7uibWj-CX1j7ljL_jTI1ZkpRniROzk1o"

llm = GoogleGenAI( # Use the new class name
    model="models/gemini-2.0-flash",
    api_key = os.getenv("GOOGLE_API_KEY")
)

def multiply(a:float,b:float) -> float:
  """Useful for multiplying two numbers."""
  return a * b

agent = FunctionAgent(
    tools = [multiply],
    llm = llm,
    system_prompt = "You are a helpful assistant that can multiply two numbers",
    streaming=False # Disable streaming
)

ctx = Context(agent)

async def main():
    response = await agent.run("My name is Logan",ctx = ctx)
    response = await agent.run("What is my name?", ctx=ctx)
    print(str(response))


# Run the agent
if __name__ == "__main__":
    asyncio.run(main())
```

#### Basic RAG
```python
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from google.genai.types import EmbedContentConfig
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.core.workflow import Context
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings

os.environ["GOOGLE_API_KEY"] = "AIzaSyD7uibWj-CX1j7ljL_jTI1ZkpRniROzk1o"

llm = GoogleGenAI( # Use the new class name
    model="models/gemini-2.0-flash",
    api_key = os.getenv("GOOGLE_API_KEY")
)

embed_model = GoogleGenAIEmbedding(
    model_name="text-embedding-004",
    api_key = os.getenv("GOOGLE_API_KEY"),
)

# Set embedding model and LLM in Settings
Settings.embed_model = embed_model
Settings.llm = llm

#RAG Setup
docs = SimpleDirectoryReader(data_dir).load_data()
index = VectorStoreIndex.from_documents(docs)
query_engine = index.as_query_engine()

async def search_documents(query:str) -> str:
    """Useful for answering natural language questions about a personal essay written by Paul Graham."""

    response = await query_engine.aquery(query)
    return str(response)
    
agent = FunctionAgent(
    tools = [multiply,search_documents],
    llm = llm,
    system_prompt = """You are a helpful assistant that can perform calculations
    and search through documents to answer questions.""",
    streaming=True
)

async def main():
    response = await agent.run(
        "What did the author do in college? Also, what's 7 * 8?"
    )
    print(response)
    
if __name__ == "__main__":

    asyncio.run(main())
```

#### Concepts
[**Structured Data Extraction**](https://developers.llamaindex.ai/python/framework/use_cases/extraction) Pydantic extractors allow you to specify a precise data structure to extract from your data and use LLMs to fill in the missing pieces in a type-safe way. This is useful for extracting structured data from unstructured sources like PDFs, websites, and more, and is key to automating workflows.

[**Query Engines**](https://developers.llamaindex.ai/python/framework/module_guides/deploying/query_engine): A query engine is an end-to-end flow that allows you to ask questions over your data. It takes in a natural language query, and returns a response, along with reference context retrieved and passed to the LLM.
## Usage Pattern

Get started with:

```python
query_engine = index.as_query_engine()
response = query_engine.query("Who is Paul Graham.")
```

To stream response:

```python
query_engine = index.as_query_engine(streaming=True)
streaming_response = query_engine.query("Who is Paul Graham.")
streaming_response.print_response_stream()
```

[**Chat Engines**](https://developers.llamaindex.ai/python/framework/module_guides/deploying/chat_engines): A chat engine is an end-to-end flow for having a conversation with your data (multiple back-and-forth instead of a single question-and-answer).

## Usage Pattern

Get started with:

```python
chat_engine = index.as_chat_engine()
response = chat_engine.chat("Tell me a joke.")
```

To stream response:

```python
chat_engine = index.as_chat_engine()
streaming_response = chat_engine.stream_chat("Tell me a joke.")
for token in streaming_response.response_gen:    
	print(token, end="")
```

#### Basic Tool creation 
```python
def multiply(a:float,b:float) -> float:
    """Multiply two numbers and return the result."""
    return a * b

def add(a:float,b:float) -> float:
    """Add two numbers and return the result."""
    return a + b  
    
agent = FunctionAgent(
    tools = [multiply, add],
    llm = llm,
    verbose = False,
    system_prompt = "You are an agent that can perform basic mathematical operations using tools.",
    streaming = True,
)
```

#### Using an exisiting tool from LlamaHub
```python
pip install llama-index-tools-yahoo-finance

from llama_index.tools.yahoo_finance import YahooFinanceToolSpec
```

```python
tools = YahooFinanceToolSpec().to_tool_list()
```
A tool list is just an array, so we can use Python’s `extend` method to add our own tools to the mix:
```python
tools.extend([multiply, add])
```

and just as usual initializing the agent:
```python
agent = FunctionAgent(
    tools = tools,
    description = "Useful for performing financial operations",
    llm = llm,
    verbose = False,
    system_prompt = "You are an agent that can perform basic mathematical operations and finance using tools.",
    streaming = True,
)
```

Building Your Own Tool:
- - A class that extends `BaseToolSpec`
- - A set of arbitrary Python functions
- - A `spec_functions` list that maps the functions to the tool’s API

```python
class YahooFinanceToolSpec(BaseToolSpec):
    """Yahoo Finance tool spec."""

    spec_functions = [
        "balance_sheet",
        "income_statement",
        "cash_flow",
        "stock_basic_info",
        "stock_analyst_recommendations",
        "stock_news",
    ]

    def __init__(self) -> None:
        """Initialize the Yahoo Finance tool spec."""

    def balance_sheet(self, ticker: str) -> str:
		"""
        Return the balance sheet of the stock.

        Args:
          ticker (str): the stock ticker to be given to yfinance

        """
        stock = yf.Ticker(ticker)
        balance_sheet = pd.DataFrame(stock.balance_sheet)
        return "Balance Sheet: \n" + balance_sheet.to_string()

    def income_statement(self, ticker: str) -> str:
        """
        Return the income statement of the stock.

        Args:
          ticker (str): the stock ticker to be given to yfinance

        """
```

#### Maintaining State
```python
from llama_index.core.workflow import Context
```
we’ll create a new Context called ctx. We pass in our workflow to properly configure this Context object for the workflow that will use it.
```python
ctx = Context(agent)
```
With our configured Context, we can pass it to our first run.
```python
response = await agent.run(user_msg="Hi, my name is Laurie!", ctx=ctx)
print(response)
```

#### Maintaining state over longer periods
- The Context is serializable, so it can be saved to a database, file, etc. and loaded back in later.
- The JsonSerializer is a simple serializer that uses `json.dumps` and `json.loads` to serialize and deserialize the context.
- The JsonPickleSerializer is a serializer that uses pickle to serialize and deserialize the context. If you have objects in your context that are not serializable, you can use this serializer.
```python
from llama_index.core.workflow import JsonPickleSerializer, JsonSerializer
```

We can then serialize our context to a dictionary and save it to a file:
```python
ctx_dict = ctx.to_dict(serializer=JsonSerializer())
```

We can deserialize it back into a Context object and ask questions just as before:
```python
restored_ctx = Context.from_dict(
    workflow, ctx_dict, serializer=JsonSerializer()
)

response3 = await workflow.run(user_msg="What's my name?", ctx=restored_ctx)
```

Whole Code:
```python
agent = FunctionAgent(
    tools = tools,
    description = "Useful for performing financial operations",
    llm = llm,
    verbose = False,
    system_prompt = "You are an agent that can perform basic mathematical operations and finance using tools.",
    streaming = True,
)

async def main():
    response = await agent.run(user_msg = "What's the current stock price of NVIDIA?",ctx = restored_ctx)
    print(response)

    ctx = Context(agent)
    ctx_dict = ctx.to_dict(serializer = JsonSerializer())
    restored_ctx = Context.from_dict(
        agent, 
        ctx_dict, 
        serializer=JsonSerializer()
    )

if __name__ == "__main__":
    asyncio.run(main())
```

#### Tools and State
- Tools can also be defined that have access to the workflow context.
- This means you can set and retrieve variables from the context and use them in the tool, or to pass information between tools.
- `AgentWorkflow` uses a context variable called `state` that is available to every agent.
- You can rely on information in `state` being available without explicitly having to pass it in.

To access the Context, the Context parameter should be the first parameter of the tool, as we’re doing here, in a tool that simply adds a name to the state:
```python
async def set_name(ctx: Context, name: str) -> str:
    async with ctx.store.edit_state() as ctx_state:
        ctx_state["state"]["name"] = name

    return f"Name set to {name}"
```

We can now create an agent that uses this tool. You can optionally provide the initial state of the agent, which we’ll do here:

```python
workflow = AgentWorkflow.from_tools_or_functions(
    [set_name],
    llm=llm,
    system_prompt="You are a helpful assistant that can set a name.",
    initial_state={"name": "unset"},
)
```

Now we can create a Context and ask the agent about the state:
```python
ctx = Context(workflow)

# check if it knows a name before setting it
response = await workflow.run(user_msg="What's my name?", ctx=ctx)
print(str(response))
```

```python
Your name has been set to "unset."
```

Then we can explicitly set the name in a new run of the agent:

```python
response2 = await workflow.run(user_msg="My name is Laurie", ctx=ctx)
print(str(response2))
```

```python
Your name has been updated to "Laurie."
```

We could now ask the agent the name again, or we can access the value of the state directly:

```python
state = await ctx.store.get("state")
print("Name as stored in state: ", state["name"])
```

Which gives us:

```python
Name as stored in state: Laurie
```

#### Streaming Output and events
- In real-world use, agents can take a long time to run.
- Providing feedback to the user about the progress of the agent is critical, and streaming allows you to do that.
- `AgentWorkflow` provides a set of pre-built events that you can use to stream output to the user.
In previous examples, we’ve used `await` on the `workflow.run` method to get the final response from the agent. However, if we don’t await the response, we get an asynchronous iterator back that we can iterate over to get the events as they come in. This iterator will return all sorts of events. We’ll start with an `AgentStream` event, which contains the “delta” (the most recent change) to the output as it comes in. We’ll need to import that event type:

```python
from llama_index.core.agent.workflow import AgentStream
from llama_index.core.agent.workflow import (
    AgentInput,
    AgentOutput,
    ToolCall,
    ToolCallResult,
    AgentStream,
)
```

```python
tools = TavilyToolSpec(api_key = os.getenv("TAVILY_API_KEY")).to_tool_list()
tools.extend([multiply, add])

agent = FunctionAgent(
    llm = llm,
    tools = tools,
    system_prompt = "You're a helpful assistant that can search the web for information. and also have basic mathematical capabilities.",
)

async def main():
    handler = agent.run(user_msg = "What's the weather like in San Francisco?")

    async for event in handler.stream_events():
        if isinstance(event,AgentStream):
            print(event.delta, end="", flush=True)
        elif isinstance(event,AgentInput):
            print("Agent input:",event.input)
            print("Agent name:",event.current_agent_name)
        elif isinstance(event,AgentOutput):
            print("Agent output:",event.response)
            print("Tool calls made:",event.tool_calls)
            print("RAW LLM Response:",event.raw)
        elif isinstance(event,ToolCallResult):
            print("Tool called:",event.tool_name)
            print("Arguments to the tool:",event.tool_kwargs)
            print("Tool Output:",event.tool_output)

    print(str(await handler))

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

`AgentStream` is just one of many events that `AgentWorkflow` emits as it runs. The others are:

- `AgentInput`: the full message object that begins the agent’s execution
- `AgentOutput`: the response from the agent
- `ToolCall`: which tools were called and with what arguments
- `ToolCallResult`: the result of a tool call

```python
async def main():
    handler = agent.run(user_msg = "What's the weather like in San Francisco?")

    async for event in handler.stream_events():
        if isinstance(event,AgentStream):
            print(event.delta, end="", flush=True)

    print(str(await handler))

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

If you run this yourself, you will see the output arriving in chunks as the agent runs, returning something like this:

```python
The current weather in San Francisco is as follows:

- **Temperature**: 17.2°C (63°F)
- **Condition**: Sunny
- **Wind**: 6.3 mph (10.1 kph) from the NNW
- **Humidity**: 54%
- **Pressure**: 1021 mb (30.16 in)
- **Visibility**: 16 km (9 miles)

For more details, you can check the full report [here](https://www.weatherapi.com/).
```

#### Human in the loop
To get a human in the loop, we’ll get our tool to emit an event that isn’t received by any other step in the workflow.
We’ll then tell our tool to wait until it receives a specific “reply” event.

We have built-in `InputRequiredEvent` and `HumanResponseEvent` events to use for this purpose. If you want to capture different forms of human input, you can subclass these events to match your own preferences.
```python
from llama_index.core.workflow import (
    InputRequiredEvent,
    HumanResponseEvent,
)
```
Next we’ll create a tool that performs a hypothetical dangerous task. There are a couple of new things happening here:

- `wait_for_event` is used to wait for a HumanResponseEvent.
- The `waiter_event` is the event that is written to the event stream, to let the caller know that we’re waiting for a response.
- `waiter_id` is a unique identifier for this specific wait call. It helps ensure that we only send one `waiter_event` for each `waiter_id`.
- The `requirements` argument is used to specify that we want to wait for a HumanResponseEvent with a specific `user_name`.
```python
async def dangerous_task(ctx: Context) -> str:
    """A dangerous task that requires human confirmation."""

    # emit an event to the external stream to be captured
    ctx.write_event_to_stream(
        InputRequiredEvent(
            prefix="Are you sure you want to proceed? ",
            user_name="Laurie",
        )
    )

    # wait until we see a HumanResponseEvent
    response = await ctx.wait_for_event(
        HumanResponseEvent, requirements={"user_name": "Laurie"}
    )

    # act on the input from the event
    if response.response.strip().lower() == "yes":
        return "Dangerous task completed successfully."
    else:
        return "Dangerous task aborted."
```

```python
workflow = FunctionAgent(
    tools=[dangerous_task],
    llm=llm,
    system_prompt="You are a helpful assistant that can perform dangerous tasks.",
)
```

Now we can run the workflow, handling the `InputRequiredEvent` just like any other streaming event, and responding with a `HumanResponseEvent` passed in using the `send_event` method:

```python
async def main():
    handler = agent.run(user_msg="I want to proceed with the dangerous task.")

    async for event in handler.stream_events():
        # capture InputRequiredEvent
        if isinstance(event, InputRequiredEvent):
            # capture keyboard input
            response = input(event.prefix)
            # send our response back
            handler.ctx.send_event(
                HumanResponseEvent(
                    response=response,
                    user_name=event.user_name,
                )
            )

    response = await handler
    print(str(response))
```

#### Multi Agent Patterns
The three most common patterns, when to choose each one, and provides a minimal code sketch for every approach.
- **AgentWorkflow (built-in)** – declare a set of agents and let `AgentWorkflow` manage the hand-offs.
- **Orchestrator pattern (built-in)** – an “orchestrator” agent chooses which sub-agent to call next; those sub-agents are exposed to it as **tools**.
- **Custom planner (DIY)** – you write the LLM prompt (often XML / JSON) that plans the sequence yourself and imperatively invoke the agents in code.

```python
async def search_web(query:str) -> str:
    """Useful for using the web to answer questions"""
    client = AsyncTavilyClient(api_key = os.getenv("TAVILY_API_KEY"))
    response = await client.search(query)
    return str(response)

async def record_notes(ctx:Context, notes:str,notes_title: str) -> str:
    """Useful for recording notes on a given topic.Your input should be notes with a title to save the notes under."""

    async with ctx.store.edit_state() as ctx_state:
        if "research_notes" not in ctx_state["state"]:
            ctx_state["state"]["research_notes"] = {}

        ctx_state["state"]["research_notes"][notes_title] = notes
    return "Notes recorded."

async def write_report(ctx:Context,report_content: str) -> str:
    """Useful for writing a report on a given topic. Your input should be a markdown formatted report."""

    async with ctx.store.edit_state() as ctx_state:
        ctx_state["state"]["report_content"] = report_content
    return "Report written."

async def review_report(ctx: Context, review: str) -> str:
    """Useful for reviewing a report and providing feedback. Your input should be a review of the report."""
    async with ctx.store.edit_state() as ctx_state:
        ctx_state["state"]["review"] = review
    return "Report reviewed."
```

```python
research_agent = FunctionAgent(
    name = "ResearchAgent",
    description="Useful for searching the web for information on a given topic and recording notes on the topic.",
    system_prompt=(
        "You are the ResearchAgent that can search the web for information on a given topic and record notes on the topic. "
        "Once notes are recorded and you are satisfied, you should hand off control to the WriteAgent to write a report on the topic. "
        "You should have at least some notes on a topic before handing off control to the WriteAgent."
    ),
    llm=llm,
    tools=[search_web, record_notes],
    can_handoff_to=["WriteAgent"],
)

write_agent = FunctionAgent(
    name="WriteAgent",
    description="Useful for writing a report on a given topic.",
    system_prompt=(
        "You are the WriteAgent that can write a report on a given topic. "
        "Your report should be in a markdown format. The content should be grounded in the research notes. "
        "Once the report is written, you should get feedback at least once from the ReviewAgent."
    ),
    llm=llm,
    tools=[write_report],
    can_handoff_to=["ReviewAgent", "ResearchAgent"],
)

review_agent = FunctionAgent(
    name="ReviewAgent",
    description="Useful for reviewing a report and providing feedback.",
    system_prompt=(
        "You are the ReviewAgent that can review the write report and provide feedback. "
        "Your review should either approve the current report or request changes for the WriteAgent to implement. "
        "If you have feedback that requires changes, you should hand off control to the WriteAgent to implement the changes after submitting the review."
    ),
    llm=llm,
    tools=[review_report],
    can_handoff_to=["WriteAgent"],
)
```

```python
agent_workflow = AgentWorkflow(
    agents=[research_agent, write_agent, review_agent],
    root_agent=research_agent.name,
    initial_state={
        "research_notes": {},
        "report_content": "Not written yet.",
        "review": "Review required.",
    },
)
```

```python
async def main():
    handler = agent_workflow.run(
        user_msg=(
            "Write me a report on the history of the internet. "
            "Briefly describe the history of the internet, including the development of the internet, the development of the web, "
            "and the development of the internet in the 21st century."
        )
    )

    current_agent = None
    current_tool_calls = ""

    async for event in handler.stream_events():
        if (
            hasattr(event,"current_agent_name")
            and event.current_agent_name != current_agent
        ):
            current_agent = event.current_agent_name
            print(f"\n\n=== {current_agent} ===")

        if isinstance(event, AgentStream):
            if event.delta:
                print(event.delta, end="", flush=True)
        elif isinstance(event, AgentInput):
            print("📥 Input:", event.input)
        elif isinstance(event, AgentOutput):
            if event.response.content:
                print("📤 Output:", event.response.content)
            if event.tool_calls:
                print(
                    "🛠️  Planning to use tools:",
                    [call.tool_name for call in event.tool_calls],
                )

        elif isinstance(event,ToolCallResult):
            print(f"🔧 Tool Result ({event.tool_name}):")
            print(f"  Arguments: {event.tool_kwargs}")
            print(f"  Output: {event.tool_output}")
        elif isinstance(event, ToolCall):
            print(f"🔨 Calling Tool: {event.tool_name}")
            print(f"  With arguments: {event.tool_kwargs}")

        state = await handler.ctx.store.get("state")
        print(state["report_content"])

if __name__ == "__main__":
    asyncio.run(main())
```

#### Use Structured Output
```python
class MathResult(BaseModel):
    operation:str = Field(description = "the performed operation")
    result : int = Field(description = "the result of the operation")

def multiply(a:int,b:int):
    """Multiplies two numbers"""
    return a * b

agent = FunctionAgent(
    llm=llm,
    tools = [multiply],
    output_cls = MathResult,
    name = "calculator",
    system_prompt = "You are a calculator agent who can multiply two numbers using the `multiply` tool."
)

async def main():
    response = await agent.run("What is 12 * 13?")
    print(response.structured_response)
    print(response.get_pydantic_model(MathResult))

# Execute the main function with asyncio
if __name__ == "__main__":
    asyncio.run(main())
```

```text
{'operation': '12 * 13', 'result': 156}
operation='12 * 13' result=156
```

For Multiple agents:
```python
class Weather(BaseModel):
    location:str = Field(description = "The location")
    weather:str = Field(description = "The weather")

def get_weather(location:str):
    """Get the weather for a location."""
    return f"The weather in {location} is sunny."

## define single agents
agent = FunctionAgent(
    llm=llm,
    tools=[get_weather],
    system_prompt="You are a weather agent that can get the weather for a given location",
    name="WeatherAgent",
    description="The weather forecaster agent.",
)
main_agent = FunctionAgent(
    name="MainAgent",
    tools=[],
    description="The main agent",
    system_prompt="You are the main agent, your task is to dispatch tasks to secondary agents, specifically to WeatherAgent",
    can_handoff_to=["WeatherAgent"],
    llm=llm,
)

## define multi-agent workflow
agent = AgentWorkflow(
    agents=[main_agent, agent],
    root_agent=main_agent.name,
    output_cls=Weather,
)

async def main():
    response = await agent.run("What is the weather in Tokyo?")
    print(response.structured_response)
    print(response.get_pydantic_model(Weather))

# Execute the main function with asyncio
if __name__ == "__main__":
    asyncio.run(main())
```