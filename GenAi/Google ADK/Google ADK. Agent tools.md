## Agent Tools Best Practice
##### The `ToolContext` Parameter
Notice the function signature includes `tool_context: ToolContext`. ADK automatically provides this object when your tool runs. It gives you two key capabilities:
1. **Request approval:** Call `tool_context.request_confirmation()`
2. **Check approval status:** Read `tool_context.tool_confirmation`

```python
LARGE_ORDER_THRESHOLD = 5

def place_shipping_order(num_containers:int,destination:str,
                        tool_context:ToolContext):
    """
    Places a shipping order for the specified number of containers to the given destination.
    If the number of containers exceeds a certain threshold, it uses a special process.
    """
    #SCENE 1 : Small order (<= 5 containers) auto approval
    if num_containers <= LARGE_ORDER_THRESHOLD:
        return {
            "status":"approved",
            "order_id": f"ORD-{num_containers}-AUTO",
            "num_containers": num_containers,
            "destination": destination,
            "message": f"Order auto-approved: {num_containers} containers to {destination}",
        }
    
    #SCENE 2 : large orders need human approval - PAUSE HERE
    if not tool_context.tool_confirmation:
        tool_context.request_confirmation(
            hint = f"Large order: {num_containers} containers to {destination}. Do you want to approve?",
            payload = {"num_containers": num_containers,
                       "destination": destination}
        )

        return { #sent to agent
            "status":"pending",
            "message": f"Order for {num_containers} containers requires approval.", 
        }

    #SCENE 3 : the tool is called AGAIN and is now resuming. Handle approval response - RESUME here
    if tool_context.tool_confirmation.confirmed:
        return {
            "status":"approved",
            "order_id":f"ORD-{num_containers}-HUMAN",
            "num_containers": num_containers,
            "destination": destination,
            "message": f"Order approved: {num_containers} conatiners to destination",
        }
    else:
        return {
            "status":"rejected",
            "message": f"Order rejected: {num_containers} containers to {destination}"
        }
```

![[Pasted image 20251122192552.png]]
#### How the Three Scenarios Work
The tool handles three scenarios by checking `tool_context.tool_confirmation`:

**Scenario 1: Small order (≤5 containers)**: Returns immediately with auto-approved status.

- `tool_context.tool_confirmation` is never checked

**Scenario 2: Large order - FIRST CALL**

- Tool detects it's a first call: `if not tool_context.tool_confirmation:`
- Calls `request_confirmation()` to request human approval
- Returns `{'status': 'pending', ...}` immediately
- **ADK automatically creates `adk_request_confirmation` event**
- Agent execution pauses - waiting for human decision

**Scenario 3: Large order - RESUMED CALL**

- Tool detects it's resuming: `if not tool_context.tool_confirmation:` is now False
- Checks human decision: `tool_context.tool_confirmation.confirmed`
- If True → Returns approved status
- If False → Returns rejected status

A regular `LlmAgent` is stateless - each call is independent with no memory of previous interactions. If a tool requests approval, the agent can't remember what it was doing.

**The solution:** Wrap your agent in an **`App`** with **resumability enabled**. The App adds a persistence layer that saves and restores state.

**What gets saved when a tool pauses:**
- All conversation messages so far
- Which tool was called (`place_shipping_order`)
- Tool parameters (10 containers, Rotterdam)
- Where exactly it paused (waiting for approval)

When you resume, the App loads this saved state so the agent continues exactly where it left off - as if no time passed

##### Create agent,app,runner
```python
shipping_agent = LlmAgent(
    name = "shipping_agent",
    model = Gemini(
        model = "gemini-2.5-flash-lite",
        retry_options= retry_config
    ),
    instruction = """You are a shipping coordinator assistant.
  
  When users request to ship containers:
   1. Use the place_shipping_order tool with the number of containers and destination
   2. If the order status is 'pending', inform the user that approval is required
   3. After receiving the final result, provide a clear summary including:
      - Order status (approved/rejected)
      - Order ID (if available)
      - Number of containers and destination
   4. Keep responses concise but informative
  """,
    tools=[FunctionTool(func=place_shipping_order)],
)
```

**Step 2: Wrap in resumable App**

**The problem:** A regular `LlmAgent` is stateless - each call is independent with no memory of previous interactions. If a tool requests approval, the agent can't remember what it was doing.

**The solution:** Wrap your agent in an **`App`** with **resumability enabled**. The App adds a persistence layer that saves and restores state.

**What gets saved when a tool pauses:**

- All conversation messages so far
- Which tool was called (`place_shipping_order`)
- Tool parameters (10 containers, Rotterdam)
- Where exactly it paused (waiting for approval)

When you resume, the App loads this saved state so the agent continues exactly where it left off - as if no time passed.

#### Create Session and Runner with the App
Pass `app=shipping_app` instead of `agent=...` so the runner knows about resumability.
```python
shipping_app = App(
    name="shipping_coordinator",
    root_agent=shipping_agent,
    resumability_config=ResumabilityConfig(is_resumable=True),
)

session_service = InMemorySessionService()

shipping_runner = Runner(
    app = shipping_app,
    session_service = session_service,
)
```

### The Critical Part - Handling Events in Your Workflow

The agent won't automatically handle pause/resume. **Every long-running operation workflow requires you to:**

1. **Detect the pause:** Check if events contain `adk_request_confirmation`
2. **Get human decision:** In production, show UI and wait for user click. Here, we simulate it.
3. **Resume the agent:** Send the decision back with the saved `invocation_id`

### 4.2 Understand Key Technical Concepts
👉 **`events`** - ADK creates events as the agent executes. Tool calls, model responses, function results - all become events

👉 **`adk_request_confirmation` event** - This event is special - it signals "pause here!"

- Automatically created by ADK when your tool calls `request_confirmation()`
- Contains the `invocation_id`
- Your workflow must detect this event to know the agent paused

👉 **`invocation_id`** - Every call to `run_async()` gets a unique `invocation_id` (like "abc123")

- When a tool pauses, you save this ID
- When resuming, pass the same ID so ADK knows which execution to continue
- Without it, ADK would start a NEW execution instead of resuming the paused one 
### Helper Functions to Process Events
These handle the event iteration logic for you.
**`check_for_approval()`** - Detects if the agent paused
- Loops through all events and looks for the special `adk_request_confirmation` event
- Returns `approval_id` (identifies this specific request) and `invocation_id` (identifies which execution to resume)
- Returns `None` if no pause detected

```python
def check_for_approval(events):
    """Check if events conatin an approval request"""

    for event in events:
        if event.content and event.content.parts:
            for part in event.content.parts:
                if(part.function_call and part.function_call.name == "adk_request_confirmation"):
                    return {
                        "approval_id": part.function_call.id,
                        "invocation_id": event.invocation_id,
                    }
    return None
```

```python
def print_agent_response(events):
    """Print agent's text responses from events"""
    for event in events:
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    print(f"Agent: {part.text}")
```

```python
def create_approval_response(approval_info,approved):
    """Create the approval response message"""
    confirmation_response = types.FunctionResponse(
        id = approval_info["approval_id"],
        name = "adk_request_confirmation",
        response = {"confirmed":approved},
    )
    return types.Content(
        role = "user",
        parts = [types.Part(function_response = confirmation_response)],
    )
```

![[Pasted image 20251122214119.png]]

```python
async def run_shipping_workflow(query:str,auto_approve:bool = True):
    """Runs a shipping workflow with approval handling"""
    print(f"\n{'='*60}")
    print(f"User > {query}\n")

    session_id = f"order_{uuid.uuid4().hex[:8]}"

    await session_service.create_session(
        app_name = "shipping_coordinator",
        user_id = "test_user",
        session_id = session_id,
    )

    query_content = types.Content(role = 'user',
                                  parts = [types.Part(text = query)])
    events = []

    #### Step 1 : Send initial request to the AGENT if num_containers > 5 ,
    #### Agent returns the special adk_request confirmation
    async for event in shipping_runner.run_async(
        user_id = "test_user",
        session_id = session_id,
        new_message = query_content,
    ):
        events.append(event)

    #### Step 2: Loop through all the events generated and check if 
    #### adk_request_confirmation is present
    approval_info = check_for_approval(events)

    ##### Step 3: if the event is present, its a large order - HUMAN Approval workflow
    if approval_info:
        print("Pause for approval...")
        print(f"Human Decision : {'APPROVE' if auto_approve else 'REJECT'} \n")

        ### PATH A: Resume the agent by calling run_async() again with the approval decision
        async for event in shipping_runner.run_async(
            user_id = "test_user",
            session_id = session_id,
            new_message = create_approval_response(approval_info, auto_approve),
            invocation_id = approval_info["invocation_id"], #CRITICAL because the same invocation id tells ADK to resume
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        print(f"Agent: {part.text}")
    else:
        #### PATH B : if adk_request_confirmation is not present, no approval needed - order completed immediately
        print_agent_response(events)
```
#### **Code breakdown**
**Step 1: Send initial request to the Agent**
- Call `run_async()` to start agent execution
- Collect all events in a list for inspection

**Step 2: Detect Pause**
- Call `check_for_approval(events)` to look for the special event: `adk_request_confirmation`
- Returns approval info (with `invocation_id`) if the special event is present; `None` if completed

**Step 3: Resume execution**
PATH A:
- If the approval info is present, at this point the Agent _pauses_ for human input.
- Once the Human input is available, call the agent again using `run_async()` and pass in the Human input.
- **Critical:** Same `invocation_id` (tells ADK to RESUME, not restart)
- Display agent's final response after resuming

PATH B:
- If the approval info is not present, then approval is not needed and the agent completes execution.

```python
async def main():
    """Main async function to run shipping workflow demos"""
    # Demo 1: Small order - no approval needed
    await run_shipping_workflow("Ship 3 containers to Singapore")

    # Demo 2: Workflow simulates human decision: APPROVE ✅
    await run_shipping_workflow("Ship 10 containers to Rotterdam", auto_approve=True)

    # Demo 3: Workflow simulates human decision: REJECT ❌
    await run_shipping_workflow("Ship 8 containers to Los Angeles", auto_approve=False)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"An error occurred: {e}")
```

Here's what happens step-by-step when you run `run_shipping_workflow("Ship 10 containers to Rotterdam", auto_approve=True)`:

```python
TIME 1: User sends "Ship 10 containers to Rotterdam"
        ↓
TIME 2: Workflow calls shipping_runner.run_async(...)
        ADK assigns a unique invocation_id = "abc123"
        ↓
TIME 3: Agent receives user message, decides to use place_shipping_order tool
        ↓
TIME 4: ADK calls place_shipping_order(10, "Rotterdam", tool_context)
        ↓
TIME 5: Tool checks: num_containers (10) > 5
        Tool calls tool_context.request_confirmation(...)
        ↓
TIME 6: Tool returns {'status': 'pending', ...}
        ↓
TIME 7: ADK creates adk_request_confirmation event with invocation_id="abc123"
        ↓
TIME 8: Workflow detects the event via check_for_approval()
        Saves approval_id and invocation_id="abc123"
        ↓
TIME 9: Workflow gets human decision → True (approve)
        ↓
TIME 10: Workflow calls shipping_runner.run_async(..., invocation_id="abc123")
         Passes approval decision as FunctionResponse
         ↓
TIME 11: ADK sees invocation_id="abc123" - knows to RESUME (instead of starting new)
         Loads saved state from TIME 7
         ↓
TIME 12: ADK calls place_shipping_order again with same parameters
         But now tool_context.tool_confirmation.confirmed = True
         ↓
TIME 13: Tool returns {'status': 'approved', 'order_id': 'ORD-10-HUMAN', ...}
         ↓
TIME 14: Agent receives result and responds to user
```
**Key point:** The `invocation_id` is how ADK knows to resume the paused execution instead of starting a new one.