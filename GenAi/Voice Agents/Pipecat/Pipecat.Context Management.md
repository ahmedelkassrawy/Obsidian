What is context in pipecat
- In Pipecat, **context** refers to the conversation history that the LLM uses to generate responses. 
- The context consists of a list of alternating user/assistant messages that represents the collective history of the entire conversation.

```python
# Example context structure
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"},
    {"role": "assistant", "content": "Hi there! How can I help you?"},
    # Context aggregators automatically add new messages here
]
```

>[!tip]
>Since Pipecat is a real-time voice AI framework, context management happens automatically as the conversation flows, but you can also control it manually when needed.

## How Context Updates During Conversations
Context updates happen automatically as frames flow through your pipeline:
User Messages:
1. User speaks → `InputAudioRawFrame` → STT Service → `TranscriptionFrame`
2. `context_aggregator.user()` receives `TranscriptionFrame` and adds user message to context

**Assistant Messages:**
1. LLM generates response → `LLMTextFrame` → TTS Service → `TTSTextFrame`
2. `context_aggregator.assistant()` receives `TTSTextFrame` and adds assistant message to context

**Frame types that update context:**
- **`TranscriptionFrame`**: Contains user speech converted to text by STT service
- **`LLMTextFrame`**: Contains LLM-generated responses
- **`TTSTextFrame`**: Contains bot responses converted to text by TTS service (represents what was actually spoken)

# Setting up Context Management
Pipecat includes a context aggregator that creates and manages context for both user and assistant messages:

1. Create Context and Context Aggregator
```python
# Create LLM service
llm = OpenAILLMService(api_key=os.getenv("OPENAI_API_KEY"))

# Create context with initial messages
messages = [
    {"role": "system", 
    "content": "You are a helpful voice assistant."}
]

# Create context (messages only)
context = LLMContext(messages)

# Create context aggregator instance
user_aggregator, assistant_aggregator = LLMContextAggregatorPair(context)
```

**About LLMContext:**
`LLMContext` is Pipecat’s universal context container that stores conversation messages, tool definitions, and tool choice settings. 
It uses an OpenAI-compatible format that works across all LLM services through automatic adapter translation.

Key properties:
- **`messages`**: List of conversation messages (system, user, assistant, tool)
- **`tools`**: Optional `ToolsSchema` defining available functions
- **`tool_choice`**: Optional strategy for tool selection

2. Context with Function calling
Context can also include tools (function definitions) that the LLM can call during conversations:
```python
from pipecat.adapters.schemas.function_schema import FunctionSchema
from pipecat.adapters.schemas.tools_schema import ToolsSchema

# Define available functions
weather_function = FunctionSchema(
    name="get_current_weather",
    description="Get the current weather",
    properties={
        "location": {
            "type": "string",
            "description": "The city and state, e.g. San Francisco, CA",
        },
        "format": {
            "type": "string",
            "enum": ["celsius", "fahrenheit"],
            "description": "The temperature unit to use.",
        },
    },
    required=["location", "format"],
)

# Create tools schema
tools = ToolsSchema(standard_tools=[weather_function])

# Create context with both messages and tools
context = LLMContext(messages, tools)
user_aggregator, assistant_aggregator = LLMContextAggregatorPair(context)
```

Function call results are also automatically stored in the context, maintaining a complete conversation history including tool interactions

3. Add Context Aggregators to Your pipeline
```python
pipeline = Pipeline([
    transport.input(),
    stt,
    context_aggregator.user(),      # User context aggregator
    llm,
    tts,
    transport.output(),
    context_aggregator.assistant(), # Assistant context aggregator
])
```
#### Context Aggregator Placement
The placement of context aggregator instances in your pipeline is **crucial** for proper operation
#### Manual Context Control
You can programmatically add new messages to the context by pushing or queueing specific frames:
### Adding Messages
- **`LLMMessagesAppendFrame`**: Appends a new message to the existing context
- **`LLMMessagesUpdateFrame`**: Completely replaces the existing context with new messages
```python
# Add a new system message to context
new_message = {
	"role": "system", 
	"content": "You are now in expert mode."
}
await task.queue_frames([
    LLMMessagesAppendFrame([new_message], run_llm=True), # Optionally trigger bot response, too
])
```

#### Retrieving Current Context
The context aggregator provides a `context` property for getting the current context:
```python
context = context_aggregator.user().context
```

#### Context Summarization
Enable it by setting `enable_context_summarization=True` when creating your context aggregators:
```python
user_aggregator, assistant_aggregator = LLMContextAggregatorPair(
    context,
    assistant_params=LLMAssistantAggregatorParams(
        enable_context_summarization=True,
    ),
)
```

#### Triggering the BOT responses
You may want to manually trigger the bot to speak in two scenarios:
1. **Starting a pipeline** where the bot should speak first
2. **After editing the context** using `LLMMessagesAppendFrame` or `LLMMessagesUpdateFrame`
```python
# Example: Bot speaks first when pipeline starts
@transport.event_handler("on_client_connected")
async def on_client_connected(transport, client):
    # Trigger a response
    await task.queue_frames([LLMRunFrame()])
```

```python
# Example: Bot speaks after context is edited
new_message = {"role": "user", "content": "Tell me a fun fact."}
await task.queue_frames([
    LLMMessagesAppendFrame([new_message], run_llm=True), # Trigger bot response
])
```

#### Key takeaways
- **Context is conversation history** - automatically maintained as users and bots exchange messages
- **Frame types matter** - `TranscriptionFrame` for users, `TTSTextFrame` for assistants
- **Placement matters** - user aggregator after STT, assistant aggregator after transport output
- **Tools are included** - function definitions and results are stored in context
- **Manual control available** - use frames to append messages or trigger responses when needed
- **Word-level precision** - proper placement ensures context accuracy during interruptions
- **Automatic summarization** - enable context summarization to manage long conversations efficiently and reduce token costs