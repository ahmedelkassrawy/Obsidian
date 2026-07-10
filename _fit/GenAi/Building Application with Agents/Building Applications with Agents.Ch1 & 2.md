# Chapter 2: Designing Agent Systems

> [!abstract] Quick Start
> Most practitioners don’t begin with a grand design document when building agent systems. They start with a messy problem, a foundation model API key, and a rough idea of what might help. This chapter is your quick start to get you up and running. We’ll cover each of the following topics in more depth through the rest of the book – many will get their own chapter – but this chapter will give you an overview of how to design an agentic system, all grounded in a specific example: managing customer support for an e‑commerce platform.

---

## 1. Our First Agent System

Every day, your customer‑support team fields dozens or hundreds of emails asking to refund a broken mug, cancel an unshipped order, or change a delivery address.  
For each message, a human agent reads free‑form text, looks up the order in your backend, calls the appropriate API, and types a confirmation email. This repetitive two‑minute process is ripe for automation – but only if we **carve off the right slice**.

When we realize that humans type keys and click buttons, often following rules and guidelines, we see that many of these same patterns can be performed by well‑designed systems that rely on foundation models. We want our agent to:

1. Take a raw customer message **plus** the order record.
2. Decide which tool to call (`issue_refund`, `cancel_order`, or `update_address_for_order`).
3. Invoke that tool with the correct parameters.
4. Send a brief confirmation message.

That two‑step workflow is **narrow enough to build quickly, valuable enough to free up human time, and rich enough to showcase intelligent behavior**.

### 1.1 A Minimal “Cancel Order” Agent (Code Example)

```python
from langchain.tools import tool
from langchain_openai.chat_models import ChatOpenAI

# 1) Define a single business tool
@tool
def cancel_order(order_id: str) -> str:
    """Cancel an order that hasn't shipped."""
    # (Here you'd call your real backend API)
    return f"Order {order_id} has been cancelled."

# 2) The agent "brain": invoke LLM, run tool, then invoke LLM again
def call_model(state):
    msgs = state["messages"]
    order = state.get("order", {"order_id": "UNKNOWN"})
    
    prompt = (
        f"You are an ecommerce support agent. ORDER ID: {order['order_id']}. "
        "If the customer asks to cancel, call cancel_order(order_id) and then send a simple confirmation. "
        "Otherwise, just respond normally."
    )
    full = [SystemMessage(content=prompt)] + msgs

    # 1st LLM pass: decides whether to call our tool
    first = ChatOpenAI(model="gpt-5", temperature=0).invoke(full)
    out = [first]

    if getattr(first, "tool_calls", None):
        # run the cancel_order tool
        tc = first.tool_calls[0]
        result = cancel_order(tc["args"])
        out.append(ToolMessage(content=result, tool_call_id=tc["id"]))

    # 2nd LLM pass: generate the final confirmation text
    second = ChatOpenAI(model="gpt-5", temperature=0).invoke(full + out)
    out.append(second)

    return {"messages": out}

# 3) Wire it all up in a StateGraph
def construct_graph():
    g = StateGraph({"order": None, "messages": []})
    g.add_node("assistant", call_model)
    g.set_entry_point("assistant")
    return g.compile()

graph = construct_graph()

if __name__ == "__main__":
    example_order = {"order_id": "A12345"}
    convo = [HumanMessage(content="Please cancel my order A12345.")]
    result = graph.invoke({"order": example_order, "messages": convo})
    for msg in result["messages"]:
        print(f"{msg.type}: {msg.content}")
```

### 1.2 Why Scope Matters
Scoping is a balancing act:

- **Too narrow** – only cancellations – you miss other high‑volume requests (refunds, address changes).
- **Too broad** – automate every support inquiry – you drown in edge cases like billing disputes, product recommendations, and technical troubleshooting.
- **Too vague** – “improve customer satisfaction” – you’ll never know when you’ve succeeded.

By focusing on a **clear, bounded workflow** (cancelling orders), we ensure:
- Concrete inputs (customer message + order record)
- Structured outputs (tool calls + confirmations)
- A tight feedback loop

**Example:** An email that says “Please cancel my order #B73973 because I found a cheaper option elsewhere.”  
The agent should call `cancel_order(order_id="B73973")` and send a simple confirmation.

### 1.3 Evaluating the Agent (Minimal Test)

In production, you need to know **how well** it performs. For our cancel‑order agent, we care:
- Did it call the correct tool?
- Did it pass the right parameters?
- Did it send a clear, correct confirmation?

A minimal evaluation snippet:

```python
example_order = {"order_id": "B73973"}
convo = [HumanMessage(content="Please cancel order #B73973. I found a cheaper option elsewhere.")]

result = graph.invoke({"order": example_order, "messages": convo})

assert any("cancel_order" in str(m.content) for m in result["messages"]), \
    "Cancel order tool not called"
assert any("cancelled" in m.content.lower() for m in result["messages"]), \
    "Confirmation message missing"

print("Agent passed minimal evaluation.")
```

> [!tip] Real Evaluation Goes Deeper
> You can measure tool precision, parameter accuracy, and overall task success rates across hundreds of examples to catch edge cases before deploying. (See Chapter 9 for a full evaluation framework.)  
> Remember: **an untested agent is an untrusted agent.**

---

## 2. Core Components of Agent Systems

Designing an effective agent‑based system requires a deep understanding of the core components that enable agents to perform tasks successfully. They must work together to ensure the agent can operate in dynamic and complex environments.

**Key components:**
- Foundation Model
- Tools
- Memory
- Orchestration
- (Planning)

---

## 3. Model Selection

### 3.4 Cost and Latency in Real Deployments

- Large models are expensive and may introduce delays.
- **Hybrid strategies**: a powerful model handles the hardest queries, a lightweight model handles routine tasks.
- **Dynamic model routing** – each request is evaluated and routed to the most appropriate model based on complexity or urgency, optimizing cost and quality.

> [!warning] Performance does not directly correlate with price.  
> Always benchmark on **your specific task** to find the best price‑per‑performance.

### 3.6 Summary: Model Selection Is Iterative

Model selection is not a one‑time decision. It must be revisited as agent capabilities, user needs, and infrastructure evolve.  
Trade‑offs: generality vs. specialization, performance vs. cost, simplicity vs. extensibility.

---
## 4. Tools

Tools are the **functional building blocks** of an agent – they enable specific actions and interactions.

### 4.1 Types of Tools

1. **Local tools** – internal logic without external dependencies (mathematical calculations, local DB queries, rule‑based decision making).
2. **API‑based tools** – interact with external services (weather APIs, stock prices, social media), extending the agent’s capabilities with real‑time data.
3. **Model Context Protocol (MCP) tools** – inject structured, real‑time context (user profiles, conversation history, world state) directly into the model’s prompt. Unlike traditional APIs, MCP can avoid full round‑trip execution and reduce redundant tool use.

### 4.2 Tool Modularity

Each tool should be a **self‑contained module** – easy to integrate, replace, or extend without overhauling the entire system.  
A customer‑service chatbot might start with basic tools and later add dispute resolution or advanced troubleshooting seamlessly.

---
## 5. Memory
Memory enables agents to maintain context, learn from past interactions, and improve over time.

### 5.1 Short‑Term Memory

- Stores information relevant to the **current task or conversation**.
- Maintains coherence during an interaction (e.g., remembering a user’s earlier queries in the same session).
- Often implemented via **rolling context windows** – sliding window of recent interactions, discarding outdated data.

### 5.2 Long‑Term Memory
- Stores knowledge and experiences over **extended periods**.
- Enables personalized experiences and trend detection.
- Stored in databases, knowledge graphs, or fine‑tuned models.
- A healthcare agent might retain years of patient vital signs to detect long‑term trends.

### 5.3 Memory Management

Must differentiate between relevant and irrelevant data, and retrieve quickly.  
Agents may also need to **forget** outdated or unnecessary details to avoid clutter.

> [!example] E‑commerce Recommendations
> Store user preferences and past purchases, but prioritize recent data to keep recommendations fresh as tastes change.

---
## 6. Orchestration

Orchestration turns isolated capabilities into **end‑to‑end solutions** – it composes, schedules, and supervises a series of skills so that each action flows toward a clear objective.

- Evaluates possible sequences of tool invocations, forecasts outcomes, and picks the most likely path.
- Monitors progress and environment, pausing or rerouting workflows as conditions change.
- In many scenarios, agents build plans incrementally: execute a few steps, then reassess based on fresh results (e.g., a conversational assistant confirming each subtask before planning the next).

> [!important] Without a solid orchestration layer, even the most powerful skills risk running at cross‑purposes or stalling entirely.  
> We’ll dive into patterns, architectures, and best practices in Chapter 5.

---
## 7. Design Trade‑Offs
Designing agent systems means balancing multiple competing factors.

### 7.1 Performance: Speed vs. Accuracy

- **Real‑time** environments (autonomous vehicles, trading): prioritize speed; milliseconds matter.
- **High‑precision** tasks (legal analysis, medical diagnostics): prioritize accuracy; slower is acceptable.
- **Hybrid approach**: quick approximate response first, then refine with a more accurate follow‑up (common in recommendations & diagnostics).

### 7.2 Scalability: Engineering GPU‑Intensive Systems

GPU resources are often the most expensive and limiting factor.

#### Key Strategies

1. **Dynamic GPU allocation** – assign GPUs based on real‑time demand, not statically.
2. **Elastic provisioning** – cloud or on‑prem clusters that auto‑scale.
3. **Priority queuing** – high‑priority tasks get immediate GPU access; others queue.
4. **Asynchronous task execution** – GPUs process tasks in parallel, reducing idle time.
5. **Dynamic load balancing** – distribute tasks to underutilized GPUs.

#### Scaling Architectures

- **Horizontal scaling**: add more GPU nodes to handle increasing workloads.
- **Hybrid cloud burst scaling**: use on‑prem for base load, burst to cloud GPUs during peak.
- **Off‑peak utilization**: run large compute jobs during cheaper, low‑demand windows.

### 7.3 Reliability: Ensuring Consistent Behavior

- **Fault tolerance**: detect failures (network, hardware) and recover gracefully; often via redundancy – duplicating critical components.
- **Consistency and robustness**: perform well under edge cases, stress tests, and real‑world constraints.

Achieving reliability requires:
- **Extensive testing** – unit, integration, simulations, adversarial tests.
- **Monitoring and feedback loops** – continuous observation in production to detect anomalies and adjust.

### 7.4 Cost: Balancing Performance and Expense

Costs must be justified by the value delivered.

- **Development costs**: complex models need large datasets, specialized talent, extensive testing infrastructure.
- **Operational costs**: compute (GPUs, cloud), data storage, bandwidth, ongoing maintenance.

#### Cost Optimization

- **Lean models** – use simpler models when possible; rule‑based may suffice.
- **Cloud‑based resources** – pay‑as‑you‑go reduces upfront infrastructure.
- **Open source models/tools** – minimize licensing costs.

> [!tip] Cost vs. Value
> Invest heavily in mission‑critical agents; use cheaper, simpler agents for less critical tasks.

---

## 8. Architecture Design Patterns

The architecture determines how agents are structured, interact, and scale.

### 8.1 Single‑Agent Architectures

- A single agent manages all tasks: decision making, planning, execution.
- **Best for** well‑defined, narrow tasks (e.g., simple chatbots, task‑specific automation like data entry).
- Advantages: simplicity, no coordination overhead, easy to deploy.
- Example: our “cancel order” agent.

### 8.2 Multiagent Architectures: Collaboration, Parallelism, Coordination

Multiple agents work together toward a common goal.

**Advantages:**

- **Collaboration & specialization** – each agent focuses on a specific sub‑task (data collection, processing, user interaction).
- **Parallelism** – multiple tasks processed simultaneously (e.g., logistics agents planning different routes).
- **Improved scalability** – add more agents as workload grows.
- **Redundancy & resilience** – failure of one agent doesn’t crash the system; others can take over.

**Challenges:**
- **Coordination & communication** – agents must exchange information efficiently; without proper orchestration, duplication, conflicting actions, and resource contention arise.
- **Increased complexity** – communication protocols, synchronization mechanisms, and coordination strategies add layers.
- **Higher overhead (token consumption)** – multiagent systems often consume more processing power due to constant context sharing, leading to higher costs and slower task completion if not optimized.

**Use cases:** financial trading systems, cybersecurity investigations, collaborative AI research platforms – any complex, distributed environment.

> [!summary] Architecture Decision
> - **Single‑agent** → simplicity, narrow tasks.
> - **Multiagent** → complex tasks, specialization, scalability, but higher engineering investment.

---
## 9. Best Practices

To build reliable, adaptable agent systems, follow these practices throughout the development lifecycle.

### 9.1 Iterative Design
Build incrementally, incorporating feedback at every cycle.

**Benefits:**
- **Early detection of issues** – avoid deeply embedded flaws.
- **User‑centric design** – frequent feedback keeps the agent aligned with real needs.
- **Scalable growth** – start with an MVP, gradually add features.

**Process:**
1. **Develop prototypes quickly** – focus on core functionality; don’t aim for perfection.
2. **Test and gather feedback** – from users, developers, stakeholders.
3. **Refine and repeat** – cycle until performance, usability, and scalability goals are met.

### 9.2 Evaluation Strategy
A robust evaluation ensures agents handle real‑world scenarios.
#### Functional Testing
- **Correctness** – consistent, accurate outputs.
- **Boundary testing** – edge cases, very large datasets, ambiguous instructions.
- **Task‑specific metrics** – domain accuracy (legal, medical).
#### Generalization
- Test ability to handle new, unseen tasks without retraining.

#### User Experience Evaluation
- **User satisfaction scores** (NPS, CSAT).
- **Task completion rates** – low completion indicates confusion/inefficiencies.
- **Explicit signals** – thumbs up/down, star ratings, accept/reject options.
- **Implicit signals** – analyze interaction logs for misinterpretations, delays, sentiment.

#### Human‑in‑the‑Loop Validation
- Human experts review a sample of outputs to verify correctness, ethical compliance, and best practices.
- These reviews calibrate and improve automated evaluations.

#### End‑to‑End Testing
- Evaluate across the full operational environment (data ingestion → task execution → output generation).

### 9.3 Real‑World Testing
Deploy agents in actual production to uncover issues not seen in controlled environments.

**Why it matters:**
- Exposes the agent to real‑world complexity, unpredictable inputs, and natural language variations.
- Reveals edge cases and performance under high load.

**Implementation approach:**
1. **Deploy in phases** – start small‑scale, then expand.
2. **Monitor agent behavior** – track KPIs: response time, accuracy, user satisfaction, system stability.
3. **Collect user feedback** – invaluable for identifying gaps and improving usability.
4. **Iterate based on insights** – feed real‑world learnings back into development.

---
## 10. Conclusion

You don’t need a 30‑page plan to start building a good agent system – but a little foresight goes a long way.

- **Pick a tractable slice** – like our cancel‑order agent – build something small, testable, and immediately useful.
- **Define what success looks like**; avoid vague or over‑scoped ambitions.
- **Focus on delivering clear value quickly.**

Effective agent systems are more than a sum of their parts. They depend on:
- Strong architecture and disciplined engineering.
- Tight feedback loops (iterative design, robust evaluation).
- Phased rollouts and real‑world testing to turn prototypes into production‑reliable systems.

> [!quote] Next Chapter
> In Chapter 3, we shift focus to the **human side** – designing agent experiences that are clear, responsive, and intuitive for the people who rely on them. Ultimately, no matter how powerful your system architecture, its success depends on how it lands in human hands.