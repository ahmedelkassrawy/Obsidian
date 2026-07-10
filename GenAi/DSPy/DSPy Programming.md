## Calling the LM directly
```python
lm = dspy.LM('gemini/gemini-2.5-flash', api_key= os.getenv("GEMINI_API_KEY"))
dspy.configure(lm=lm)

lm("Say this is a test",)
lm(messages = [
    {
        "role":"user",
        "Content": "Say this is a test!"
    }
])
```

#### Using Modules
```python
lm = dspy.LM('gemini/gemini-2.5-flash', api_key= os.getenv("GEMINI_API_KEY"))
dspy.configure(lm=lm)

qa = dspy.ChainOfThought("question -> answer") #return an answer after given a question
response = qa(question = "How many floors are in the castle David Gregory inherited?")
print(response.answer)
```

##### Caching
```python
gpt_4o_mini = dspy.LM('openai/gpt-4o-mini', temperature=0.9, max_tokens=3000, stop=None, cache=False)
```

If we want tot keep caching enabled but force a new request (to get diff outputs):
- pass a unique "rollout_id" 
- set a non-zero "temperature"
- DSPy hashes both inputs and the "rollout_id" when looking up a cache entry
- so diff values forces a new LM request while still caching future calls with the same inputs and "rollout_id"
- The ID also recorded in "lm.history" which makes it easy to track or compare diff rollouts during experiments
- Changing only the `rollout_id` while keeping `temperature=0` will not affect the LM's output.

```python
lm("Say this is a test!", rollout_id=1, temperature=1.0)
```

```python
predict = dspy.Predict("question -> answer")
predict(question="What is 1 + 52?", config={"rollout_id": 5, "temperature": 1.0})
```
#####  Inspecting output and usage metadata.
```python
len(lm.history)  # e.g., 3 calls to the LM
lm.history[-1].keys()  # access the last call to the LM, with all metadata
```

**When should you use the Responses API?**
- When you want to leverage enhanced reasoning, multi-turn, or richer output capabilities provided by certain models.

```python
import dspy

# Configure DSPy to use the Responses API for your language model
dspy.configure(
    lm=dspy.LM(
        "openai/gpt-5-mini",
        model_type="responses",
        temperature=1.0,
        max_tokens=16000,
    ),
)
```
---
#### Signatures
When we assign tasks to LMs in DSPy, we specify the behavior we need as a Signature.
**A signature is a declarative specification of input/output behavior of a DSPy module.**

Signature allows you to tell the LM what it needs to do, rather than specify how we should ask the LM to do it.

While typical function signatures just _describe_ things, DSPy Signatures _declare and initialize the behavior_ of modules.

Moreover, the field names matter in DSPy Signatures. You express semantic roles in plain English: a `question` is different from an `answer`, a `sql_query` is different from `python_code`.

Writing signatures is far more modular, adaptive, and reproducible than hacking at prompts or finetunes. The DSPy compiler will figure out how to build a highly-optimized prompt for your LM (or finetune your small LM) for your signature, on your data, and within your pipeline.

In many cases, we found that compiling leads to better prompts than humans write. Not because DSPy optimizers are more creative than humans, but simply because they can try more things and tune the metrics directly.

Signatures can be defined as a short string, with argument names and optional types that define semantic roles for inputs/outputs.

1. Question Answering: `"question -> answer"`, which is equivalent to `"question: str -> answer: str"` as the default type is always `str`
2. Sentiment Classification: `"sentence -> sentiment: bool"`, e.g. `True` if positive
3. Summarization: `"document -> summary"`

Your signatures can also have multiple input/output fields with types:
1. Retrieval-Augmented Question Answering: `"context: list[str], question: str -> answer: str"`
2. Multiple-Choice Question Answering with Reasoning: `"question, choices: list[str] -> reasoning: str, selection: int"`

Inline:
```python
toxicity = dspy.Predict(
    dspy.Signature(
        "comment -> toxic: bool",
        instructions = "Marks as 'toxic' if the comment includes insults, harassment or sarcastic derogatory remarks."
    )
)

comment = "you are beautiful"
toxicity(comment = comment).toxic
```

```python
sentence = "its a charming and often affecting journey."

classify = dspy.Predict(
    dspy.Signature("sentence -> sentiment: bool",
    instructions = "Marks as 'positive' if the comment is not includeing negative comments or ideas"
	)
)
classify(sentence = sentence).sentiment
```

Many DSPy modules (except `dspy.Predict`) return auxiliary information by expanding your signature under the hood.

For example, `dspy.ChainOfThought` also adds a `reasoning` field that includes the LM's reasoning before it generates the output `summary`.

```python
print("Reasoning:", response.reasoning)
```

Class-based:
For some advanced tasks, you need more verbose signatures. This is typically to:
1. Clarify something about the nature of the task as a `docstring`
2. Supply hints on the nature of an input field expressed as a `desc` arg for `dspy.InputField`
3. Supply constraints on output field expressed as a `desc` arg for `dspy.OutputField`

```python
from typing import Literal

class Emotion(dspy.Signature):
    """Classify emotion."""

    sentence: str = dspy.InputField()
    sentiment: Literal['sadness', 'joy', 'love', 'anger', 'fear', 'surprise'] = dspy.OutputField()

sentence = "i started feeling a little vulnerable when the giant spotlight started blinding me"  # from dair-ai/emotion

classify = dspy.Predict(Emotion)
classify(sentence=sentence)
```

```python
Prediction(
    sentiment='fear'
)
```

>[!tip]
>There's nothing wrong with specifying your requests to the LM more clearly. Class-based Signatures help you with that. However, don't prematurely tune the keywords of your signature by hand. 
>The DSPy optimizers will likely do a better job (and will transfer better across LMs). 

```python
class CheckCitationFaithfulness(dspy.Signature):
    """Verify that the text is based on the provided context."""

    context: str = dspy.InputField(desc="facts here are assumed to be true")
    text: str = dspy.InputField()
    faithfulness: bool = dspy.OutputField()
    evidence: dict[str, list[str]] = dspy.OutputField(desc="Supporting evidence for claims")

context = "The 21-year-old made seven appearances for the Hammers and netted his only goal for them in a Europa League qualification round match against Andorran side FC Lustrains last season. Lee had two loan spells in League One last term, with Blackpool and then Colchester United. He scored twice for the U's but was unable to save them from relegation. The length of Lee's contract with the promoted Tykes has not been revealed. Find all the latest football transfers on our dedicated page."
text = "Lee scored 3 goals for Colchester United."

faithfulness = dspy.ChainOfThought(CheckCitationFaithfulness)
faithfulness(context=context, text=text)
```

Custom Type:
```python
# Simple custom type
class QueryResult(pydantic.BaseModel):
    text: str
    score: float

signature = dspy.Signature("query: str -> result: QueryResult")

class MyContainer:
    class Query(pydantic.BaseModel):
        text: str
    class Score(pydantic.BaseModel):
        score: float

signature = dspy.Signature("query: MyContainer.Query -> score: MyContainer.Score")
```
---
#### Modules
A **DSPy module** is a building block for programs that use LMs.
- Each built-in module abstracts a **prompting technique** (like chain of thought or ReAct). Crucially, they are generalized to handle any signature.
    
- A DSPy module has **learnable parameters** (i.e., the little pieces comprising the prompt and the LM weights) and can be invoked (called) to process inputs and return outputs.
    
- Multiple modules can be composed into bigger modules (programs). DSPy modules are inspired directly by NN modules in PyTorch, but applied to LM programs.

#### How do I use a built-in module, like `dspy.Predict` or `dspy.ChainOfThought`?
Internally, all other DSPy modules are built using `dspy.Predict`
To use a module, we first **declare** it by giving it a signature. Then we **call** the module with the input arguments, and extract the output fields!

```python
sentence = "it's a charming and often affecting journey."

classify = dspy.Predict("sentence -> sentiment: bool")
response = classify(sentence = sentence)
print(response.sentiment)
```

When we declare a module, we can pass configuration keys to it.
as n =5 , for request five completions or `temperature` or `max_len`

>[!note] 
>Let's use `dspy.ChainOfThought`. In many cases, simply swapping `dspy.ChainOfThought` in place of `dspy.Predict` improves quality.

```python
question = "What's something great about the ColBERT retrieval model?"

classify = dspy.ChainOfThought("question -> answer",n = 5)
response = classify(question = question)
print(response.completions.answer)
```

```python
['One great thing about the ColBERT retrieval model is its superior efficiency and effectiveness compared to other models.',
 'Its ability to efficiently retrieve relevant information from large document collections.',
 'One great thing about the ColBERT retrieval model is its superior performance compared to other models and its efficient use of pre-trained language models.',
 'One great thing about the ColBERT retrieval model is its superior efficiency and accuracy compared to other models.',
 'One great thing about the ColBERT retrieval model is its ability to incorporate user feedback and support complex queries.']
```

Let's discuss the output object here. The `dspy.ChainOfThought` module will generally inject a `reasoning` before the output field(s) of your signature.
Let's inspect the (first) reasoning and answer!

```python
print(f"Reasoning: {response.reasoning}") #for the first answer
print(f"Answer: {response.answer}") #for the first answer
```

```python
response.completions[3].reasoning == response.completions.reasoning[3]
response.completions[3].reasoning #the same
response.completions.reasoning[3] #the same
```

#### DSPy Modules
1. **`dspy.Predict`**: Basic predictor. Does not modify the signature. Handles the key forms of learning (i.e., storing the instructions and demonstrations and updates to the LM).
    
2. **`dspy.ChainOfThought`**: Teaches the LM to think step-by-step before committing to the signature's response.
    
3. **`dspy.ProgramOfThought`**: Teaches the LM to output code, whose execution results will dictate the response.
    
4. **`dspy.ReAct`**: An agent that can use tools to implement the given signature.
    
5. **`dspy.MultiChainComparison`**: Can compare multiple outputs from `ChainOfThought` to produce a final prediction.

We also have some function-style modules:
6. **`dspy.majority`**: Can do basic voting to return the most popular response from a set of predictions.

#### Tracking Usage
```python
dspy.configure(track_usage=True)
```

you can access usage statistics using `dspy.Prediction` object:
```python
usage = prediction_instance.get_lm_usage()
```

```python
import dspy

# Configure DSPy with tracking enabled
dspy.configure(
    lm=dspy.LM("openai/gpt-4o-mini", cache=False),
    track_usage=True
)

# Define a simple program that makes multiple LM calls
class MyProgram(dspy.Module):
    def __init__(self):
        self.predict1 = dspy.ChainOfThought("question -> answer")
        self.predict2 = dspy.ChainOfThought("question, answer -> score")

    def __call__(self, question: str) -> str:
        answer = self.predict1(question=question)
        score = self.predict2(question=question, answer=answer)
        return score

# Run the program and check usage
program = MyProgram()
output = program(question="What is the capital of France?")
print(output.get_lm_usage())
```

```python
# First call - will show usage statistics
output = program(question="What is the capital of Zambia?")
print(output.get_lm_usage())  # Shows token usage

# Second call - same question, will use cache
output = program(question="What is the capital of Zambia?")
print(output.get_lm_usage())  # Shows empty dict: {}
```
----
#### Adapters
- Adapters are the bridge between `dspy.Predict` and the actual Language Model (LM).
- When ou call a DSPy module, the adapter takes your signature, user inputs, and other attributes like `demos` (few-shot examples) and converts them into multi-turn messages that get sent to the LM. 

The adapter system is responsible for:

- Translating DSPy signatures into system messages that define the task and request/response structure.
- Formatting input data according to the request structure outlined in DSPy signatures.
- Parsing LM responses back into structured DSPy outputs, such as `dspy.Prediction` instances.
- Managing conversation history and function calls.
- Converting pre-built DSPy types into LM prompt messages, e.g., `dspy.Tool`, `dspy.Image`, etc.

>[!note] 
>You can use `dspy.configure(adapter=...)` to choose the adapter for the entire Python process, or `with dspy.context(adapter=...):` to only affect a certain namespace.

If no adapter is specified in the DSPy workflow, each `dspy.Predict.__call__` defaults to using the `dspy.ChatAdapter`. Thus, the two code snippets below are equivalent:
```python
predict = dspy.Predict("question -> answer")
result = predict(question="What is the capital of France?")

#THE SAME AS 

dspy.configure(
    lm=dspy.LM("openai/gpt-4o-mini"),
    adapter=dspy.ChatAdapter(),  # This is the default value
)

predict = dspy.Predict("question -> answer")
result = predict(question="What is the capital of France?")
```

## Where Adapters Fit in the System

The flow works as follows:
1. The user calls their DSPy agent, typically a `dspy.Module` with inputs.
2. The inner `dspy.Predict` is invoked to obtain the LM response.
3. `dspy.Predict` calls **Adapter.format()**, which converts its signature, inputs, and demos into multi-turn messages sent to the `dspy.LM`. `dspy.LM` is a thin wrapper around `litellm`, which communicates with the LM endpoint.
4. The LM receives the messages and generates a response.
5. **Adapter.parse()** converts the LM response into structured DSPy outputs, as specified in the signature.
6. The caller of `dspy.Predict` receives the parsed outputs.

See the messages sent to the LLM
```python
# Simplified flow example
signature = dspy.Signature("question -> answer")
inputs = {"question": "What is 2+2?"}
demos = [{"question": "What is 1+1?", "answer": "2"}]

adapter = dspy.ChatAdapter()
print(adapter.format(signature, demos, inputs))
```

See the system message sent to the llm
```python
import dspy

signature = dspy.Signature("question -> answer")
system_message = dspy.ChatAdapter().format_system_message(signature)
print(system_message)
```

#### Type of Adapters
**ChatAdapter** is the default adapter and works with all language models. It uses a field-based format with special markers.
it includes the JSON schema of the type.

We use `dspy.inspect_history()` to display the formatted messages by `dspy.ChatAdapter` clearly.

```python
from pydantic import BaseModel

class ScienceNews(BaseModel):
  text:str
  scientists_involved : list[str]

class NewsQA(dspy.Signature):
  """Get news about the given science field"""
  science_field: str = dspy.InputField()
  year:int = dspy.InputField()
  num_of_outputs:int = dspy.InputField()
  news: list[ScienceNews] = dspy.OutputField(desc = "science news")

predict = dspy.Predict(NewsQA)
predict(science_field = "computer Thoery",year = 2022,num_of_outputs = 1)
dspy.inspect_history()
```

```
[2025-08-15T22:24:29.378666]

System message:

Your input fields are:
1. `science_field` (str):
2. `year` (int):
3. `num_of_outputs` (int):
Your output fields are:
4. `news` (list[ScienceNews]): science news
All interactions will be structured in the following way, with the appropriate values filled in.

[[ ## science_field ## ]]
{science_field}

[[ ## year ## ]]
{year}

[[ ## num_of_outputs ## ]]
{num_of_outputs}

[[ ## news ## ]]
{news}        # note: the value you produce must adhere to the JSON schema: {"type": "array", "$defs": {"ScienceNews": {"type": "object", "properties": {"scientists_involved": {"type": "array", "items": {"type": "string"}, "title": "Scientists Involved"}, "text": {"type": "string", "title": "Text"}}, "required": ["text", "scientists_involved"], "title": "ScienceNews"}}, "items": {"$ref": "#/$defs/ScienceNews"}}

[[ ## completed ## ]]
In adhering to this structure, your objective is:
        Get news about the given science field


User message:

[[ ## science_field ## ]]
Computer Theory

[[ ## year ## ]]
2022

[[ ## num_of_outputs ## ]]
1

Respond with the corresponding output fields, starting with the field `[[ ## news ## ]]` (must be formatted as a valid Python list[ScienceNews]), and then ending with the marker for `[[ ## completed ## ]]`.


Response:

[[ ## news ## ]]
[
    {
        "scientists_involved": ["John Doe", "Jane Smith"],
        "text": "In 2022, researchers made significant advancements in quantum computing algorithms, demonstrating their potential to solve complex problems faster than classical computers. This breakthrough could revolutionize fields such as cryptography and optimization."
    }
]

[[ ## completed ## ]]
```

>[!tip] Practice: locate Signature information in the printed LM history
Try adjusting the signature, and observe how the changes are reflected in the printed LM message.

Because the output field is structured as defined by ChatAdapter, it can be automatically parsed into structured data.

#### When to Use ChatAdapter
`ChatAdapter` offers the following advantages:

- **Universal compatibility**: Works with all language models, though smaller models may generate responses that do not match the required format.
- **Fallback protection**: If `ChatAdapter` fails, it automatically retries with `JSONAdapter`.

In general, `ChatAdapter` is a reliable choice if you don't have specific requirements.

#### When Not to Use ChatAdapter
Avoid using `ChatAdapter` if you are:

- **Latency sensitive**: `ChatAdapter` includes more boilerplate output tokens compared to other adapters, so if you're building a system sensitive to latency, consider using a different adapter.

### JSONAdapter

**JSONAdapter** prompts the LM to return JSON data containing all output fields as specified in the signature. It is effective for models that support structured output via the `response_format` parameter, leveraging native JSON generation capabilities for more reliable parsing.

#### Format Structure
The input part of the prompt formatted by `JSONAdapter` is similar to `ChatAdapter`, but the output part differs, as shown below:
```python
dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"), adapter=dspy.JSONAdapter())
...
dspy.inspect_history()
```

```
Respond with a JSON object in the following order of fields: `news` (must be formatted as a valid Python list[ScienceNews]).


Response:

{
  "news": [
    {
      "text": "In 2022, researchers made significant advancements in quantum computing algorithms, demonstrating that quantum systems can outperform classical computers in specific tasks. This breakthrough could revolutionize fields such as cryptography and complex system simulations.",
      "scientists_involved": [
        "Dr. Alice Smith",
        "Dr. Bob Johnson",
        "Dr. Carol Lee"
      ]
    }
  ]
}
```

#### When to Use JSONAdapter
`JSONAdapter` is good at:

- **Structured output support**: When the model supports the `response_format` parameter.
- **Low latency**: Minimal boilerplate in the LM response results in faster responses.

#### When Not to Use JSONAdapter
Avoid using `JSONAdapter` if you are:

- Using a model that does not natively support structured output, such as a small open-source model hosted on Ollama.****
---
#### Tools
There are two main approaches to using tools in DSPy:

1. **`dspy.ReAct`** - A fully managed tool agent that handles reasoning and tool calls automatically
2. **Manual tool handling** - Direct control over tool calls using `dspy.Tool`, `dspy.ToolCalls`, and custom signatures
## Approach 1: Using `dspy.ReAct` (Fully Managed)
The `dspy.ReAct` module implements the Reasoning and Acting (ReAct) pattern, where the language model iteratively reasons about the current situation and decides which tools to call.
```python
import dspy

# Define your tools as functions
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    # In a real implementation, this would call a weather API
    return f"The weather in {city} is sunny and 75°F"

def search_web(query: str) -> str:
    """Search the web for information."""
    # In a real implementation, this would call a search API
    return f"Search results for '{query}': [relevant information...]"

# Create a ReAct agent
react_agent = dspy.ReAct(
    signature="question -> answer",
    tools=[get_weather, search_web],
    max_iters=5
)

# Use the agent
result = react_agent(question="What's the weather like in Tokyo?")
print(result.answer)
print("Tool calls made:", result.trajectory)
```

Params:
```python
react_agent = dspy.ReAct(
    signature="question -> answer",  # Input/output specification
    tools=[tool1, tool2, tool3],     # List of available tools
    max_iters=10                     # Maximum number of tool call iterations
)
```

#### Manual Tool Handling
```python
import dspy

class ToolSignature(dspy.Signature):
    """Signature for manual tool handling."""
    question: str = dspy.InputField()
    tools: list[dspy.Tool] = dspy.InputField()
    outputs: dspy.ToolCalls = dspy.OutputField()

def weather(city: str) -> str:
    """Get weather information for a city."""
    return f"The weather in {city} is sunny"

def calculator(expression: str) -> str:
    """Evaluate a mathematical expression."""
    try:
        result = eval(expression)  # Note: Use safely in production
        return f"The result is {result}"
    except:
        return "Invalid expression"

# Create tool instances
tools = {
    "weather": dspy.Tool(weather),
    "calculator": dspy.Tool(calculator)
}

# Create predictor
predictor = dspy.Predict(ToolSignature)

# Make a prediction
response = predictor(
    question="What's the weather in New York?",
    tools=list(tools.values())
)

# Execute the tool calls
for call in response.outputs.tool_calls:
    # Execute the tool call
    result = call.execute()
    # For versions earlier than 3.0.4b2, use: result = tools[call.name](**call.args)
    print(f"Tool: {call.name}")
    print(f"Args: {call.args}")
    print(f"Result: {result}")
```

The `dspy.Tool` class wraps regular Python functions to make them compatible with DSPy's tool system:
```python
# Create a tool
tool = dspy.Tool(my_function)

# Tool properties
print(tool.name)        # "my_function"
print(tool.desc)        # The function's docstring
print(tool.args)        # Parameter schema
print(str(tool))        # Full tool description
```

Understanding `dspy.ToolCalls`
The `dspy.ToolCalls` type represents the output from a model that can make tool calls. Each individual tool call can be executed using the `execute` method:

```python
for call in response.outputs.tool_calls:
  print(f"Tool Name: {call.name}")
  print(f"Arguments: {call.args}")

  result = call.execute() # Option1: automatically finds functions by name
  
  result = call.execute(functions = {
      "weather": weather,
      "calculator": calculator
  }) #Option 2: pass tools as a dict

  result = call.execute(functions = [dspy.Tool(weather), dspy.Tool(calculator)])
  #Option 3: Pass tool objects as a list

  print(f"Result: {result}")
```

#### Using Native Tool Calling
DSPy adapters support **native function calling**

>[!warning]
Native tool calling doesn't guarantee better quality
It's possible that native tool calling produces lower quality than custom tool calling.

### Adapter Behavior
Different DSPy adapters have different defaults for native function calling:

- **`ChatAdapter`** - Uses `use_native_function_calling=False` by default (relies on text parsing)
- **`JSONAdapter`** - Uses `use_native_function_calling=True` by default (uses native function calling)

```python
import dspy

# ChatAdapter with native function calling enabled
chat_adapter_native = dspy.ChatAdapter(use_native_function_calling=True)

# JSONAdapter with native function calling disabled
json_adapter_manual = dspy.JSONAdapter(use_native_function_calling=False)

# Configure DSPy to use the adapter
dspy.configure(lm=dspy.LM(model="openai/gpt-4o"), adapter=chat_adapter_native)
```
---
#### Async Tools
DSPy tools support both synchronous and asynchronous functions. When working with async tools, you have two options:
#### Using `acall` for Async Tools
The recommended approach is to use `acall` when working with async tools:

```python
import asyncio
import dspy

async def async_weather(city: str) -> str:
    """Get weather information asynchronously."""
    await asyncio.sleep(0.1)  # Simulate async API call
    return f"The weather in {city} is sunny"

tool = dspy.Tool(async_weather)

# Use acall for async tools
result = await tool.acall(city="New York")
print(result)
```

#### Running Async Tools in Sync Mode
If you need to call an async tool from synchronous code, you can enable automatic conversion using the `allow_tool_async_sync_conversion` setting:

```python
import asyncio
import dspy

async def async_weather(city: str) -> str:
    """Get weather information asynchronously."""
    await asyncio.sleep(0.1)
    return f"The weather in {city} is sunny"

tool = dspy.Tool(async_weather)

# Enable async-to-sync conversion
with dspy.context(allow_tool_async_sync_conversion=True):
    # Now you can use __call__ on async tools
    result = tool(city="New York")
    print(result)
```

#### Best Practices
##### 1. Tool Function Design
- **Clear docstrings**: Tools work better with descriptive documentation
- **Type hints**: Provide clear parameter and return types
- **Simple parameters**: Use basic types (str, int, bool, dict, list) or Pydantic models
##### 2. Choosing Between ReAct and Manual Handling
---
#### MCP
DSPy supports MCP, allowing you to use tools from any MCP server with DSPy agents.

```python
pip install -U "dspy[mcp]"
```

MCP enables you to:
- **Use standardized tools** - Connect to any MCP-compatible server.
- **Share tools across stacks** - Use the same tools across different frameworks.
- **Simplify integration** - Convert MCP tools to DSPy tools with one line.

DSPy does not handle MCP server connections directly. You can use client interfaces of the `mcp` library to establish the connection and pass `mcp.ClientSession` to `dspy.Tool.from_mcp_tool` in order to convert mcp tools into DSPy tools.

#### Using MCP with DSPy
1. HTTP Server (Remote)
2. Stdio Server (Local Process)

#### HTTP Server
```python
import asyncio
import dspy
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

async def main():
    # Connect to HTTP MCP server
    async with streamablehttp_client("http://localhost:8000/mcp") as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the session
            await session.initialize()

            # List and convert tools
            response = await session.list_tools()
            dspy_tools = [
                dspy.Tool.from_mcp_tool(session, tool)
                for tool in response.tools
            ]

            # Create and use ReAct agent
            class TaskSignature(dspy.Signature):
                task: str = dspy.InputField()
                result: str = dspy.OutputField()

            react_agent = dspy.ReAct(
                signature=TaskSignature,
                tools=dspy_tools,
                max_iters=5
            )

            result = await react_agent.acall(task="Check the weather in Tokyo")
            print(result.result)

asyncio.run(main())
```

#### Stdio Server
```python
import asyncio
import dspy
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    # Configure the stdio server
    server_params = StdioServerParameters(
        command="python",                    # Command to run
        args=["path/to/your/mcp_server.py"], # Server script path
        env=None,                            # Optional environment variables
    )

    # Connect to the server
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the session
            await session.initialize()

            # List available tools
            response = await session.list_tools()

            # Convert MCP tools to DSPy tools
            dspy_tools = [
                dspy.Tool.from_mcp_tool(session, tool)
                for tool in response.tools
            ]

            # Create a ReAct agent with the tools
            class QuestionAnswer(dspy.Signature):
                """Answer questions using available tools."""
                question: str = dspy.InputField()
                answer: str = dspy.OutputField()

            react_agent = dspy.ReAct(
                signature=QuestionAnswer,
                tools=dspy_tools,
                max_iters=5
            )

            # Use the agent
            result = await react_agent.acall(
                question="What is 25 + 17?"
            )
            print(result.answer)

# Run the async function
asyncio.run(main())
```

#### Tool Conversion
DSPy automatically handles the conversion from MCP tools to DSPy tools:
```python
# MCP tool from session
mcp_tool = response.tools[0]

# Convert to DSPy tool
dspy_tool = dspy.Tool.from_mcp_tool(session, mcp_tool)

# The DSPy tool preserves:
# - Tool name and description
# - Parameter schemas and types
# - Argument descriptions
# - Async execution support

# Use it like any DSPy tool
result = await dspy_tool.acall(param1="value", param2=123)
```
