```python 
from crewai import Agent
from crewai_tools import SerperDevTool

# Create an agent with all available parameters
agent = Agent(
    role="Senior Data Scientist",
    goal="Analyze and interpret complex datasets to provide actionable insights",
    backstory="With over 10 years of experience in data science and machine learning, "
              "you excel at finding patterns in complex datasets.",
    llm="gpt-4",  # Default: OPENAI_MODEL_NAME or "gpt-4"
    function_calling_llm=None,  # Optional: Separate LLM for tool calling
    verbose=False,  # Default: False
    allow_delegation=False,  # Default: False
    max_iter=20,  # Default: 20 iterations
    max_rpm=None,  # Optional: Rate limit for API calls
    max_execution_time=None,  # Optional: Maximum execution time in seconds
    max_retry_limit=2,  # Default: 2 retries on error
    respect_context_window=True,  # Default: True
    use_system_prompt=True,  # Default: True
    multimodal=False,  # Default: False
    inject_date=False,  # Default: False
    date_format="%Y-%m-%d",  # Default: ISO format
    reasoning=False,  # Default: False
    max_reasoning_attempts=None,  # Default: None
    tools=[SerperDevTool()],  # Optional: List of tools
    knowledge_sources=None,  # Optional: List of knowledge sources
    embedder=None,  # Optional: Custom embedder configuration
    system_template=None,  # Optional: Custom system prompt template
    prompt_template=None,  # Optional: Custom prompt template
    response_template=None,  # Optional: Custom response template
    step_callback=None,  # Optional: Callback function for monitoring
)
```

#### Adding Tools
```python
from crewai import Agent
from crewai_tools import SerperDevTool, WikipediaTools

# Create tools
search_tool = SerperDevTool()
wiki_tool = WikipediaTools()

# Add tools to agent
researcher = Agent(
    role="AI Technology Researcher",
    goal="Research the latest AI developments",
    tools=[search_tool, wiki_tool],
    verbose=True
)
```

### How Context Window Management Works

When an agent’s conversation history grows too large for the LLM’s context window, CrewAI automatically detects this situation and can either:

1. **Automatically summarize content** (when `respect_context_window=True`)
2. **Stop execution with an error** (when `respect_context_window=False`)

#### Use `respect_context_window=True` (Default) when:

- **Processing large documents** that might exceed context limits
- **Long-running conversations** where some summarization is acceptable
- **Research tasks** where general context is more important than exact details
- **Prototyping and development** where you want robust execution

#### Use `respect_context_window=False` when:

- **Precision is critical** and information loss is unacceptable
- **Legal or medical tasks** requiring complete context
- **Code review** where missing details could introduce bugs
- **Financial analysis** where accuracy is paramount

#### 1. Use RAG Tools
```python
from crewai_tools import RagTool

# Create RAG tool for large document processing
rag_tool = RagTool()

rag_agent = Agent(
    role="Research Assistant",
    goal="Query large knowledge bases efficiently",
    backstory="Expert at using RAG tools for information retrieval",
    tools=[rag_tool],  # Use RAG instead of large context windows
    respect_context_window=True,
    verbose=True
)
```

#### 2. Use Knowledge Sources
```python
# Use knowledge sources instead of large prompts
knowledge_agent = Agent(
    role="Knowledge Expert",
    goal="Answer questions using curated knowledge",
    backstory="Expert at leveraging structured knowledge sources",
    knowledge_sources=[your_knowledge_sources],  # Pre-processed knowledge
    respect_context_window=True,
    verbose=True
)
```

### Context Window Best Practices

1. **Monitor Context Usage**: Enable `verbose=True` to see context management in action
2. **Design for Efficiency**: Structure tasks to minimize context accumulation
3. **Use Appropriate Models**: Choose LLMs with context windows suitable for your tasks
4. **Test Both Settings**: Try both `True` and `False` to see which works better for your use case
5. **Combine with RAG**: Use RAG tools for very large datasets instead of relying solely on context windows
#### Memory and Context

- `memory`: Enable to maintain conversation history
- `respect_context_window`: Prevents token limit issues
- `knowledge_sources`: Add domain-specific knowledge bases

#### Execution Control

- `max_iter`: Maximum attempts before giving best answer
- `max_execution_time`: Timeout in seconds
- `max_rpm`: Rate limiting for API calls
- `max_retry_limit`: Retries on error

#### Advanced Features

- `multimodal`: Enable multimodal capabilities for processing text and visual content
- `reasoning`: Enable agent to reflect and create plans before executing tasks
- `inject_date`: Automatically inject current date into task descriptions

#### Templates

- `system_template`: Defines agent’s core behavior
- `prompt_template`: Structures input format
- `response_template`: Formats agent responses

## Direct Agent Interaction with `kickoff()`

Agents can be used directly without going through a task or crew workflow using the `kickoff()` method. This provides a simpler way to interact with an agent when you don’t need the full crew orchestration capabilities.

### How `kickoff()` Works

The `kickoff()` method allows you to send messages directly to an agent and get a response, similar to how you would interact with an LLM but with all the agent’s capabilities (tools, reasoning, etc.).

```python
from crewai import Agent
from crewai_tools import SerperDevTool

# Create an agent
researcher = Agent(
    role="AI Technology Researcher",
    goal="Research the latest AI developments",
    tools=[SerperDevTool()],
    verbose=True
)

# Use kickoff() to interact directly with the agent
result = researcher.kickoff("What are the latest developments in language models?")

# Access the raw response
print(result.raw)
```

### Parameters and Return Values

| Parameter         | Type                               | Description                                                               |
| ----------------- | ---------------------------------- | ------------------------------------------------------------------------- |
| `messages`        | `Union[str, List[Dict[str, str]]]` | Either a string query or a list of message dictionaries with role/content |
| `response_format` | `Optional[Type[Any]]`              | Optional Pydantic model for structured output                             |

The method returns a `LiteAgentOutput` object with the following properties:

- `raw`: String containing the raw output text
- `pydantic`: Parsed Pydantic model (if a `response_format` was provided)
- `agent_role`: Role of the agent that produced the output
- `usage_metrics`: Token usage metrics for the execution

### Structured Output
You can get structured output by providing a Pydantic model as the `response_format`:

```python
from pydantic import BaseModel
from typing import List

class ResearchFindings(BaseModel):
    main_points: List[str]
    key_technologies: List[str]
    future_predictions: str

# Get structured output
result = researcher.kickoff(
    "Summarize the latest developments in AI for 2025",
    response_format = ResearchFindings
)

# Access structured data
print(result.pydantic.main_points)
print(result.pydantic.future_predictions)
```

### Multiple Messages
You can also provide a conversation history as a list of message dictionaries:

```python
messages = [
    {"role": "user", "content": "I need information about large language models"},
    {"role": "assistant", "content": "I'd be happy to help with that! What specifically would you like to know?"},
    {"role": "user", "content": "What are the latest developments in 2025?"}
]

result = researcher.kickoff(messages)
```

### Async Support
An asynchronous version is available via `kickoff_async()` with the same parameters:

```python
import asyncio

async def main():
    result = await researcher.kickoff_async("What are the latest developments in AI?")
    print(result.raw)

asyncio.run(main())
```

##   
Important Considerations and Best Practices

### Security and Code Execution

`allow_code_execution` and `code_execution_mode` are deprecated and `CodeInterpreterTool` has been removed. Use a dedicated sandbox service such as [E2B](https://e2b.dev/) or [Modal](https://modal.com/) for secure code execution.

### Performance Optimization

- Use `respect_context_window: true` to prevent token limit issues
- Set appropriate `max_rpm` to avoid rate limiting
- Enable `cache: true` to improve performance for repetitive tasks
- Adjust `max_iter` and `max_retry_limit` based on task complexity

### Memory and Context Management

- Leverage `knowledge_sources` for domain-specific information
- Configure `embedder` when using custom embedding models
- Use custom templates (`system_template`, `prompt_template`, `response_template`) for fine-grained control over agent behavior

### Advanced Features

- Enable `reasoning: true` for agents that need to plan and reflect before executing complex tasks
- Set appropriate `max_reasoning_attempts` to control planning iterations (None for unlimited attempts)
- Use `inject_date: true` to provide agents with current date awareness for time-sensitive tasks
- Customize the date format with `date_format` using standard Python datetime format codes
- Enable `multimodal: true` for agents that need to process both text and visual content

### Agent Collaboration

- Enable `allow_delegation: true` when agents need to work together
- Use `step_callback` to monitor and log agent interactions
- Consider using different LLMs for different purposes:
    - Main `llm` for complex reasoning
    - `function_calling_llm` for efficient tool usage

### Date Awareness and Reasoning

- Use `inject_date: true` to provide agents with current date awareness for time-sensitive tasks
- Customize the date format with `date_format` using standard Python datetime format codes
- Valid format codes include: %Y (year), %m (month), %d (day), %B (full month name), etc.
- Invalid date formats will be logged as warnings and will not modify the task description
- Enable `reasoning: true` for complex tasks that benefit from upfront planning and reflection

### Model Compatibility

- Set `use_system_prompt: false` for older models that don’t support system messages
- Ensure your chosen `llm` supports the features you need (like function calling)

## Troubleshooting Common Issues

1. **Rate Limiting**: If you’re hitting API rate limits:
    - Implement appropriate `max_rpm`
    - Use caching for repetitive operations
    - Consider batching requests
2. **Context Window Errors**: If you’re exceeding context limits:
    - Enable `respect_context_window`
    - Use more efficient prompts
    - Clear agent memory periodically
3. **Code Execution Issues**: If code execution fails:
    - Verify Docker is installed for safe mode
    - Check execution permissions
    - Review code sandbox settings
4. **Memory Issues**: If agent responses seem inconsistent:
    - Check knowledge source configuration
    - Review conversation history management

Remember that agents are most effective when configured according to their specific use case. Take time to understand your requirements and adjust these parameters accordingly.