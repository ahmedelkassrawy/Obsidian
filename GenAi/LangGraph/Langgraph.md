When you build an agent with LangGraph, you will first break it apart into discrete steps called **nodes**
Then, you will describe the different decisions and transitions from each of your nodes. 
Finally, you connect nodes together through a shared **state** that each node can read from and write to

```
The agent should:

- Read incoming customer emails
- Classify them by urgency and topic
- Search relevant documentation to answer questions
- Draft appropriate responses
- Escalate complex issues to human agents
- Schedule follow-ups when needed

Example scenarios to handle:

1. Simple product question: "How do I reset my password?"
2. Bug report: "The export feature crashes when I select PDF format"
3. Urgent billing issue: "I was charged twice for my subscription!"
4. Feature request: "Can you add dark mode to the mobile app?"
5. Complex technical issue: "Our API integration fails intermittently with 504 errors"
```

---
Step 1: Map out your workflow as discrete steps

![[Pasted image 20260222040714.png]]

----
Step 2: Identify what each step needs to do

llm steps : when a step needs to understand , analyze , genrate text or make reasoning decisions
- Classify intent
	- Static context (prompt): Classification categories, urgency definitions, response format
	- Dynamic context (from state): Email content, sender information
	- Desired outcome: Structured classification that determines routing
- Draft reply
	- Static context (prompt): Tone guidelines, company policies, response templates
	- Dynamic context (from state): Classification results, search results, customer history
	- Desired outcome: Professional email response ready for review

data steps: When a step needs to retrieve information from external sources
- Doc search
	- Parameters: Query built from intent and topic
	- Retry strategy: Yes, with exponential backoff for transient failures
	- Caching: Could cache common queries to reduce API calls
- Customer history lookup
	- Parameters: Customer email or ID from state
	- Retry strategy: Yes, but with fallback to basic info if unavailable
	- Caching: Yes, with time-to-live to balance freshness and performance

action steps: When a step needs to perform an external action
- Send reply
	- When to execute node: After approval (human or automated)
	- Retry strategy: Yes, with exponential backoff for network issues
	- Should not cache: Each send is a unique action
- Bug track
	- When to execute node: Always when intent is “bug”
	- Retry strategy: Yes, critical to not lose bug reports
	- Returns: Ticket ID to include in response
   
User input steps
- Human review node
	- Context for decision: Original email, draft response, urgency, classification
	- Expected input format: Approval boolean plus optional edited response
	- When triggered: High urgency, complex issues, or quality concerns
---
Step 3: Design your state

What belongs in state?
Ask yourself these questions about each piece of data:
- Include in state
	Does it need to persist across steps? If yes, it goes in state.
- Don't store
	Can you derive it from other data? If yes, compute it when needed instead of storing it in state.

Here we need to track:
- email , sender info
- classification results (needed by nodes afterwards)
- search results and customer data (expensive)
- The draft response (needs to persist through review)
- Execution metadata (for debugging and recovery)

>[!tip]
>Keep state raw, format prompts on-demand
>Your state should store raw data, not formatted text.
>Format prompts inside nodes when you need them.

Define the state:
```python
from typing import TypedDict, Literal

class EmailClassification(TypedDict): 
	intent: Literal["question", "bug", "billing", "feature", "complex"] 
	urgency: Literal["low", "medium", "high", "critical"] 
	topic: str 
	summary: str
	
class EmailAgentState(TypedDict):
	email_content: str
	sender_email:str
	email_id:str
	
	classification:EmailClassification | None
	
	search_results: list[str] | None
	customer_history: dict | None
	
	draft_response: str | None
	messages:list[str] | None
```
all are raw data no formatted

Handle errors appropriately:

| Error Type                                                      | Who Fixes It       | Strategy                           | When to Use                                      |
| --------------------------------------------------------------- | ------------------ | ---------------------------------- | ------------------------------------------------ |
| Transient errors (network issues, rate limits)                  | System (automatic) | Retry policy                       | Temporary failures that usually resolve on retry |
| LLM-recoverable errors (tool failures, parsing issues)          | LLM                | Store error in state and loop back | LLM can see the error and adjust its approach    |
| User-fixable errors (missing information, unclear instructions) | Human              | Pause with `interrupt()`           | Need user input to proceed                       |
| Unexpected errors                                               | Developer          | Let them bubble up                 | Unknown issues that need debugging               |

Transient errors
```python
from langgraph.types import RetryPolicy

workflow.add_node(
    "search_documentation",
    search_documentation,
    retry_policy=RetryPolicy(max_attempts=3, initial_interval=1.0)
)
```

LLM-recoverable
```python
from langgraph.types import Command

def execute_tool(state:State) -> Command(Literal["agent","execute_tool"]):
	try:
		result = run_tool(state["tool_call"])
		return Command(
			update = {"tool_result":result},
			goto = "agent"
		)
	except ToolError as e:
		#let the llm see what went wrong
		return Command(
			update = {"tool_result": f"Tool error: {str(e)}"},
			goto = "agent"
		)
```

User fixable
Pause and collect information from the user when needed (like account IDs, order numbers, or clarifications):
```python
from langgraph.types import Command

def lookup_customer_history(state:State) -> Command[Literal["draft_response"]]:
	if not state.get("customer_id"):
		user_input = interrupt(
			{
				"message": "Customer ID needed",
				"request": "Please provide the cusotmer account ID to lookup"
			}
		)
		return Command(
			update = {"customer_id": user_input["customer_id"]},
			goto = "lookup_customer_history"
		)
		
	customer_data = fetch_customer_history(state["customer_id"])
	return Command(
		update = {"customer_history":customer_data},
		goto = "draft_response"
	)
```

Unexpected:
```python
def send_reply(state: EmailAgentState): 
	try: 
		email_service.send(state["draft_response"]) 
	except Exception: 
		raise # Surface unexpected errors
```
---
Implementing Our nodes

Read and classify nodes
```python
from typing import Literal
from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt, Command, RetryPolicy
from langchain_openai import ChatOpenAI
from langchain.messages import HumanMessage

def read_email(state:EmailAgentState) -> dict:
	"""Extract and parse email content"""
	return {
		"messages": [HumanMessage(content = f"Processing email: {state['email_content']}")]
	}
	
def classify_intent(state:EmailAgentState) -> Command[Literal["search_documentation", "human_review", "draft_response", "bug_tracking"]]:
	#create a llm with structured output to get email classification
	structured_llm = llm.with_structured_output(EmailClassification)
	
	#format prompt 
	classification_prompt = f"""
	Analyze this customer email and classify it: 
	Email: {state['email_content']} 
	From: {state['sender_email']} 
	
	Provide classification including intent, urgency, topic, and summary.
	"""
	
	classification = structured_llm.invoke(classification_prompt)
	
	if classification["intent"] == "billing" or classification['urgency'] == 'critical':
		goto = "human_review"
	elif classification["intent"] in ["question","feature"]:
		goto = "search_documentation"
	elif classification["intent"] == "bug":
		goto = "bug_tracking"
	else: 
		goto = "draft_response"
		
	return Command(
		update = {"classification":classification},
		goto = goto
	)
```

```python
def search_documentation(state: EmailAgentState) -> Command[Literal["draft_response"]]:
    """Search knowledge base for relevant information"""

    # Build search query from classification
    classification = state.get('classification', {})
    query = f"{classification.get('intent', '')} {classification.get('topic', '')}"

    try:
        # Implement your search logic here
        # Store raw search results, not formatted text
        search_results = [
            "Reset password via Settings > Security > Change Password",
            "Password must be at least 12 characters",
            "Include uppercase, lowercase, numbers, and symbols"
        ]
    except SearchAPIError as e:
        # For recoverable search errors, store error and continue
        search_results = [f"Search temporarily unavailable: {str(e)}"]

    return Command(
        update={"search_results": search_results},  # Store raw results or error
        goto="draft_response"
    )

def bug_tracking(state: EmailAgentState) -> Command[Literal["draft_response"]]:
    """Create or update bug tracking ticket"""

    # Create ticket in your bug tracking system
    ticket_id = "BUG-12345"  # Would be created via API

    return Command(
        update={
            "search_results": [f"Bug ticket {ticket_id} created"],
            "current_step": "bug_tracked"
        },
        goto="draft_response"
    )
```

```python
def draft_response(state: EmailAgentState) -> Command[Literal["human_review", "send_reply"]]:
	"""Generate response using context and route based on quality"""
	classification = state.get("classification",{})
	
	#format context from raw state data 
	context_sections = []
	
	if state.get("search_results):
		formated_docs = "\n".join([f"- {doc}" for doc in state['search_results']])
		context_sections.append(f"Relevant documentation: \n{formated_docs}")
		
	if state.get("customer_history"):
		context_sections.append(f"Customer tier: {state['customer_history'].get('tier', 'standard')}")
		
	draft_prompt = f"""
	Draft response to this customer email:
	{state["email_content"]}
	
	Email intent: {classification.get("intent","unkown")}
	Urgency Level: {classification.get("urgency","medium")}
	
	{chr(10).join(context_sections)} 
	Guidelines: 
	- Be professional and helpful 
    - Address their specific concern 
	- Use the provided documentation when relevant
	"""
	
	response = llm.invoke(draft_prompt)
	
	#determine if human review is needed:
	needs_review = (
		classification.get("urgency") in ["high","critical"] or classification.get('intent') == 'complex' 
	)
	
	if needs_review:
		goto = "human_review"
	else:
		goto = "send_reply"
		
	return Command(
		update = {"draft_response":response.content},
		goto = goto
	)
	
def human_review(state: EmailAgentState) -> Command[Literal["send_reply", END]]: 
	"""Pause for human review using interrupt and route based on decision"""
	
	classification = state.get("classification",{})
	
	# interrupt() must come first - any code before it will re-run on resume
	human_decision = interrupt(
		{
			"email_id": state.get("email_id",""),
			"original_email": state.get("email_content", ""),
			"draft_response": state.get("draft_response",""),
			"urgency": classification.get("urgency"),
			"intent": classification.get("intent"),
			"action": "Please review and approve/edit this response" #hitl needed
		}
	)
	
	if human_decision.get("approved"):
		return Command(
			update = {"draft_response":human_decision.get("edited_response",state.get('draft_response',''))},
			goto = "send_reply"
		)
	else:
		#rejection means human will handle 
		return Command(
			update = {},
			goto = END
		)
		
def send_reply(state:EmailAgentState) -> dict:
	"""Send the email reply"""
	print(f"Sending reply: {state['draft_response'][:100]}...")
    return {}
```

---
Wire it up
To enable [human-in-the-loop](https://docs.langchain.com/oss/python/langgraph/interrupts) with `interrupt()`, we need to compile with a [checkpointer](https://docs.langchain.com/oss/python/langgraph/persistence) to save state between runs:
```python
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import RetryPolicy

# Create the graph
workflow = StateGraph(EmailAgentState)

# Add nodes with appropriate error handling
workflow.add_node("read_email", read_email)
workflow.add_node("classify_intent", classify_intent)

# Add retry policy for nodes that might have transient failures
workflow.add_node(
    "search_documentation",
    search_documentation,
    retry_policy=RetryPolicy(max_attempts=3)
)
workflow.add_node("bug_tracking", bug_tracking)
workflow.add_node("draft_response", draft_response)
workflow.add_node("human_review", human_review)
workflow.add_node("send_reply", send_reply)

# Add only the essential edges
workflow.add_edge(START, "read_email")
workflow.add_edge("read_email", "classify_intent")
workflow.add_edge("send_reply", END)

# Compile with checkpointer for persistence, in case run graph with Local_Server --> Please compile without checkpointer
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)
```

The graph structure is minimal because routing happens inside nodes through `Command`. 
Each node declares where it can go using type hints like `Command[Literal["node1", "node2"]]`, making the flow explicit and traceable.

Testing the agent
```python
# Test with an urgent billing issue
initial_state = {
    "email_content": "I was charged twice for my subscription! This is urgent!",
    "sender_email": "customer@example.com",
    "email_id": "email_123",
    "messages": []
}

# Run with a thread_id for persistence
config = {"configurable": {"thread_id": "customer_123"}}
result = app.invoke(initial_state, config)
# The graph will pause at human_review
print(f"human review interrupt:{result['__interrupt__']}")

# When ready, provide human input to resume
from langgraph.types import Command

human_response = Command(
    resume={
        "approved": True,
        "edited_response": "We sincerely apologize for the double charge. I've initiated an immediate refund..."
    }
)

# Resume execution
final_result = app.invoke(human_response, config)
print(f"Email sent successfully!")
```

Invoking the Agent
```python
def run_agent():
    session_count = 0

    while True:
        print("=" * 50)
        
        query = input("Enter a query (or 'exit' to quit): ").strip()
        if query.lower() in ("exit", "quit"):
            print("Goodbye!")
            break

        session_count += 1
        config = {"configurable": {"thread_id": f"session_{session_count}"}}

        initial_state = {
            "patient_id": "",
            "reason_for_visit": "",
            "classification": None,
            "patient_history": None,
            "messages": []
        }

        result = agent.invoke(initial_state, config)
        result = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user", 
                        "content": query
                    }
                ]
            }, config
        )

        # Handle interrupt loop
        while "__interrupt__" in result:
            current_interrupt = result["__interrupt__"][0]
            print("Interrupt:", current_interrupt.value)

            user_response = input(f"{current_interrupt.value['request']}: ").strip()
            
            if user_response.lower() in ("exit", "quit"):
                print("Exiting session.")
                return

            # Resume with the user's input
            result = agent.invoke(Command(resume=user_response), config)

        # Display a user-friendly summary
        print("\n" + "=" * 50)
        print("✅ Session Complete!")
        print(f"  Patient ID    : {result.get('patient_id', 'N/A')}")
        print(f"  Reason        : {result.get('reason_for_visit', 'N/A')}")
        
        classification = result.get("classification")
        
        if classification:
            print(f"  Urgency       : {classification.get('urgency', 'N/A')}")
            print(f"  Department    : {classification.get('department', 'N/A')}")
            print(f"  Topic         : {classification.get('topic', 'N/A')}")
        print("=" * 50)


if __name__ == "__main__":
    run_agent()
```