### Task Execution Flow
Tasks can be executed in two ways:
- **Sequential**: Tasks are executed in the order they are defined
- **Hierarchical**: Tasks are assigned to agents based on their roles and expertise
- 
```python
crew = Crew(
    agents=[agent1, agent2],
    tasks=[task1, task2],
    process=Process.sequential  # or Process.hierarchical
)
```

## Task Attributes

| Attribute           | Parameters        | Type  | Description                                                      |
| ------------------- | ----------------- | ----- | ---------------------------------------------------------------- |
| **Description**     | `description`     | `str` | A clear, concise statement of what the task entails.             |
| **Expected Output** | `expected_output` | `str` | A detailed description of what the task’s completion looks like. |
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
### Task Methods and Properties

|Method/Property|Description|
|---|---|
|**json**|Returns the JSON string representation of the task output if the output format is JSON.|
|**to_dict**|Converts the JSON and Pydantic outputs to a dictionary.|
|**str**|Returns the string representation of the task output, prioritizing Pydantic, then JSON, then raw.|
```python
task1 = Task(
    description="""Create a blog title and content on a given topic. Make sure the content is under 200 words.""",
    expected_output="A compelling blog title and well-written content.",
    agent=blog_agent,
    output_pydantic=Blog,
)
```