---
date: 2026-09-28
type: project-note
project: resolveflow
status: active
tags:
  - domain/ai-eng
  - type/project-note
  - resolveflow
  - topic/agents
description: "Graph state, reducers, routes, conditional edges, interrupt/resume, and LangGraph lessons to reuse."
hubs:
  - "[[00 ResolveFlow Index]]"
---

# 06 LangGraph Orchestration

> Part of [[00 ResolveFlow Index]]. Previous: [[05 RefundService]] · Next: [[07 Intent Routing and LLM Classifier]]

## Build notes

Orchestration of Langgraph
```
state.py     What data moves through the workflow?
nodes.py     What work happens?
routes.py    Where does execution go next?
builder.py   How is the complete graph assembled?
```

Reducers
`errors` uses list addition
```python
errors: Annotated[list[str], operator.add]
```

```python
{
	"errors": [
		"There is soemthing wrong at"
	]
}
```

A workflow can accumulate many messages, evidence records and events, but it has one current proposal, decision and result.

The routes 
```
After validation
├── errors → END
└── valid → load_transactions

After detection
├── no duplicate → END
└── duplicate → create_evidence

After approval
├── approved → execute_action
└── rejected → END
```

```python
def route_after_validation(state:ResolveFlowState):
    if state.get("errors"):
        return "end"
        
    return "load_transactions"

def route_after_detection(state:ResolveFlowState):
    if state.get("duplicate_finding") is None:
        return "end"
        
    return "create_evidence"

def route_after_approval(state:ResolveFlowState):
    decision = state.get("approval_decision")

    if (decision is not None and decision.status == ApprovalStatus.APPROVED):
        return "execute_action"
        
    return "end"
```

Conditional edges
```python
graph.add_conditional_edges(
        "request_approval",
        route_after_approval,
        {
            "execute_action": "execute_action",
            "end" : END
      
```

Workflow Diagram
```
flowchart TD
    A[Initial ticket state] --> B[Validate request]

    B -->|missing fields| Z[END with errors]
    B -->|valid| C[Load tenant and customer transactions]

    C --> D[Detect duplicate within five minutes]

    D -->|not found| N[Add no-duplicate message]
    N --> Z

    D -->|found| E[Create evidence]
    E --> F[Create pending refund proposal]
    F --> G[Interrupt for human approval]

    G -->|rejected| Z
    G -->|approved| H[RefundService checks authorization]
    H --> I[Billing gateway checks provider rules]
    I --> J[Receipt and refunded transaction]
    J --> K[Successful ActionResult]
    K --> Z
```

## LangGraph — lessons to reuse

### Nodes return partial updates, reducers decide how they merge

A node returns only the keys it changes. The state's annotations decide what happens next:

| Field | Annotation | Returning `{"x": v}` does |
|---|---|---|
| `messages` | `add_messages` | Appends (and replaces by message ID) |
| `errors`, `evidence`, `trajectory` | `operator.add` | Appends the list |
| `step_count` | `operator.add` on `int` | Adds, so returning `1` is a counter |
| `proposed_action`, `action_result` | none | Overwrites |

> [!tip] Rule
> Accumulating things (messages, evidence, errors, events) get a reducer. Things that have "one current value" (proposal, decision, result) do not.

### Missing keys are normal

`TypedDict` does not create defaults. A key a node never wrote simply does not exist:

```python
assert "action_result" not in final_state   # rejected path
state.get("proposed_action")                 # not state["proposed_action"]
```

Use `.get()` for anything a path might skip. This is the same lesson as `__interrupt__` in the API.

### `trajectory` is a test tool

Every node appends its name. Asserting the exact list proves the **path**, not just the result:

```python
assert final_state["trajectory"] == ["validate_request", "classify_intent", ..., "request_approval"]
```

A test that only checks the final answer can pass while the graph took the wrong route.

### Injecting dependencies into nodes

A node is called with `state` only. Extra dependencies are bound in the builder:

```python
graph.add_node("classify_intent", partial(classify_intent, classifier=classifier))
graph.add_node("execute_action", lambda state: execute_action(state, refund_service))
```

Both work. `partial` is slightly better: it keeps the function's name and cannot capture the wrong variable later (lambdas in a loop bind late). The real win is `build_refund_graph(gateway, classifier)`: tests pass a fake, production passes the real one, and no node imports a global.

> [!note] Fakes do not need inheritance
> `FakeIntentClassifier` does not subclass `IntentClassifier`. It only has a `classify_intent(message)` method that returns a `TicketIntent`. Python only cares that the method exists (duck typing).

### Routes are pure functions that return labels

```python
def route_after_intent(state) -> str:
    ...
    return "human_handoff"   # the last line is the safe default
```

- A route reads state and returns a label. The `path_map` in `add_conditional_edges` maps labels to nodes, so labels like `"end"` stay stable even if node names change.
- Pure functions are unit-testable without building a graph.
- **The fall-through default goes to the safest path.** Anything unknown, missing, or below the threshold ends in human handoff.
- Policy numbers (confidence `0.75`, the five-minute window) live in the orchestration layer, not in the general-purpose service.

### `interrupt()`: how pausing really works

```python
answer = interrupt({"question": "...", "action": proposed_action.model_dump(mode="json")})
```

- Requires a **checkpointer** and a **`thread_id`**. Without them there is nothing to resume.
- The dict passed to `interrupt()` is what the reviewer sees. Make it JSON-safe.
- The value in `Command(resume=...)` becomes the **return value** of `interrupt()`.

> [!warning] On resume, the node runs again from its first line
> LangGraph does not continue from the middle of the function. It re-executes `request_approval` from the top, and this time `interrupt()` returns the resume value instead of pausing. So **never put a side effect before `interrupt()`** (no refund, no email, no DB write). Everything above it will run twice. Here it only reads state, so it is safe.

### `InMemorySaver` is for learning

Checkpoints live in process memory. A server restart loses every paused ticket, and two server processes do not share them. Production needs a persistent saver (for example Postgres). Keep this in mind before calling the approval flow "done."
