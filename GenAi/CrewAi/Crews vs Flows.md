## How It All Works Together

1. **The Flow** triggers an event or starts a process.
2. **The Flow** manages the state and decides what to do next.
3. **The Flow** delegates a complex task to a **Crew**.
4. **The Crew**’s agents collaborate to complete the task.
5. **The Crew** returns the result to the **Flow**.
6. **The Flow** continues execution based on the result.

## When to Use Crews vs. Flows

**The short answer: Use both.**For any production-ready application, **start with a Flow**.

- **Use a Flow** to define the overall structure, state, and logic of your application.
- **Use a Crew** within a Flow step when you need a team of agents to perform a specific, complex task that requires autonomy.

|Use Case|Architecture|
|---|---|
|**Simple Automation**|Single Flow with Python tasks|
|**Complex Research**|Flow managing state -> Crew performing research|
|**Application Backend**|Flow handling API requests -> Crew generating content -> Flow saving to DB|
## The Key Distinction

The most important thing to understand: **these capabilities fall into two categories**.
### Action Capabilities (Tools, MCPs, Apps)

These give agents the ability to **do things** — call APIs, read files, search the web, send emails. At execution time, all three resolve into the same internal format (`BaseTool` instances) and appear in a unified tool list the agent can call.

```python
from crewai import Agent
from crewai_tools import SerperDevTool, FileReadTool

agent = Agent(
    role="Researcher",
    goal="Find and compile market data",
    backstory="Expert market analyst",
    tools=[SerperDevTool(), FileReadTool()],  # Local tools
    mcps=["https://mcp.example.com/sse"],     # Remote MCP server tools
    apps=["gmail", "google_sheets"],           # Platform integrations
)
```

### Context Capabilities (Skills, Knowledge)

These modify the agent’s **prompt** — injecting expertise, instructions, or retrieved data before the agent starts reasoning. They don’t give agents new actions; they shape how agents think and what information they have access to.

```python
from crewai import Agent

agent = Agent(
    role="Security Auditor",
    goal="Audit cloud infrastructure for vulnerabilities",
    backstory="Expert in cloud security with 10 years of experience",
    skills=["./skills/security-audit"],        # Domain instructions
    knowledge_sources=[pdf_source, url_source], # Retrieved facts
)
```

---

## When to Use What

|You need…|Use|Example|
|---|---|---|
|Agent to search the web|**Tools**|`tools=[SerperDevTool()]`|
|Agent to call a remote API via MCP|**MCPs**|`mcps=["https://api.example.com/sse"]`|
|Agent to send emails via Gmail|**Apps**|`apps=["gmail"]`|
|Agent to follow specific procedures|**Skills**|`skills=["./skills/code-review"]`|
|Agent to reference company docs|**Knowledge**|`knowledge_sources=[pdf_source]`|
|Agent to search the web AND follow review guidelines|**Tools + Skills**|Use both together|

---

## Combining Capabilities

In practice, agents often use **multiple capability types together**. Here’s a realistic example:

```python
from crewai import Agent
from crewai_tools import SerperDevTool, FileReadTool, CodeInterpreterTool

# A fully-equipped research agent
researcher = Agent(
    role="Senior Research Analyst",
    goal="Produce comprehensive market analysis reports",
    backstory="Expert analyst with deep industry knowledge",

    # ACTION: What the agent can DO
    tools=[
        SerperDevTool(),         # Search the web
        FileReadTool(),          # Read local files
        CodeInterpreterTool(),   # Run Python code for analysis
    ],
    mcps=["https://data-api.example.com/sse"],  # Access remote data API
    apps=["google_sheets"],                      # Write to Google Sheets

    # CONTEXT: What the agent KNOWS
    skills=["./skills/research-methodology"],    # How to conduct research
    knowledge_sources=[company_docs],            # Company-specific data
)
```

---

## Comparison Table

|Feature|Tools|MCPs|Apps|Skills|Knowledge|
|---|---|---|---|---|---|
|**Gives agent actions**|✅|✅|✅|❌|❌|
|**Modifies prompt**|❌|❌|❌|✅|✅|
|**Requires code**|Yes|Config only|Config only|Markdown only|Config only|
|**Runs locally**|Yes|Depends|Yes (with env var)|N/A|Yes|
|**Needs API keys**|Per tool|Per server|Integration token|No|Embedder only|
|**Set on Agent**|`tools=[]`|`mcps=[]`|`apps=[]`|`skills=[]`|`knowledge_sources=[]`|
|**Set on Crew**|❌|❌|❌|`skills=[]`|`knowledge_sources=[]`|