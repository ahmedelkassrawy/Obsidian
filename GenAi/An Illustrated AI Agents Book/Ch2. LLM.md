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