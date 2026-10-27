LLM power agents to go from observations to actions

Autoregressive models -> the ones that output text is actually a loop where the text is predicted one after another , and then added as input and then we process the new input again to generate next token.

For an LLM to be able to power an agent, it needs an additional set of capabilities to fit the expected role. LLM creators train LLMs in the subsequent phase of training, called posttraining, to be able to parse inputs and generate outputs in a format that supports these expected capabilities

System Prompt
Describe the expected behaviour of the model in a way that takes priorty over what the end user ask the model

Its baked into how the model is used rather than how its trained

Multiturn conversations
Tool Use 

```python
from pydantic import BaseModel

class Response(BaseModel):
	content:str = ""
	reasoning: str | None = None
	tool_call:dict | None = None
	metadata: dict | None = None
```

```python 
class LLM:
    def __init__(self,model:str,
                api_key:str,
                base_url:str=None,
                think:bool = False):
        self.model = model
        self.api_key = api_key
        self.base_url = base_url
        self.think = think

    def generate(self,messages:list[dict],
                tools:list | None = None) -> Response:
        #build request body
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
            data = json.dumps(body).encode("utf-8"),
            headers = {
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
            content = message.get("content") or "",
            reasoning = message.get("reasoning") or "",
            tool_call = tool_call,
            metadata = metadata
        )
```

```python
llm = LLM(model = "google/gemma-4-31b-it:free",
    api_key= os.environ["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1",
    think = False
)

response = llm.generate(
    messages = [
        {
            "role": "user",
            "content": "Hello, how are you? can you tell me what model you are?"
        }
    ],
    tools = None
)
print(response)
```

A step and trajectory
we arre creating an agentic harness and a vital component of any harness , is that we can easily debug what is happening during inference

An agent might run for several turns at a time and run into an incorrent tool usage.To easily debug that we want to keep track of evetyhing the model has done so far

```python
class Step(BaseModel):
    """single step in trajectory"""
    thought:str = ""
    action:dict | None = None
    observation:str | None = None
    answer:str | None = None
    metadata:dict | None = None
```

The answer is the final answer of the model and represents that the agent has reached the end of its turn.

The observation is the output of tool usage

we use the term action to describe a tool call because in Chapter 6 we will explore loops of thought → action → observation that allow for autonomous behavior.

To reach its final answer, an agent might need various steps and use different actions. This sequence of steps is called the agent’s trajectory

We likewise track this information as it allows for easily debugging this sequence of steps to identify where and why an agent might have failed

```python
import json
import os
import time
import urllib.error
import urllib.request
from pydantic import BaseModel

class TinyAgent:
    """A minimal , modular and educational agent framework"""
    def __init__(self):
        self.llm = None
        self.memory = None
        self.tools = None
        self.planner = None

    def run(self,task:str):
        """Run agent on a task"""
        return self._step(task)

    def _step(self,task:str):
        """Perform a single step"""
        #### IMplemeneted 
        return f"Recieved: {task}"

    def _execute_action(self,action:str):
        """Execute an action"""
        #### Implemented
        return f"Executed: {action}"


class Response(BaseModel):
    content: str = ""
    reasoning: str = ""
    tool_call:dict | None = None
    metadata:dict | None = None

class LLM:
    def __init__(self,model:str,
                api_key:str,
                base_url:str=None,
                think:bool = False):
        self.model = model
        self.api_key = api_key
        self.base_url = base_url
        self.think = think

    def generate(self,messages:list[dict],
                tools:list | None = None) -> Response:
        #build request body
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
            data = json.dumps(body).encode("utf-8"),
            headers = {
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
            content = message.get("content") or "",
            reasoning = message.get("reasoning") or "",
            tool_call = tool_call,
            metadata = metadata
        )

class Step(BaseModel):
    """single step in trajectory"""
    thought:str = ""
    action:dict | None = None
    observation:str | None = None
    answer:str | None = None
    metadata:dict | None = None

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

        # Base fields present in every step (reasoning and metadata)
        step = Step(
            thought=response.get("reasoning", ""),
            metadata=response.get("metadata", None),
        )

        # If an observation is present, record the tool action and its result (intermediate step).
        # Otherwise, treat it as the final step containing the completed answer.
        if observation is not None:
            step.action = response.get("tool_call", None)
            step.observation = observation
        else:
            step.answer = response.get("content", "")

        # Append the constructed step to the current active run
        self.runs[-1]["steps"].append(step)

llm = LLM(model = "google/gemma-4-31b-it:free",
    api_key= os.environ["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1",
    think = False
)

response = llm.generate(
    messages = [
        {
            "role": "user",
            "content": "Hello, how are you? can you tell me what model you are?"
        }
    ],
    tools = None
)
print(response)
```

Invoking as agent
```python
llm = LLM(model = "nvidia/nemotron-3-ultra-550b-a55b:free",
    api_key= os.environ["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1",
    think = False
)

agent = TinyAgent(llm=llm)
response = agent.run("What is the capital of France?")
# print(response)
print(agent.trajecotry.runs)
```

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

What we built?
```text
TinyAgent/ 
├── agent.py ← Updated (Integrated the `LLM` into your `TinyAgent`) 
├── llm.py ← New (An LLM wrapper for local or cloud models) 
└── trajectory.py ← New (Step and Trajectory tracking)
```

### Training a LLM
Two major phases of training 
- Pre Training 
- Post Training

Pretraing -> where they get their name from , because they are trained on a Language processing task called `Language Modeling`

![[Pasted image 20261026180006.png]]

Pretraining : Language Modeling
Language Modelling is the task of presenting a model with a seq of words -> and asking it to predict the next word that is most likely to appear

This phase requires vast amount and it takes a major part of the computing done during the training process

Pretraining data is drawn from curated mixtures of sources including web text, books, and code, each filtered to satisfy quality criteria.

we can take one span of that text and present it to the model. We hide the last token, give the model all the previous tokens, and ask it to predict the next word in the sequence.

At the start, the model under training would almost always guess incorrectly, which is part of the process. Now that we have its wrong prediction and the correct word, we plug them both in our loss calculation and update the weights of the model so that next time it has a better chance of making the right prediction. This is done billions of times and in the end results in a base model.

Post Training :SFT
Base models have strong latent capabilities, including reasoning, summarization, translation, and code generation, that often require heavy prompt engineering to unlock.

The first step of posttraining is called supervised fine-tuning (SFT). It is also sometimes referred to as instruction-tuning because it’s where a model is trained to follow instructions we give it in prompts.

SFT training example is composed of a prompt and a completion that shows how we want the model to behave if it sees such a prompt.

The update rule is almost identical to that of pretraining

The key difference:
While prompt tokens are included in the input context, they are excluded from the loss computation -> so the model is trained on only the response tokens

The SFT training phase is essential, yet not enough to produce a cutting-edge model. It teaches the model to follow instructions, but it cannot fully capture human preferences about what makes a response genuinely helpful, accurate, or well-reasoned

The RL step is what pushes the model to be fully captured human preferences that make it helpful

Post Training: Reinforcement Learning
- In SFT , we show the model what the desired output looks like

RL is a different training methodology , we use methods that evaluate quality of a model generated response and update the model weights based on quality score , called `reward`

Reinforcement Learning from Human Feedback (RLHF), which relies on preference scores collected from humans or specialized models called reward models,

![[Pasted image 20261027141403.png]]

The RLHF training objective is to update the model to increase the likelihood of generating output like the preferred response and decrease the likelihood of generating output like the rejected response. 

This can be used to polish model behaviors such as response length, type of language the model uses, safe type of completions to generate or to avoid, and many other types of behaviors

![[Pasted image 20261027141600.png]]

Reinforcement Learning with Verifiable Rewards (RLVR).
- it updates the model based on a reward score
- The difference here is that the rewards can be obtained from automated ways of verifying the outputs
- for example, if it follows a certain format, or the final answer it results in is equal to the correct answer (that we knew beforehand, in the case of math problems, for example).

In an RLVR training step, we take one of the problems and pass it to the model with instructions about the format that we want. 

Once the model generates its output, we can automatically verify whether it followed the requested format and if it arrived at the correct solution of the problem.

The model’s response is then scored on two verifiable dimensions: format (did it use the correct tags?) and accuracy (was the answer right?). The combined reward signal is used to update the model weights.


![[Screenshot 2026-10-27 142408.png]]

Two kinds of rewards:
- format reward -> scoring whether the model uses the correct format for the output and assigning reward of 0.3 if correct or 0 if incorrect
- accuracy reward -> compares the final result to the actual result and assigns a reward of 0.7 if correct and 0 if incorrect

Group Relative Policy Optimizations (GRPO) algo has another key ingredient beyond reward assignement

Rather than scoring a single response , at each training step GRPO generates a group of response for the same prompt using a temp setting that ensure diversity among them

We generate five answers from the model, assign a reward to each one, and use those scores to update the model.

![[Pasted image 20261027145447.png]]

