```python
from pydantic_ai import Agent
import asyncio
import os

os.environ["GEMINI_API_KEY"] = "AIzaSyB38nvrIt6MFrEchALd6Eouz9UHVrt9Tso"  # Replace with your actual API key

agent = Agent(
    'google-gla:gemini-2.0-flash',
    system_prompt="Be concise,reply with one sentence"
)

result1 = agent.run_sync("Tell me a joke")
print(result1.data)

result2 = agent.run_sync("Explain?",message_history=result1.new_messages())
print(result2.data)

print(result2.all_messages())
```

```python
result1 = agent.run_sync("Tell me a joke")
history = result1.new_messages() #extract mesage history 
as_python_objects = to_jsonable_python(history) #convert the mesage hsitory to json
history = ModelMessagesTypeAdapter.validate_python(as_python_objects) #convert the json to the same type as the original message history
res2 = agent.run_sync("Tell me a different joke",
                      message_history = history)

```

#### Iterating over the agent steps
```python
async def main():
    nodes = []

    async with agent.iter("What is Pydantic-AI") as agent_run:
        async for node in agent_run:
            nodes.append(node)

    # print(nodes)
    print(agent_run.result.data)
	print(agent_run.usage())

asyncio.run(main())

#start a stream of intermediate steps taken by agent
#iterate over each step the agent takes while answering the question
#collect each step
#and print the final result
```

### What is happening here?
1. **`agent.iter()` starts a streaming execution**
    - It doesn’t just return the final answer but allows us to track each processing step (**node**).
    - `agent_run` represents the **agent's execution graph**.

```python
res = agent.run_sync(
    'What is the capital of Italy? Answer with just the city.',
    usage_limits=UsageLimits(response_tokens_limit=10),
)

print(res.usage())
print(res.data)
```

```python
try:
    res_exception = agent.run_sync(
        'What is the capital of Italy? Answer with paragraph.',
        usage_limits=UsageLimits(response_tokens_limit=5),
    )
except UsageLimitExceeded as e:
    print(e)
```

```python
res = agent.run_sync(
    'What is the capital of Italy?', model_settings={'temperature': 0.0})

print(res.data)
```

```python
from pydantic_ai import Agent,RunContext
from datetime import date

agent = Agent(
    'google-gla:gemini-2.0-flash',
    deps_type = str,
    system_prompt="Use the customer's name while replying to them."
)

@agent.system_prompt
def add_user_name(ctx : RunContext[str]) -> str:
    return f"The user's name is {ctx.deps}"

@agent.system_prompt
def add_the_date() -> str:  
    return f'The date is {date.today()}.'


result = agent.run_sync('What is the date?', deps='Frank')
print(result.data)
```