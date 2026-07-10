- a `Task` is a specific assignment completed by an `Agent`.
- Tasks provide all necessary details for execution, such as a description, the agent responsible, required tools, and more, facilitating a wide range of action complexities.
- Tasks within CrewAI can be collaborative, requiring multiple agents to work together.

### Task Execution Flow

Tasks can be executed in two ways:

- **Sequential**: Tasks are executed in the order they are defined
- **Hierarchical**: Tasks are assigned to agents based on their roles and expertise

The execution flow is defined when creating the crew:

```python
crew = Crew(
    agents=[agent1, agent2],
    tasks=[task1, task2],
    process=Process.sequential  # or Process.hierarchical
)
```

## ## Task Attributes

|Attribute|Parameters|Type|Description|
|---|---|---|---|
|**Description**|`description`|`str`|A clear, concise statement of what the task entails.|
|**Expected Output**|`expected_output`|`str`|A detailed description of what the task’s completion looks like.|
|**Name** _(optional)_|`name`|`Optional[str]`|A name identifier for the task.|
|**Agent** _(optional)_|`agent`|`Optional[BaseAgent]`|The agent responsible for executing the task.|
|**Tools** _(optional)_|`tools`|`List[BaseTool]`|The tools/resources the agent is limited to use for this task.|
|**Context** _(optional)_|`context`|`Optional[List["Task"]]`|Other tasks whose outputs will be used as context for this task.|
|**Async Execution** _(optional)_|`async_execution`|`Optional[bool]`|Whether the task should be executed asynchronously. Defaults to False.|
|**Human Input** _(optional)_|`human_input`|`Optional[bool]`|Whether the task should have a human review the final answer of the agent. Defaults to False.|
|**Markdown** _(optional)_|`markdown`|`Optional[bool]`|Whether the task should instruct the agent to return the final answer formatted in Markdown. Defaults to False.|
|**Config** _(optional)_|`config`|`Optional[Dict[str, Any]]`|Task-specific configuration parameters.|
|**Output File** _(optional)_|`output_file`|`Optional[str]`|File path for storing the task output.|
|**Create Directory** _(optional)_|`create_directory`|`Optional[bool]`|Whether to create the directory for output_file if it doesn’t exist. Defaults to True.|
|**Output JSON** _(optional)_|`output_json`|`Optional[Type[BaseModel]]`|A Pydantic model to structure the JSON output.|
|**Output Pydantic** _(optional)_|`output_pydantic`|`Optional[Type[BaseModel]]`|A Pydantic model for task output.|
|**Callback** _(optional)_|`callback`|`Optional[Any]`|Function/object to be executed after task completion.|
|**Guardrail** _(optional)_|`guardrail`|`Optional[Callable]`|Function to validate task output before proceeding to next task.|
|**Guardrails** _(optional)_|`guardrails`|`Optional[List[Callable]]`|List of guardrails to validate task output before proceeding to next task.|
|**Guardrail Max Retries** _(optional)_|`guardrail_max_retries`|`Optional[int]`|Maximum number of retries when guardrail validation fails. Defaults to 3.|


```python
from crewai import Task

research_task = Task(
    description="""
        Conduct a thorough research about AI Agents.
        Make sure you find any interesting and relevant information given
        the current year is 2025.
    """,
    expected_output="""
        A list with 10 bullet points of the most relevant information about AI Agents
    """,
    agent=researcher
)

reporting_task = Task(
    description="""
        Review the context you got and expand each topic into a full section for a report.
        Make sure the report is detailed and contains any and all relevant information.
    """,
    expected_output="""
        A fully fledge reports with the mains topics, each with a full section of information.
    """,
    agent=reporting_analyst,
    markdown=True,  # Enable markdown formatting for the final output
    output_file="report.md"
)
```

## Task Output
Understanding task outputs is crucial for building effective AI workflows. CrewAI provides a structured way to handle task results through the `TaskOutput` class, which supports multiple output formats and can be easily passed between tasks.

This class provides a structured way to access results of a task, including various formats such as raw output, JSON, and Pydantic models.

By default, the `TaskOutput` will only include the `raw` output. A `TaskOutput` will only include the `pydantic` or `json_dict` output if the original `Task` object was configured with `output_pydantic` or `output_json`, respectively.

### Task Output Attributes

|Attribute|Parameters|Type|Description|
|---|---|---|---|
|**Description**|`description`|`str`|Description of the task.|
|**Summary**|`summary`|`Optional[str]`|Summary of the task, auto-generated from the first 10 words of the description.|
|**Raw**|`raw`|`str`|The raw output of the task. This is the default format for the output.|
|**Pydantic**|`pydantic`|`Optional[BaseModel]`|A Pydantic model object representing the structured output of the task.|
|**JSON Dict**|`json_dict`|`Optional[Dict[str, Any]]`|A dictionary representing the JSON output of the task.|
|**Agent**|`agent`|`str`|The agent that executed the task.|
|**Output Format**|`output_format`|`OutputFormat`|The format of the task output, with options including RAW, JSON, and Pydantic. The default is RAW.|
|**Messages**|`messages`|`list[LLMMessage]`|The messages from the last task execution.|

### Task Methods and Properties

|Method/Property|Description|
|---|---|
|**json**|Returns the JSON string representation of the task output if the output format is JSON.|
|**to_dict**|Converts the JSON and Pydantic outputs to a dictionary.|
|**str**|Returns the string representation of the task output, prioritizing Pydantic, then JSON, then raw.|

### Accessing Task Outputs

Once a task has been executed, its output can be accessed through the `output` attribute of the `Task` object. The `TaskOutput` class provides various ways to interact with and present this output.

#### Example

```python
# Example task
task = Task(
    description='Find and summarize the latest AI news',
    expected_output='A bullet list summary of the top 5 most important AI news',
    agent=research_agent,
    tools=[search_tool]
)

# Execute the crew
crew = Crew(
    agents=[research_agent],
    tasks=[task],
    verbose=True
)

result = crew.kickoff()

# Accessing the task output
task_output = task.output

print(f"Task Description: {task_output.description}")
print(f"Task Summary: {task_output.summary}")
print(f"Raw Output: {task_output.raw}")
if task_output.json_dict:
    print(f"JSON Output: {json.dumps(task_output.json_dict, indent=2)}")
if task_output.pydantic:
    print(f"Pydantic Output: {task_output.pydantic}")
```

## Markdown Output Formatting

The `markdown` parameter enables automatic markdown formatting for task outputs. When set to `True`, the task will instruct the agent to format the final answer using proper Markdown syntax.

Using Markdown Formatting
```python
# Example task with markdown formatting enabled
formatted_task = Task(
    description="Create a comprehensive report on AI trends",
    expected_output="A well-structured report with headers, sections, and bullet points",
    agent=reporter_agent,
    markdown=True  # Enable automatic markdown formatting
)
```

When `markdown=True`, the agent will receive additional instructions to format the output using:

- `#` for headers
- `**text**` for bold text
- `*text*` for italic text
- `-` or `*` for bullet points
- `` `code` `` for inline code
- language ``` for code blocks ```

### Benefits of Markdown Output

- **Consistent Formatting**: Ensures all outputs follow proper markdown conventions
- **Better Readability**: Structured content with headers, lists, and emphasis
- **Documentation Ready**: Output can be directly used in documentation systems
- **Cross-Platform Compatibility**: Markdown is universally supported

## Task Dependencies and Context
Tasks can depend on the output of other tasks using the `context` attribute. For example:

```python
research_task = Task(
    description="Research the latest developments in AI",
    expected_output="A list of recent AI developments",
    agent=researcher
)

analysis_task = Task(
    description="Analyze the research findings and identify key trends",
    expected_output="Analysis report of AI trends",
    agent=analyst,
    context=[research_task]  # This task will wait for research_task to complete
)
```

## Task Guardrails

Task guardrails provide a way to validate and transform task outputs before they are passed to the next task. This feature helps ensure data quality and provides feedback to agents when their output doesn’t meet specific criteria.CrewAI supports two types of guardrails:

1. **Function-based guardrails**: Python functions with custom validation logic, giving you complete control over the validation process and ensuring reliable, deterministic results.
2. **LLM-based guardrails**: String descriptions that use the agent’s LLM to validate outputs based on natural language criteria. These are ideal for complex or subjective validation requirements.

- An Agent defines _who_ does the work (role, goal, backstory, tools), 
- while a Task defines _what_ work to do and _what output_ is expected. 
- Tasks give you structured control: explicit descriptions, expected outputs, context chaining from other tasks, guardrails, async execution, output files/Pydantic schemas, and orchestration via a Crew's sequential or hierarchical process — things a bare agent call doesn't provide.

Per CrewAI's 80/20 rule, task design matters more than agent design for execution quality. You can call `agent.kickoff(...)` directly for one-shot prompts (as shown on your migration page), but Tasks are what enable multi-step, validated, agent-collaborative workflows.