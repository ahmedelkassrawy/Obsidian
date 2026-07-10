I added HITL middleware to the subgraphs
Added checkpointer to the top level agent (supervisor agent) which is required to pause and resume execution

System Layers Architecture:
1. Bottom layer: tools before getting used in the sub-agents
2. Middle Layer: the subagents
3. Top Layer: The supervisor agent that uses and coordinates the sub-agents

**When to use the supervisor pattern**
- Use the supervisor pattern when you have multiple distinct domains (calendar, email, CRM, database), each domain has multiple tools or complex logic, you want centralized workflow control, and sub-agents don’t need to converse directly with users.

- For simpler cases with just a few tools, use a single agent. When agents need to have conversations with users, use [handoffs](https://docs.langchain.com/oss/python/langchain/multi-agent/handoffs) instead. 
- For peer-to-peer collaboration between agents, consider other multi-agent patterns.

```python
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain.tools import tool
from typing import Optional
from langsmith.run_helpers import traceable
from dotenv import load_dotenv
from langchain.agents.middleware import HumanInTheLoopMiddleware 
from langgraph.checkpoint.memory import InMemorySaver 
import os

os.environ["GROQ_API_KEY"] = "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"

os.environ["LANGSMITH_TRACING"]="true"
os.environ["LANGSMITH_API_KEY"] ="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"
os.environ["LANGSMITH_PROJECT"]="atlas"
os.environ["LANGSMITH_ENDPOINT"] = "https://api.smith.langchain.com"

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=os.getenv("GROQ_API_KEY"),
)

@tool
@traceable
def create_calendar_event(title:str, 
    start_time:str,end_time:str,
    attendees: list[str],location:str = "") -> str:
    """Create a calendar event. Requires exact ISO datetime format"""
    return f"Event created: {title} from {start_time} to {end_time} with {len(attendees)} attendees at {location}"

@tool
@traceable
def send_email(to:list[str],subject:str,body:str,
               cc:list[str] = []) -> str:
    """Send an email."""
    return f"Email sent to {', '.join(to)} with subject: {subject}"

@tool
@traceable
def get_available_time_slots(attendees:Optional[list[str]],date:str,
                             duration_minutes:int) -> list[str]:
    """Check calendar availability for attendees and return available time slots."""
    return ["09:00","14:00","16:00"]

CALENDAR_AGENT_PROMPT = (
    "You are a calendar scheduling assistant."
    "Parse natural language scheduling requests (eg. 'next Tuesday at 2pm')"
    "into proper ISO datetime format."
    "Use get_available_time_slots to check the time slots availability when needed."
    "Use create_calendar_event to schedule events."
    "Always confirm what was scheduled in your final response."
)

calendar_agent = create_agent(llm,
                              tools = [create_calendar_event, get_available_time_slots],
                              system_prompt = CALENDAR_AGENT_PROMPT,
                              middleware=[
                                  HumanInTheLoopMiddleware(
                                      interrupt_on = {"create_calendar_event": True},
                                      description_prefix="Calendar event pending approval"
                                  ),
                              ])

EMAIL_AGENT_PROMPT = (
    "You are an email assistant."
    "Compose professional emails based on natural language requests"
    "Extract recieptnt information and craft a clear subject and body for the email."
    "Use send_email to send the message"
    "Always confirm what was sent in your final response."
)
email_agent = create_agent(llm,
                        tools = [send_email],
                        system_prompt=EMAIL_AGENT_PROMPT,
                        middleware = [
                            HumanInTheLoopMiddleware(
                                interrupt_on = {"send_email": True},
                                description_prefix="Outbound email pending approval",
                            ),
                        ])

@tool
@traceable
def schedule_event(request:str) -> str:
    """Schedule calendar events based on natural language requests.
    Use this when the user wants to create, modify, or check calendar appointments.
    Handles date/time parsing, availability checking, and event creation.

    Input: Natural language scheduling request (e.g., 'meeting with design team
    next Tuesday at 2pm')
    """

    result = calendar_agent.invoke(
        {
            "messages": [
                {
                    "role":"user",
                    "content":request
                }
            ]
        }
    )

    return result["messages"][-1].text
@tool
@traceable
def manage_email(request: str) -> str:
    """Send emails using natural language.

    Use this when the user wants to send notifications, reminders, or any email
    communication. Handles recipient extraction, subject generation, and email
    composition.

    Input: Natural language email request (e.g., 'send them a reminder about
    the meeting')
    """
    result = email_agent.invoke(
        {
            "messages": [
                {
                    "role": "user", 
                    "content": request
                }
            ]
        }
    )
    return result["messages"][-1].text

SUPERVISOR_PROMPT = (
    "You are a helpful personal assistant. "
    "You can schedule calendar events and send emails. "
    "Break down user requests into appropriate tool calls and coordinate the results. "
    "When a request involves multiple actions, use multiple tools in sequence."
)

supervisor_agent = create_agent(
    llm,
    tools=[schedule_event, manage_email],
    system_prompt=SUPERVISOR_PROMPT,
    checkpointer=InMemorySaver(), 
)
```

```python
query = (
    "Schedule a meeting with the design team next Tuesday at 2pm for 1 hour, "
    "and send them an email reminder about reviewing the new mockups."
)

for step in supervisor_agent.stream(
    {
	    "messages": 
		    [
			    {
				    "role": "user", 
				    "content": query
				}
			]
	}
):
    for update in step.values():
        for message in update.get("messages", []):
            message.pretty_print()
```

```python
query = (
    "Schedule a meeting with the design team next Tuesday at 2pm for 1 hour, "
    "and send them an email reminder about reviewing the new mockups."
)

config = {"configurable": {"thread_id": "6"}}

interrupts = []
for step in supervisor_agent.stream(
    {
        "messages": [
            {
                "role":"user",
                "content":query
            }
        ]
    },
    config = config,
):
    for update in step.values():
        if isinstance(update,dict):
            for message in update.get("messages",[]):
                message.pretty_print()
        else:
            interrupt_ = update[0]
            interrupts.append(interrupt_)

            print(f"\nINTERRUPTED: {interrupt_.id}")
```

We can specify decisions for each interrupt by referring to its ID using a [`Command`](https://reference.langchain.com/python/langgraph/types/#langgraph.types.Command).

```python
from langgraph.types import Command 

resume = {}
for interrupt_ in interrupts:
    if interrupt_.id == "2b56f299be313ad8bc689eff02973f16":
        # Edit email
        edited_action = interrupt_.value["action_requests"][0].copy()
        edited_action["args"]["subject"] = "Mockups reminder"
        resume[interrupt_.id] = {
            "decisions": [{"type": "edit", "edited_action": edited_action}]
        }
    else:
        resume[interrupt_.id] = {"decisions": [{"type": "approve"}]}

interrupts = []
for step in supervisor_agent.stream(
    Command(resume=resume), 
    config,
):
    for update in step.values():
        if isinstance(update, dict):
            for message in update.get("messages", []):
                message.pretty_print()
        else:
            interrupt_ = update[0]
            interrupts.append(interrupt_)
            print(f"\nINTERRUPTED: {interrupt_.id}")
```

## Advanced: Control information flow
By default, sub-agents receive only the request string from the supervisor. You might want to pass additional context, such as conversation history or user preferences.

Pass additional conversational context to sub-agents
```python
from langchain.tools import tool, ToolRuntime

@tool
def schedule_event(
    request: str,
    runtime: ToolRuntime
) -> str:
    """Schedule calendar events using natural language."""
    # Customize context received by sub-agent
    original_user_message = next(
        message for message in runtime.state["messages"]
        if message.type == "human"
    )
    prompt = (
        "You are assisting with the following user inquiry:\n\n"
        f"{original_user_message.text}\n\n"
        "You are tasked with the following sub-request:\n\n"
        f"{request}"
    )
    result = calendar_agent.invoke({
        "messages": [{"role": "user", "content": prompt}],
    })
    return result["messages"][-1].text
```
This allows sub-agents to see the full conversation context, which can be useful for resolving ambiguities like “schedule it for the same time tomorrow” (referencing a previous conversation).

### Control what supervisor receives
You can also customize what information flows back to the supervisor:
```python
import json

@tool
def schedule_event(request: str) -> str:
    """Schedule calendar events using natural language."""
    result = calendar_agent.invoke({
        "messages": [{"role": "user", "content": request}]
    })

    # Option 1: Return just the confirmation message
    return result["messages"][-1].text

    # Option 2: Return structured data
    # return json.dumps({
    #     "status": "success",
    #     "event_id": "evt_123",
    #     "summary": result["messages"][-1].text
    # })
```
**Important:** Make sure sub-agent prompts emphasize that their final message should contain all relevant information. A common failure mode is sub-agents that perform tool calls but don’t include the results in their final response.
