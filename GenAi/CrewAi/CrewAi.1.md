```python
from crewai import Agent
from crewai_tools import SerperDevTool

research_agent = Agent(
    role = "Research Analyst",
    goal = "Find and summarize the information about specific topics",
    backstory = "You are an experienced researcher with attention to detail",
    tools = [SerperDevTool()],
    verbose = True
)
```

Parameter Details
​
Critical Parameters
role, goal, and backstory are required and shape the agent’s behavior
llm determines the language model used (default: OpenAI’s GPT-4)
​
Memory and Context
memory: Enable to maintain conversation history
respect_context_window: Prevents token limit issues
knowledge_sources: Add domain-specific knowledge bases
​
Execution Control
max_iter: Maximum attempts before giving best answer
max_execution_time: Timeout in seconds
max_rpm: Rate limiting for API calls
max_retry_limit: Retries on error
​
Code Execution
allow_code_execution: Must be True to run code
code_execution_mode:
"safe": Uses Docker (recommended for production)
"unsafe": Direct execution (use only in trusted environments)
This runs a default Docker image. If you want to configure the docker image, the checkout the Code Interpreter Tool in the tools section. Add the code interpreter tool as a tool in the agent as a tool parameter.

​
Advanced Features
multimodal: Enable multimodal capabilities for processing text and visual content
reasoning: Enable agent to reflect and create plans before executing tasks
inject_date: Automatically inject current date into task descriptions
​
Templates
system_template: Defines agent’s core behavior
prompt_template: Structures input format
response_template: Formats agent responses
When using custom templates, ensure that both system_template and prompt_template are defined. The response_template is optional but recommended for consistent output formatting.

When using custom templates, you can use variables like {role}, {goal}, and {backstory} in your templates. These will be automatically populated during execution.

### Memory
```python
from crewai import Agent

analyst = Agent(
    role="Data Analyst",
    goal="Analyze and remember complex data patterns",
    memory=True,  # Enable memory
    verbose=True
)
```
When `memory` is enabled, the agent will maintain context across multiple interactions, improving its ability to handle complex, multi-step tasks.

### Context Window Management
### How Context Window Management Works

When an agent’s conversation history grows too large for the LLM’s context window, CrewAI automatically detects this situation and can either:

1. **Automatically summarize content** (when `respect_context_window=True`)
2. **Stop execution with an error** (when `respect_context_window=False`)
```python
# Agent with automatic context management (default)
smart_agent = Agent(
    role="Research Analyst",
    goal="Analyze large documents and datasets",
    backstory="Expert at processing extensive information",
    respect_context_window=True,  # 🔑 Default: auto-handle context limits
    verbose=True
)
```
### Automatic Context Handling (`respect_context_window=True`)

This is the **default and recommended setting** for most use cases. When enabled, CrewAI willl

**What happens when context limits are exceeded:**

- ⚠️ **Warning message**: `"Context length exceeded. Summarizing content to fit the model context window."`
- 🔄 **Automatic summarization**: CrewAI intelligently summarizes the conversation history
- ✅ **Continued execution**: Task execution continues seamlessly with the summarized context
- 📝 **Preserved information**: Key information is retained while reducing token count

### Strict Context Limits (`respect_context_window=False`)

When you need precise control and prefer execution to stop rather than lose any information:
```python
# Agent with strict context limits
strict_agent = Agent(
    role="Legal Document Reviewer",
    goal="Provide precise legal analysis without information loss",
    backstory="Legal expert requiring complete context for accurate analysis",
    respect_context_window=False,  # ❌ Stop execution on context limit
    verbose=True
)
```

**What happens when context limits are exceeded:**
- ❌ **Error message**: `"Context length exceeded. Consider using smaller text or RAG tools from crewai_tools."`
- 🛑 **Execution stops**: Task execution halts immediately
- 🔧 **Manual intervention required**: You need to modify your approach

### Choosing the Right Setting
Use `respect_context_window=True` (Default) when:

- **Processing large documents** that might exceed context limits
- **Long-running conversations** where some summarization is acceptable
- **Research tasks** where general context is more important than exact details
- **Prototyping and development** where you want robust execution
#### Use `respect_context_window=False` when:
- **Precision is critical** and information loss is unacceptable
- **Legal or medical tasks** requiring complete context
- **Code review** where missing details could introduce bugs
- **Financial analysis** where accuracy is paramount

### Alternative Approaches for Large Data

When dealing with very large datasets, consider these strategies:
1. Use RAG Tools
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
2. Use Knowledge Sources
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

Context Window Best Practices

1. **Monitor Context Usage**: Enable `verbose=True` to see context management in action
2. **Design for Efficiency**: Structure tasks to minimize context accumulation
3. **Use Appropriate Models**: Choose LLMs with context windows suitable for your tasks
4. **Test Both Settings**: Try both `True` and `False` to see which works better for your use case
5. **Combine with RAG**: Use RAG tools for very large datasets instead of relying solely on context windows

### Kickoff()
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

|Parameter|Type|Description|
|---|---|---|
|`messages`|`Union[str, List[Dict[str, str]]]`|Either a string query or a list of message dictionaries with role/content|
|`response_format`|`Optional[Type[Any]]`|Optional Pydantic model for structured output|
The method returns a `LiteAgentOutput` object with the following properties:
- `raw`: String containing the raw output text
- `pydantic`: Parsed Pydantic model (if a `response_format` was provided)
- `agent_role`: Role of the agent that produced the output
- `usage_metrics`: Token usage metrics for the execution

## Important Considerations and Best Practices
Security and Code Execution

- When using `allow_code_execution`, be cautious with user input and always validate it
- Use `code_execution_mode: "safe"` (Docker) in production environments
- Consider setting appropriate `max_execution_time` limits to prevent infinite loops

Performance Optimization
- Use `respect_context_window: true` to prevent token limit issues
- Set appropriate `max_rpm` to avoid rate limiting
- Enable `cache: true` to improve performance for repetitive tasks
- Adjust `max_iter` and `max_retry_limit` based on task complexity

Memory and Context Management

- Leverage `knowledge_sources` for domain-specific information
- Configure `embedder` when using custom embedding models
- Use custom templates (`system_template`, `prompt_template`, `response_template`) for fine-grained control over agent behavior

Advanced Features

- Enable `reasoning: true` for agents that need to plan and reflect before executing complex tasks
- Set appropriate `max_reasoning_attempts` to control planning iterations (None for unlimited attempts)
- Use `inject_date: true` to provide agents with current date awareness for time-sensitive tasks
- Customize the date format with `date_format` using standard Python datetime format codes
- Enable `multimodal: true` for agents that need to process both text and visual content

Agent Collaboration

- Enable `allow_delegation: true` when agents need to work together
- Use `step_callback` to monitor and log agent interactions
- Consider using different LLMs for different purposes:
    - Main `llm` for complex reasoning
    - `function_calling_llm` for efficient tool usage

Date Awareness and Reasoning

- Use `inject_date: true` to provide agents with current date awareness for time-sensitive tasks
- Customize the date format with `date_format` using standard Python datetime format codes
- Valid format codes include: %Y (year), %m (month), %d (day), %B (full month name), etc.
- Invalid date formats will be logged as warnings and will not modify the task description
- Enable `reasoning: true` for complex tasks that benefit from upfront planning and reflection

Model Compatibility

- Set `use_system_prompt: false` for older models that don’t support system messages
- Ensure your chosen `llm` supports the features you need (like function calling)

Troubleshooting Common Issues

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
