To handle generating large amounts of data (like 50+ high-quality queries) without the LLM getting "tired" or repetitive, we use a **Map-Reduce** pattern. In LangGraph, this is done by sending a list of tasks to a node and having it process them in parallel.

### 1. The Strategy
Instead of asking for 50 queries in one shot, we break the request into **5 batches of 10**. This keeps the "attention" of the LLM sharp and ensures diversity.

### 2. Update your State
You need a field in your `TypedDict` that can handle a list of results from parallel workers. We use the `operator.add` reducer for this.
```python
search_queries: Annotated[List[SearchQuery], operator.add] batch_tasks: List[dict] # To store the split tasks
```

### 3. The "Map" Node: `prepare_batches`
This node calculates how many batches are needed based on the `number_required`.
```python
def prepare_batches(state: GraphState):
    total = state["parsed_query"].number_required
    
    batch_size = 10
    num_batches = (total // batch_size) + (1 if total % batch_size > 0 else 0)
    
    # Create a list of instructions for the parallel workers
    tasks = []
    
    for i in range(num_batches):
        tasks.append(
	        {
	            "batch_id": i,
	            "count": batch_size if i < num_batches - 1 else total % batch_size
	        }
		)
    return {"batch_tasks": tasks}
```

### 4. The "Worker" Node: `refine_query`
This node stays mostly the same, but it now only generates a small batch. Because LangGraph can "map" over the `batch_tasks`, this node will run multiple times in parallel.

### 5. Defining the Graph (The Magic Part)
In your `StateGraph` definition, you use `Send` to trigger the parallel execution.
```python
from langgraph.constants import Send
from langgraph.graph import StateGraph, START, END

def map_refine_queries(state: GraphState):
    # This logic tells LangGraph: "For every task in batch_tasks, 
    # run the 'refine_query' node in parallel."
    return [Send("refine_query", {"task": t, "parsed_query": state["parsed_query"]}) 
            for t in state["batch_tasks"]]

workflow = StateGraph(GraphState)

workflow.add_node("extract_topics", extract_topics_logic)
workflow.add_node("prepare_batches", prepare_batches)
workflow.add_node("refine_query", refine_query_logic) # Your improved prompt goes here
workflow.add_node("generate_synthetic_data", generate_logic)

workflow.add_edge(START, "extract_topics")
workflow.add_edge("extract_topics", "prepare_batches")

# The Map-Reduce Trigger
workflow.add_conditional_edges("prepare_batches", map_refine_queries)

# Once all 'refine_query' workers finish, they "Reduce" (add) 
# their results into search_queries and move to the next step.
workflow.add_edge("refine_query", "generate_synthetic_data")
workflow.add_edge("generate_synthetic_data", END)
```

- **Speed:** If you're generating 50 queries, 5 parallel calls of 10 queries will finish in the time it takes to do one call.
    
- **Quality:** The LLM is much better at maintaining a unique "creative spark" over 10 items than 50.
    
- **Error Tolerance:** If one batch fails, you can retry just that batch rather than restarting the entire 50-item generation.
---
LangGraph Dynamic Fan-Out Pattern: 
it returns a list of `Send` objects to spawn multiple parallerl executions of the same **`web_search_worker` node, one per search query.**

>[!tip]
>**Map-Reduce** pattern where one node generates multiple parallel sub-tasks, runs them concurrently, then merges results back into the parent graph's state.

```
START → parse_query → produce_search_query → [orchestrate_searches]
                                                      ↓
                                        Spawns N parallel "web_search_worker"
                                                      ↓
                                    All complete → END (merges results)
```

1. `produce_search_query` runs and populates `state["search_queries"]` with `["query1", "query2", ...]`
2. **`orchestrate_searches`** (conditional edge) receives this state and **returns `[Send(...), Send(...)]`**

##### Send Objects Explained
```python
return [Send("web_search_worker", {"search_query": sq}) 
        for sq in state["search_queries"]]
```

- **`Send(node_name, input_dict)`**: Tells LangGraph "spawn a new execution of this node with this input"
- Each `Send` gets **isolated `WorkerState`** (sub-state) containing only `{"search_query": "query1"}`
- **Merging**: Worker outputs (`Command(update={"web_results": [...]})`) accumulate into parent `AgentState`

>[!warning]
>In the worker make a separate state away from AgentState and return the result in the Command Object to specify the state updates

```python
class WorkerState(TypedDict):
    search_query: SearchQuery
```

1. Make the conditional edge func
- **`Send(node_name, input_dict)`**: Tells LangGraph "spawn a new execution of this node with this input"
```python
def orchestrate_searches(state: AgentState):
    """Orchestrator logic: Returns a list of Send commands to parallel web_search_worker nodes."""
    return [Send("web_search_worker", {"search_query": sq}) 
            for sq in state["search_queries"]]
```

2. The worker itself
Check that the state itself is not the same as AgentState
```python
def web_search_worker(state: WorkerState):
    """Worker node: executes a single search query."""
    search_query = state["search_query"]

    tool = TavilySearchResults(
        max_results=10,
        topic="general"
    )

    results = tool.invoke(
        {
            "query": search_query.query
        }
    )

    return Command(
        update = {
            "web_results": [
                {
                    "query": search_query.query, 
                    "results": results
                }
            ]
        }
    )
```

```python
produce_search_query ─┐
                      ├─► web_search_worker (query1)
                      ├─► web_search_worker (query2)
                      ├─► web_search_worker (queryN)
orchestrate_searches ─┘
```