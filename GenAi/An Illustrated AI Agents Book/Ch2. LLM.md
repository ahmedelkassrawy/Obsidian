---
tags: [genai, llm, agents, transformers, post-training]
---

LLMs are what let an agent go from **observations** to **actions**.

## How an LLM generates text

> [!definition] Autoregressive model
> A model that generates text one token at a time. Each predicted token is added back to the input, and the model processes the new, longer input to predict the next token. Text generation is really a loop.

To power an agent, an LLM needs more than plain text prediction. Model creators add these extra capabilities in a later training phase called **post-training**. It teaches the model to read inputs and produce outputs in formats that support what an agent needs to do.

## Capabilities an agent needs

### System prompt

> [!definition] System prompt
> Instructions that describe how the model should behave. They take priority over whatever the end user asks the model.

The system prompt is part of how the model is *used*, not how it's *trained*.

### Multi-turn conversations

The model has to follow a conversation across several back-and-forth turns.

### Tool use

The model has to be able to request a tool call in a structured format the harness can parse.

## Building an LLM wrapper

The first piece of the harness is a `Response` model that holds everything we care about from one model call: the text, any reasoning, an optional tool call, and metadata.

```python
# llm.py
from pydantic import BaseModel

class Response(BaseModel):
    content: str = ""
    reasoning: str | None = None
    tool_call: dict | None = None
    metadata: dict | None = None
```

Next, the `LLM` class sends a chat-completions request to an OpenAI-compatible endpoint (OpenRouter here). A few things to notice:

- `max_tokens` is capped at 256.
- If `think` is `False`, it sets `reasoning_effort` to `"none"`.
- It retries up to 3 times on rate limits (`429`) and gateway errors (`502`, `503`, `504`), waiting `2 ** attempt` seconds between tries.
- It keeps only the **first** tool call if the model returns several.

```python
# llm.py
import json
import time
import urllib.error
import urllib.request

class LLM:
    def __init__(self, model: str,
                 api_key: str,
                 base_url: str = None,
                 think: bool = False):
        self.model = model
        self.api_key = api_key
        self.base_url = base_url
        self.think = think

    def generate(self, messages: list[dict],
                 tools: list | None = None) -> Response:
        # build request body
        body = {
            "model": self.model,
            "messages": messages,
            "max_tokens": 256,
        }

        if tools:
            body["tools"] = tools
        if not self.think:
            body["reasoning_effort"] = "none"

        request = urllib.request.Request(
            f"{self.base_url.rstrip('/')}/chat/completions",
            data=json.dumps(body).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer " + self.api_key,
            }
        )

        for attempt in range(3):
            try:
                with urllib.request.urlopen(request, timeout=60) as response:
                    data = json.loads(response.read())
                break
            except urllib.error.HTTPError as error:
                if error.code not in {429, 502, 503, 504} or attempt == 2:
                    details = error.read().decode("utf-8", errors="replace")
                    raise RuntimeError(
                        f"OpenRouter request failed with HTTP {error.code}: {details}"
                    ) from error
                time.sleep(2 ** attempt)
            except urllib.error.URLError as error:
                if attempt == 2:
                    raise RuntimeError(
                        f"OpenRouter request could not be completed: {error.reason}"
                    ) from error
                time.sleep(2 ** attempt)

        message = data["choices"][0]["message"]
        tool_calls = message.get("tool_calls", None)

        if tool_calls:
            tool_call = tool_calls[0]
        else:
            tool_call = None

        metadata = {
            "model": data["model"],
            "prompt_tokens": data["usage"]["prompt_tokens"],
            "completion_tokens": data["usage"]["completion_tokens"],
        }

        return Response(
            content=message.get("content") or "",
            reasoning=message.get("reasoning") or "",
            tool_call=tool_call,
            metadata=metadata
        )
```

Calling it:

```python
import os

llm = LLM(
    model="google/gemma-4-31b-it:free",
    api_key=os.environ["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1",
    think=False
)

response = llm.generate(
    messages=[
        {
            "role": "user",
            "content": "Hello, how are you? can you tell me what model you are?"
        }
    ],
    tools=None
)
print(response)
```

## Steps and trajectories

We're building an **agentic harness**, and a vital part of any harness is being able to see what happened during inference.

An agent may run for several turns and make a wrong tool call somewhere along the way. To debug that easily, we keep a record of everything the model has done so far.

```python
# trajectory.py
class Step(BaseModel):
    """single step in trajectory"""
    thought: str = ""
    action: dict | None = None
    observation: str | None = None
    answer: str | None = None
    metadata: dict | None = None
```

The fields of a step:

| Field | Meaning |
| --- | --- |
| `thought` | The model's reasoning for this step |
| `action` | A tool call the model made |
| `observation` | The output the tool returned |
| `answer` | The model's final answer — the agent has reached the end of its turn |
| `metadata` | Model name and token counts |

> [!definition] Action
> The book's word for a tool call. Chapter 6 builds loops of **thought → action → observation** that let an agent act on its own.

> [!definition] Trajectory
> The sequence of steps an agent takes, possibly using several actions, to reach its final answer.

We track the trajectory for the same reason as the steps: it makes it easy to find where and why an agent failed.

### Full script

Everything so far in one file, plus the `Trajectory` class and a `TinyAgent` that uses the `LLM` and records each run:

```python
import json
import os
import time
import urllib.error
import urllib.request
from pydantic import BaseModel

class Response(BaseModel):
    content: str = ""
    reasoning: str = ""
    tool_call: dict | None = None
    metadata: dict | None = None

class LLM:
    def __init__(self, model: str,
                 api_key: str,
                 base_url: str = None,
                 think: bool = False):
        self.model = model
        self.api_key = api_key
        self.base_url = base_url
        self.think = think

    def generate(self, messages: list[dict],
                 tools: list | None = None) -> Response:
        # build request body
        body = {
            "model": self.model,
            "messages": messages,
            "max_tokens": 256,
        }

        if tools:
            body["tools"] = tools
        if not self.think:
            body["reasoning_effort"] = "none"

        request = urllib.request.Request(
            f"{self.base_url.rstrip('/')}/chat/completions",
            data=json.dumps(body).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer " + self.api_key,
            }
        )

        for attempt in range(3):
            try:
                with urllib.request.urlopen(request, timeout=60) as response:
                    data = json.loads(response.read())
                break
            except urllib.error.HTTPError as error:
                if error.code not in {429, 502, 503, 504} or attempt == 2:
                    details = error.read().decode("utf-8", errors="replace")
                    raise RuntimeError(
                        f"OpenRouter request failed with HTTP {error.code}: {details}"
                    ) from error
                time.sleep(2 ** attempt)
            except urllib.error.URLError as error:
                if attempt == 2:
                    raise RuntimeError(
                        f"OpenRouter request could not be completed: {error.reason}"
                    ) from error
                time.sleep(2 ** attempt)

        message = data["choices"][0]["message"]
        tool_calls = message.get("tool_calls", None)

        if tool_calls:
            tool_call = tool_calls[0]
        else:
            tool_call = None

        metadata = {
            "model": data["model"],
            "prompt_tokens": data["usage"]["prompt_tokens"],
            "completion_tokens": data["usage"]["completion_tokens"],
        }

        return Response(
            content=message.get("content") or "",
            reasoning=message.get("reasoning") or "",
            tool_call=tool_call,
            metadata=metadata
        )

class Step(BaseModel):
    """single step in trajectory"""
    thought: str = ""
    action: dict | None = None
    observation: str | None = None
    answer: str | None = None
    metadata: dict | None = None

class Trajectory:
    """Manages execution runs, each containing a query and its sequence of steps."""

    def __init__(self):
        self.runs: list[dict] = []

    def initialize(self, query: str):
        """Starts a new run session with the given query and an empty step list."""
        self.runs.append(
            {
                "query": query,
                "steps": []
            }
        )

    def add(self, response: Response, observation: str | None = None):
        """Records a step from the model response, capturing intermediate actions or the final answer."""
        if not self.runs:
            raise RuntimeError("Cannot add a step before calling initialize().")

        # Base fields present in every step (reasoning and metadata).
        # Response is a Pydantic model, so read its attributes directly (it has no .get()).
        step = Step(
            thought=response.reasoning or "",
            metadata=response.metadata,
        )

        # If an observation is present, record the tool action and its result (intermediate step).
        # Otherwise, treat it as the final step containing the completed answer.
        if observation is not None:
            step.action = response.tool_call
            step.observation = observation
        else:
            step.answer = response.content

        # Append the constructed step to the current active run
        self.runs[-1]["steps"].append(step)


class TinyAgent:
    """A minimal, modular and educational agent framework"""
    def __init__(self, llm: LLM):
        self.llm = llm
        self.trajectory = Trajectory()
        self.memory = None
        self.tools = None
        self.planner = None

    def run(self, task: str):
        """Run agent on a task"""
        self.trajectory.initialize(task)
        return self._step(task)

    def _step(self, task: str):
        """Perform a single step: ask the LLM and record the result"""
        response = self.llm.generate(
            messages=[{"role": "user", "content": task}]
        )
        self.trajectory.add(response)
        return response.content

    def _execute_action(self, action: str):
        """Execute an action"""
        #### Implemented in a later chapter
        return f"Executed: {action}"


llm = LLM(
    model="google/gemma-4-31b-it:free",
    api_key=os.environ["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1",
    think=False
)

response = llm.generate(
    messages=[
        {
            "role": "user",
            "content": "Hello, how are you? can you tell me what model you are?"
        }
    ],
    tools=None
)
print(response)
```

### Invoking it as an agent

```python
llm = LLM(
    model="nvidia/nemotron-3-ultra-550b-a55b:free",
    api_key=os.environ["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1",
    think=False
)

agent = TinyAgent(llm=llm)
response = agent.run("What is the capital of France?")
# print(response)
print(agent.trajectory.runs)
```

Example output:

```text
[
    {
        'query': 'What is 2 + 2?',
        'steps': [
            Step(thought='',
                action=None,
                observation=None,
                answer='2 + 2 is 4.',
                metadata={
                    'model': 'gemma4:e4b', 'prompt_tokens': 17,
                    'completion_tokens': 9
                }
            )
        ]
    }
]
```

> [!note]
> The example output comes from a different run (the `2 + 2` query on `gemma4:e4b`), not the France query shown. Your own output will show your query and model.

> [!warning] Fixes vs the book's code
> - `Trajectory.add` originally called `response.get(...)`. `Response` is a Pydantic model with no `.get()`, so that crashed. It now reads `response.reasoning`, `response.content`, etc.
> - The book's `TinyAgent` skeleton took no arguments and had no `trajectory`, so `TinyAgent(llm=llm)` failed. It now takes an `llm`, creates a `Trajectory`, and `_step` calls the LLM and records the step. It sits after `Trajectory` in the script because its type hint needs `LLM` defined first.

### What we built

```text
TinyAgent/
├── agent.py       ← Updated (integrated the LLM into TinyAgent)
├── llm.py         ← New (an LLM wrapper for local or cloud models)
└── trajectory.py  ← New (Step and Trajectory tracking)
```

## Training an LLM

There are two major phases of training:

1. **Pre-training**
2. **Post-training**

LLMs get their name from pre-training, because it trains them on a language-processing task called **language modeling**.

![[Pasted image 20261026180006.png]]

### Pre-training: language modeling

> [!definition] Language modeling
> Showing a model a sequence of words and asking it to predict the word most likely to come next.

This phase needs a vast amount of data and takes up most of the compute spent on training. The data comes from curated mixes of web text, books, and code, each filtered for quality.

How one training step works:

1. Take a span of text and hide its last token.
2. Give the model all the earlier tokens and ask it to predict the next one.
3. Early on, the model almost always guesses wrong — that's expected.
4. Feed the wrong prediction and the correct word into the loss calculation, then update the model's weights so it has a better chance next time.

Repeat this billions of times and you get a **base model**.

### Post-training: SFT

Base models already have strong hidden abilities — reasoning, summarization, translation, code generation — but often need heavy prompt engineering to bring them out.

> [!definition] Supervised fine-tuning (SFT)
> The first step of post-training, also called **instruction-tuning**. It trains the model to follow the instructions we give it in prompts.

Each SFT training example is a **prompt** plus a **completion** that shows how we want the model to respond to that prompt.

The update rule is almost the same as in pre-training, with one key difference:

> [!tip] What SFT trains on
> The prompt tokens are in the input context, but they're **left out of the loss**. The model is trained only on the response tokens.

> [!warning] SFT isn't enough on its own
> SFT teaches the model to follow instructions, but it can't fully capture human preferences about what makes a response genuinely helpful, accurate, or well-reasoned. The reinforcement learning step is what pushes the model toward those preferences.

### Post-training: reinforcement learning

In SFT we *show* the model what the desired output looks like. RL works differently: we **score** the quality of a response the model generated and update the weights based on that score.

> [!definition] Reward
> The quality score given to a model-generated response during RL training.

#### RLHF

> [!definition] Reinforcement Learning from Human Feedback (RLHF)
> RL that uses preference scores collected from humans, or from specialized models called **reward models**.

![[Pasted image 20261027141403.png]]

The RLHF objective is to make the model **more** likely to produce output like the preferred response and **less** likely to produce output like the rejected one.

It's used to polish behaviors like response length, the kind of language the model uses, which completions are safe to generate or avoid, and many more.

![[Pasted image 20261027141600.png]]

#### RLVR

> [!definition] Reinforcement Learning with Verifiable Rewards (RLVR)
> RL where the reward comes from an **automated check** of the output — for example, whether it follows a required format, or whether its final answer matches a correct answer we already know (as with math problems).

In an RLVR training step:

1. Take a problem and pass it to the model, along with instructions about the output format we want.
2. The model generates its output.
3. Automatically check whether it followed the format and whether it reached the correct solution.
4. Combine both scores into one reward signal and use it to update the weights.

![[Screenshot 2026-10-27 142408.png]]

The two kinds of reward:

| Reward | What it checks | Score |
| --- | --- | --- |
| Format reward | Did the model use the correct format (e.g. the right tags)? | 0.3 if correct, 0 if not |
| Accuracy reward | Does the final result match the actual answer? | 0.7 if correct, 0 if not |

#### GRPO

> [!definition] Group Relative Policy Optimization (GRPO)
> An RL algorithm that, instead of scoring a single response, generates a **group** of responses to the same prompt at each training step. A temperature setting keeps the responses diverse.

For example, we generate five answers from the model, give each one a reward, and use those scores to update the model.

![[Pasted image 20261027145447.png]]

## Transformer architecture

A Transformer decoder has three major components:

1. A **tokenizer**
2. A stack of **Transformer blocks**
3. A **language modeling head** (LM head)

> [!definition] Tokenizer
> The software that breaks the input text into tokens. It has a fixed vocabulary size — say, 50,000 tokens.

The model has the same number of **embedding vectors** as there are tokens in the vocabulary — one per token.

> [!definition] Embedding
> A numeric vector that represents a token. Embeddings are what the model actually computes with when it processes its input.

![[Pasted image 20261027150825.png]]

![[Pasted image 20261027151009.png]]

### The LM head

- The final vector is passed to the LM head to interpret.
- The LM head does a simple calculation that produces a **probability score for every token** in its vocabulary.
- Those scores reflect everything the model learned in training. Tokens with high probabilities are the ones most likely to come next.

### Processing through the Transformer blocks

A neural network turns inputs into an output in a **forward pass**: the calculation flows through its layers in order.

The Transformer blocks work exactly this way. The first block processes the input and passes its result to the next block, and so on. The final block hands its result to the LM head, and then decoding happens as described above.

### Context length

> [!definition] Context length (context size)
> The number of "tracks" a model supports — that is, how many tokens can flow through it at once. A model with a 100,000-token context length can only hold that many tokens, which limits its combined input and output.

For agent developers, context length is a key factor when choosing a model. It caps how much information you can put in the model's input.

> [!definition] Context engineering
> The discipline of choosing the most relevant information to fit inside the model's context limit. The book comes back to this repeatedly.

### KV caching

After the first forward pass processes all the input tokens, it's common to **cache** the results. On the next forward pass, the model then only processes the one track for the new token being generated.

> [!definition] KV caching
> Caching the results of earlier forward passes so that only the newest token needs processing. Also called **prompt caching** or **prefix caching**.

## Inside the Transformer block

The first block does some processing on the input vectors and hands its results — the same number and size of vectors — to the next block. This continues block by block until the last block in the stack.

Each Transformer block has two major components:

- A **self-attention** layer
- A **feed-forward neural network** layer

![[Pasted image 20261027152027.png]]

### The feed-forward neural network

This layer does the heavy lifting in predicting the next token, because training shapes it to reproduce the patterns in the training data.

For example, a feed-forward network trained on vast amounts of web data, given the words *"The Shawshank,"* would predict *"Redemption"* next — because the 1994 film is by far the most common place that sequence appears.

> [!definition] Mixture of Experts (MoE)
> An architecture that replaces one large feed-forward network with many smaller, more specialized networks called **experts**. A **router** looks at each input token and decides which expert (or set of experts) is best suited to process it.

The book's example is a basic MoE feed-forward layer with four experts behind a router.

![[Pasted image 20261027152316.png]]

### Self-attention: an overview

Language carries a lot of meaning in **word order** and **context**.

- A word like *bank* can mean a financial institution or a riverbank.
- We can only tell which one is meant by looking at the context around it.
- The self-attention layer is what lets the Transformer make that distinction.

> [!definition] Self-attention
> A layer that enriches a token's vector with information from the most relevant **previous** tokens in the sequence.

![[Pasted image 20261027152601.png]]

Self-attention works in two steps:

1. **Score** how relevant each previous token is.
2. **Combine** the relevant information into the token being processed.

---
