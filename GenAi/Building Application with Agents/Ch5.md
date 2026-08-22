
# Chapter 5: Orchestration

Now that your agent has a set of tools that can be used, it's time to orchestrate them to solve real tasks. Orchestration involves more than just deciding which tools to call and when—it also requires constructing the right context for each model invocation to ensure effective, grounded actions. While simple tasks may only need a single tool and minimal context, more complex workflows demand careful planning, memory retrieval, and dynamic context assembly to perform each step accurately.

In this chapter, we'll cover orchestration strategies, context engineering, tool selection, execution, and planning topologies to build agents capable of handling realistic, multistep tasks efficiently and reliably. As we can see in **Figure 5-1**, orchestration is how the system utilizes the resources at its disposal to address the user query effectively.

> **Figure 5-1.** Orchestration as the core logic that handles user queries and coordinates calls to the foundation models, external and local tools, and to various databases to retrieve additional information.

---

## Agent Types

Before diving into specific orchestration strategies, it's important to understand the different types of agents you can build. Each agent type embodies a distinct approach to reasoning, planning, and action, shaping how tasks are decomposed and executed. Some agents respond instantly with preprogrammed mappings, while others iteratively reason and reflect to handle complex, open-ended goals.

The choice of agent type directly influences your system's performance, cost, and capabilities. In this section, we will explore the spectrum: from **reflex agents** that provide lightning-fast responses, to **deep research agents** that tackle multistage investigations with adaptive plans and synthesis.

### Reflex Agents

Reflex agents implement a direct mapping from input to action without any internal reasoning trace. Simple reflex agents follow "if-condition, then-action" rules, calling the appropriate tool immediately upon detecting predefined triggers. Because they bypass intermediate thought steps, reflex agents deliver responses with minimal latency and predictable performance, making them well suited for use cases like keyword-based routing, single-step data lookups, or basic automations (e.g., "If X, call tool Y"). However, their limited expressiveness means they cannot handle tasks requiring multistep reasoning or context beyond the immediate input.

### ReAct Agents

ReAct agents interleave **Reasoning** and **Action** in an iterative loop: the model generates a thought, selects and invokes a tool, observes the result, and repeats as needed. This pattern enables the agent to break complex tasks into manageable steps, updating its plan based on intermediate observations:

- `ZERO_SHOT_REACT_DESCRIPTION` (LangChain) presents tools and instructions in a single prompt, relying on the LLM's innate reasoning to select and call tools without example traces.
- `CHAT_ZERO_SHOT_REACT_DESCRIPTION` extends this by incorporating conversational history, enabling the agent to use past exchanges when deciding on its next action.

ReAct agents excel in exploratory scenarios—dynamic data analysis, multisource aggregation, or troubleshooting—where the ability to adapt midstream outweighs the additional latency and computational overhead. Their looped structure also provides transparency ("chain of thought") that aids debugging and auditability, though it can increase API costs and response times.

### Planner-Executor Agents

Planner-executor agents split a task into two distinct phases: **planning**, where the model generates a multistep plan; and **execution**, where each planned step is carried out via tool calls. This clear separation lets the planner focus on long-horizon reasoning while executors invoke only the necessary tools, reducing redundant LLM calls. Because the plan is explicit, debugging and monitoring become straightforward—you can inspect the generated plan, track which step failed, and replan if needed.

**Advantages:**

- **Clear decomposition** – Complex tasks break down into manageable subtasks.
- **Debuggability** – Explicit plans reveal where and why errors occur.
- **Cost efficiency** – Smaller models or fewer LLM calls handle execution, reserving large models for planning.

### Query-Decomposition Agents

Query-decomposition agents tackle a complex question by iteratively breaking it into subquestions, invoking search or other tools for each, and then synthesizing a final answer. This pattern—often called "self-ask with search"—prompts the model:

> “What follow-up question do I need?” → call search → “What’s the next question?” → … → “What’s the final answer?”

**Example (SELF_ASK_WITH_SEARCH):**

- Ask: "Who lived longer, X or Y?"
- Self-ask: "What's X's lifespan?" → search tool
- Self-ask: "What's Y's lifespan?" → search tool
- Synthesize: "X lived 85 years, Y lived 90 years, so Y lived longer"

This approach excels when external knowledge retrieval is needed, ensuring each fact is grounded in tool output before composing the final response.

### Reflection Agents

Reflection and metareasoning agents extend the ReAct paradigm by not only interleaving thought and action but also reviewing past steps to identify and correct mistakes before proceeding. In this approach—exemplified by the recently proposed **RefAct** framework—the agent continuously grounds its reasoning in goal-state reflections, measuring its current state against the intended outcome and adjusting its plan when misalignments arise.

This pattern shines in high-stakes workflows where early errors can cascade into costly failures—such as financial transaction orchestration, medical diagnosis support, or critical incident response. The added metareasoning overhead does incur extra latency and compute, but for tasks where correctness and reliability outweigh speed, reflection agents offer a powerful guardrail against error propagation.

### Deep Research Agents

Deep research agents specialize in tackling open-ended, highly complex investigations that require extensive external knowledge gathering, hypothesis testing, and synthesis—think literature reviews, scientific discovery, or strategic market analysis. They combine multiple patterns: a planner-executor phase to chart research workflows; query-decomposition to break down big questions into targeted searches; and ReAct loops to iteratively refine hypotheses based on new findings.

**Typical cycle:**

1. Plan the overall research agenda (e.g., identify key subtopics or data sources).
2. Decompose each subtopic into concrete queries (via SELF_ASK or similar).
3. Invoke tools—from academic search APIs to domain-specific databases—and reflect on the relevance and reliability of each result.
4. Synthesize the insights into an evolving report or set of recommendations, using LLM-driven summarization and critique at each step.

**Strengths & Weaknesses:**

| Strengths | Weaknesses |
|-----------|-------------|
| Handles high-complexity, multistage investigations | High cost (extensive model use, multiple API calls) |
| Adaptive research direction as new evidence emerges | Latency (each layer adds delay) |
| Transparent explicit plans and decomposition steps | Fragility – relies on quality/availability of external data sources |

**Best use cases:** long-form, expert-level tasks – academic literature surveys, technical due diligence, competitive intelligence – where depth and rigor trump speed.

---

### Table 5-1. Common Agent Archetypes

| Agent Type        | Strength                                         | Weakness                               | Best Use Case                              |
|-------------------|--------------------------------------------------|----------------------------------------|---------------------------------------------|
| Reflex            | Millisecond responses                            | No multistep reasoning                 | Keyword routing, simple lookups             |
| ReAct             | Flexible, on-the-fly adaptation                  | Higher latency and cost                | Exploratory workflows, troubleshooting      |
| Plan-execute      | Clear task breakdown                             | Planning overhead                      | Complex, multistep processes                |
| Query-decomposition | Grounded retrieval accuracy                    | Multiple tool calls                    | Research, fact-based Q&A                    |
| Reflection        | Early error detection                            | Added compute and latency              | High-stakes, safety-critical tasks          |
| Deep research     | Management of multistage adaptive investigations | High compute costs, very high latency  | Long-form literature reviews                |

> This landscape is evolving at breakneck speed. Consider this list a starting point rather than a definitive taxonomy.

---

## Tool Selection

Tool selection is the foundation for more advanced planning. Different approaches offer unique advantages and considerations.

### Table 5-2. Tool Selection Strategies

| Technique                | Pros                                                                 | Cons                                           |
|--------------------------|----------------------------------------------------------------------|------------------------------------------------|
| Standard tool selection  | Simple to implement                                                  | Scales poorly to high numbers of tools        |
| Semantic tool selection  | Very scalable to large numbers of tools; typically low latency       | Often worse selection accuracy due to semantic collisions |
| Hierarchical tool selection | Very scalable to large numbers of tools                           | Slower because it requires multiple sequential LLM calls |

### Standard Tool Selection

The simplest approach: the tool definition and description are provided to an LLM, and the model selects the most appropriate tool. Output is compared with the toolset, and the closest one is chosen.

**Tips for effective tool descriptions:**
- Give every tool a concise, descriptive name (e.g., `calculate_sum` instead of `process_numbers`).
- Follow with a one-sentence summary highlighting its unique purpose.
- Include an example invocation in the description.
- Enforce input constraints by specifying types and ranges.

**Example tool definitions:**

```python
from langchain_core.tools import tool
import requests

@tool
def query_wolfram_alpha(expression: str) -> str:
    """
    Query Wolfram Alpha to compute expressions or retrieve information.
    Args:
        expression (str): The mathematical expression or query to evaluate.
    Returns:
        str: The result of the computation or the retrieved information.
    """
    api_url = f'https://api.wolframalpha.com/v1/result?i={requests.utils.quote(expression)}&appid=YOUR_WOLFRAM_ALPHA_APP_ID'
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.text
        else:
            raise ValueError(f"Wolfram Alpha API Error: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Failed to query Wolfram Alpha: {e}")

@tool
def trigger_zapier_webhook(zap_id: str, payload: dict) -> str:
    """
    Trigger a Zapier webhook to execute a predefined Zap.
    Args:
        zap_id (str): The unique identifier for the Zap to be triggered.
        payload (dict): The data to send to the Zapier webhook.
    Returns:
        str: Confirmation message upon successful triggering of the Zap.
    Raises:
        ValueError: If the API request fails or returns an error.
    """
    zapier_webhook_url = f"https://hooks.zapier.com/hooks/catch/{zap_id}/"
    try:
        response = requests.post(zapier_webhook_url, json=payload)
        if response.status_code == 200:
            return f"Zapier webhook '{zap_id}' successfully triggered."
        else:
            raise ValueError(f"Zapier API Error: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Failed to trigger Zapier webhook '{zap_id}': {e}")

@tool
def send_slack_message(channel: str, message: str) -> str:
    """
    Send a message to a specified Slack channel.
    Args:
        channel (str): The Slack channel ID or name where the message will be sent.
        message (str): The content of the message to send.
    Returns:
        str: Confirmation message upon successful sending of the Slack message.
    Raises:
        ValueError: If the API request fails or returns an error.
    """
    api_url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": "Bearer YOUR_SLACK_BOT_TOKEN",
        "Content-Type": "application/json"
    }
    payload = {"channel": channel, "text": message}
    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response_data = response.json()
        if response.status_code == 200 and response_data.get("ok"):
            return f"Message successfully sent to Slack channel {channel}"
        else:
            error_msg = response_data.get("error", "Unknown error")
            raise ValueError(f"Slack API Error: {error_msg}")
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Failed to send message to Slack channel {channel}: {e}")
```

**Binding tools and invoking:**

```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# Initialize LLM with GPT-4o and bind tools
llm = ChatOpenAI(model_name="gpt-4o")
llm_with_tools = llm.bind_tools([get_stock_price, send_slack_message, query_wolfram_alpha])

messages = [HumanMessage("What is the stock price of Apple")]
ai_msg = llm_with_tools.invoke(messages)
messages.append(ai_msg)

for tool_call in ai_msg.tool_calls:
    tool_msg = get_stock_price.invoke(tool_call)
    messages.append(tool_msg)

final_response = llm_with_tools.invoke(messages)
print(final_response.content)
```

### Semantic Tool Selection

Semantic tool selection uses semantic representations to index all available tools and semantic search to retrieve the most relevant ones. Ahead of time, each tool definition and description is embedded using an encoder-only model (e.g., OpenAI's Ada, Amazon Titan, Cohere Embed, ModernBERT). The tools are indexed in a lightweight vector database.

> **Figure 5-2.** Semantic tool embedding for retrieval-based selection. Each tool or skill is encoded into a dense vector representation using an embedding model. These vectors are then stored for efficient semantic search.

> **Figure 5-3.** Semantic tool retrieval and invocation workflow. At runtime, the user query is embedded and used to retrieve the top relevant tools from the vector database. The foundation model then selects the appropriate tool and determines its parameters, invokes the tool, and integrates the tool's output to generate the final user response.

**Implementation example:**

```python
import numpy as np
from langchain_openai import OpenAIEmbeddings
import faiss

# Initialize OpenAI embeddings
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

# Tool descriptions
tool_descriptions = {
    "query_wolfram_alpha": "Use Wolfram Alpha to compute mathematical expressions or retrieve information.",
    "trigger_zapier_webhook": "Trigger a Zapier webhook to execute predefined automated workflows.",
    "send_slack_message": "Send messages to specific Slack channels to communicate with team members."
}

# Create embeddings for each tool description
tool_embeddings = []
tool_names = []

for tool_name, description in tool_descriptions.items():
    embedding = embeddings.embed_text(description)
    tool_embeddings.append(embedding)
    tool_names.append(tool_name)

# Initialize FAISS vector store
dimension = len(tool_embeddings[0])
index = faiss.IndexFlatL2(dimension)

# Normalize embeddings for cosine similarity
faiss.normalize_L2(np.array(tool_embeddings).astype('float32'))

# Convert to FAISS-compatible format
tool_embeddings_np = np.array(tool_embeddings).astype('float32')
index.add(tool_embeddings_np)

# Map index to tool functions
index_to_tool = {
    0: query_wolfram_alpha,
    1: trigger_zapier_webhook,
    2: send_slack_message
}

def select_tool(query: str, top_k: int = 1) -> list:
    """
    Select the most relevant tool(s) based on the user's query using vector-based retrieval.
    """
    query_embedding = embeddings.embed_text(query).astype('float32')
    faiss.normalize_L2(query_embedding.reshape(1, -1))
    D, I = index.search(query_embedding.reshape(1, -1), top_k)
    selected_tools = [index_to_tool[idx] for idx in I[0] if idx in index_to_tool]
    return selected_tools

def determine_parameters(query: str, tool_name: str) -> dict:
    """
    Use the LLM to analyze the query and determine the parameters for the tool to be invoked.
    """
    messages = [HumanMessage(content=f'Based on the user\'s query: {query}, what parameters should be used for the tool {tool_name}?')]
    response = llm(messages)
    parameters = {}
    if tool_name == "query_wolfram_alpha":
        parameters["expression"] = response.get('expression', query)  # extract mathematical expression
    elif tool_name == "trigger_zapier_webhook":
        parameters["zap_id"] = response.get('zap_id', "123456")
        parameters["payload"] = response.get('payload', {"data": query})
    elif tool_name == "send_slack_message":
        parameters["channel"] = response.get('channel', "#general")
        parameters["message"] = response.get('message', query)
    return parameters

# Example user query
user_query = "Solve this equation: 2x + 3 = 7"
selected_tools = select_tool(user_query, top_k=1)
tool_name = selected_tools[0] if selected_tools else None

if tool_name:
    args = determine_parameters(user_query, tool_name.__name__)
    try:
        tool_result = tool_name.invoke(args)
        print(f"Tool {tool_name.__name__} Result: {tool_result}")
    except ValueError as e:
        print(f"Error invoking tool '{tool_name.__name__}': {e}")
else:
    print("No tool was selected.")
```

### Hierarchical Tool Selection

If you have a large number of tools, especially semantically similar ones, hierarchical tool selection improves accuracy at the cost of higher latency. Organize tools into groups, provide descriptions for each group, first select a group, then perform a secondary search within that group.

> **Figure 5-4.** Hierarchical tool-selection workflow. The agent first chooses the most relevant tool group for the query, and then narrows the search to select a single tool within that group.

**Implementation example:**

```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

llm = ChatOpenAI(model_name="gpt-4", temperature=0)

# Define tool groups with descriptions
tool_groups = {
    "Computation": {
        "description": "Tools related to mathematical computations and data analysis.",
        "tools": []
    },
    "Automation": {
        "description": "Tools that automate workflows and integrate different services.",
        "tools": []
    },
    "Communication": {
        "description": "Tools that facilitate communication and messaging.",
        "tools": []
    }
}

# Assign tools to groups
tool_groups["Computation"]["tools"].append(query_wolfram_alpha)
tool_groups["Automation"]["tools"].append(trigger_zapier_webhook)
tool_groups["Communication"]["tools"].append(send_slack_message)

def select_group_llm(query: str) -> str:
    prompt = f"Select the most appropriate tool group for the following query: {query}. Options are: Computation, Automation, Communication."
    response = llm([HumanMessage(content=prompt)])
    return response.content.strip()

def select_tool_llm(query: str, group_name: str) -> str:
    prompt = f"Based on the query: {query}, select the most appropriate tool from the group {group_name}."
    response = llm([HumanMessage(content=prompt)])
    return response.content.strip()

# Example usage
user_query = "Solve this equation: 2x + 3 = 7"
selected_group_name = select_group_llm(user_query)

if selected_group_name:
    print(f"Selected Tool Group: {selected_group_name}")
    selected_tool_name = select_tool_llm(user_query, selected_group_name)
    selected_tool = globals().get(selected_tool_name, None)
    
    if selected_tool:
        # Prepare arguments based on the tool
        args = {}
        if selected_tool == query_wolfram_alpha:
            args["expression"] = user_query
        elif selected_tool == trigger_zapier_webhook:
            args["zap_id"] = "123456"
            args["payload"] = {"message": user_query}
        elif selected_tool == send_slack_message:
            args["channel"] = "#general"
            args["message"] = user_query
        
        try:
            tool_result = selected_tool.invoke(args)
            print(f"Tool '{selected_tool.__name__}' Result: {tool_result}")
        except ValueError as e:
            print(f"Error: {e}")
    else:
        print("No relevant tool found within the selected group.")
else:
    print("No relevant tool group found for your query.")
```

---

## Tool Execution

**Parametrization** is the process of defining and setting parameters that guide tool execution. Parameters are defined by the tool definition. The current agent state (progress so far) is included as additional context in the prompt window, and the foundation model fills the parameters with appropriate data types. Additional context (e.g., current time, user location) can be injected as needed.

Once parameters are set, the **tool execution phase** begins. Some tools execute locally, others remotely via API. Timeout and retry logic must be adjusted to the latency and performance requirements of the use case.

---

## Tool Topologies

Today, most chatbot systems rely on single tool execution without planning. For complex tasks, we enable agents to flexibly arrange multiple tools in the correct order.

### Single Tool Execution

Tasks requiring exactly one tool. Planning consists of choosing the most appropriate tool, parameterizing it, executing it, and composing the final response.

> **Figure 5-5.** Single tool execution workflow: user query → model → tool selection → tool output → final response.

> **Figure 5-6.** Example of single tool execution for weather retrieval in New York City.

### Parallel Tool Execution

When multiple actions are needed on the input (e.g., looking up a patient record from multiple data sources). Common approach: retrieve a maximum number of tools (say five) using semantic tool selection, then ask the LLM to filter to the necessary ones. Tools are independently parameterized and executed in parallel, then results are passed to the LLM for final response.

> **Figure 5-7.** Parallel tool execution pattern: user asks how to handle a customer ticket → multiple tools run in parallel (customer details, order history, service logs, similar tickets, support policies) → integrate outputs → generate final response.

### Chains

Chains are sequences of actions executed one after another, each depending on the previous one. LangChain offers the **LangChain Expression Language (LCEL)** for declarative chain building.

```python
from langchain_core.runnables import RunnableLambda
from langchain.chat_models import ChatOpenAI
from langchain_core.prompts import PromptTemplate

# Wrap a function or model call as a Runnable
llm = RunnableLambda.from_callable(ChatOpenAI(model_name="gpt-4", temperature=0).generate)
prompt = RunnableLambda.from_callable(lambda text: PromptTemplate.from_template(text).format_prompt({"input": text}).to_messages())

# LCEL chain using pipes
chain = prompt | llm

# Invoke the chain
result = chain.invoke("what is the capital of France?")
```

> **Figure 5-8.** Agentic chain execution pattern: user prompt → model reasoning → tool invocation → environment observation → loop back.

It is highly recommended to set a maximum length to tool chains, as errors can compound.

### Graphs

For scenarios with multiple decision points, a **graph topology** models complex, non-hierarchical flows. Nodes represent discrete tool invocations or logical steps. Edges (including `add_conditional_edges`) declare transition conditions. Outputs from multiple branches can be consolidated into a single downstream node.

**LangGraph example:**

```python
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(model_name="gpt-4", temperature=0)

# 1. Node definitions
def categorize_issue(state: dict) -> dict:
    prompt = f"Classify this support request as 'billing' or 'technical'.\n\nMessage: {state['user_message']}"
    generations = llm.generate([{"role": "user", "content": prompt}]).generations
    kind = generations[0][0].text.strip().lower()
    return {**state, "issue_type": kind}

def handle_invoice(state: dict) -> dict:
    # Fetch invoice details...
    return {**state, "step_result": f"Invoice details for {state['user_id']}"}

def handle_refund(state: dict) -> dict:
    return {**state, "step_result": "Refund process initiated"}

def handle_login(state: dict) -> dict:
    return {**state, "step_result": "Password reset link sent"}

def handle_performance(state: dict) -> dict:
    return {**state, "step_result": "Performance metrics analyzed"}

def summarize_response(state: dict) -> dict:
    details = state.get("step_result", "")
    summary = llm.generate([{"role": "user", "content": f"Write a concise customer reply based on: {details}"}]).generations[0][0].text.strip()
    return {**state, "response": summary}

# 2. Build the graph
graph = StateGraph()

# Start → categorize_issue
graph.add_edge(START, categorize_issue)

# categorize_issue → billing or technical
def top_router(state):
    return "billing" if state["issue_type"] == "billing" else "technical"

graph.add_conditional_edges(
    categorize_issue,
    top_router,
    mapping={"billing": handle_invoice, "technical": handle_login}
)

# Billing sub-branches: invoice vs. refund
def billing_router(state):
    msg = state["user_message"].lower()
    return "invoice" if "invoice" in msg else "refund"

graph.add_conditional_edges(
    handle_invoice,
    billing_router,
    mapping={"invoice": handle_invoice, "refund": handle_refund}
)

# Technical sub-branches: login vs. performance
def tech_router(state):
    msg = state["user_message"].lower()
    return "login" if "login" in msg else "performance"

graph.add_conditional_edges(
    handle_login,
    tech_router,
    mapping={"login": handle_login, "performance": handle_performance}
)

# Consolidation edges
graph.add_edge(handle_refund, summarize_response)
graph.add_edge(handle_performance, summarize_response)
graph.add_edge(handle_invoice, summarize_response)
graph.add_edge(handle_login, summarize_response)
graph.add_edge(summarize_response, END)

# 3. Execute
initial_state = {
    "user_message": "Hi, I need help with my invoice and possibly a refund.",
    "user_id": "U1234"
}
result = graph.run(initial_state, max_depth=5)
print(result["response"])
```

**Guidelines:**
- Start with a chain if your task is strictly linear.
- Adopt a graph only when you must both branch and later consolidate multiple streams.
- Sketch your topology on paper first.
- Cap depth and branching factor.
- Write unit tests for each router.

---

## Context Engineering

Context engineering ensures that each step in an agent's plan has the right information and instructions to perform effectively. It involves dynamically assembling all inputs—user messages, retrieved knowledge, workflow state, and system prompts—into a structured, token-efficient context window.

**Core practices:**

1. **Prioritize relevance** – Retrieve only the most useful information.
2. **Maintain clarity** – Use structured formatting or schemas (e.g., Model Context Protocol, MCP).
3. **Use summarization** – Compress longer histories into concise representations.
4. **Dynamic assembly** – Assemble context at each inference step to reflect current objectives.

Context engineering sits at the intersection of memory, knowledge, and orchestration. A well-engineered context unlocks the full potential of even modest models.

---

## Conclusion

The success of agents relies heavily on the approach to orchestration. Best practices for designing a planning system:

1. Carefully consider latency vs. accuracy trade-offs.
2. Determine the typical number of actions required.
3. Assess how much the plan needs to change based on prior results.
4. Design representative test cases to evaluate different planning approaches.
5. Choose the simplest planning approach that meets your requirements.

Start small with well-designed scenarios and simpler orchestration, then gradually increase complexity as needed. In the next chapter, we will explore how **memory** can further enhance your agents' capabilities—enabling them to recall knowledge, maintain context across interactions, and perform tasks with greater intelligence and personalization.
```