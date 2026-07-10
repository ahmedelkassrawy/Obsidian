#### Workflow
A workflow is an event driven,step based way to control the execution flow

Your app is divided into sections called "Steps" which are triggered by "Events".By combining steps and events , you can create complex flows that encapsulate logic and make your app more maintainabke and easier to undersatnd.They can have arbitrary inputs and outputs, which are passed around by Events.
## An example

In this visualization, you can see a moderately complex workflow designed to take a query, optionally improve upon it, and then attempt to answer the query using three different RAG strategies. The LLM gets answers from all three strategies and judges which is the “best”, and returns that. We can break this flow down:
- It is triggered by a `StartEvent`
- A step called `judge_query` determines if the query is of high quality. If not, a `BadQueryEvent` is generated.
- A `BadQueryEvent` will trigger a step called `improve_query` which will attempt to improve the query, which will then trigger a `JudgeEvent`
- A `JudgeEvent` will trigger `judge_query` again, creating a loop which can continue until the query is judged of sufficient quality. This is called “Reflection” and is a key part of agentic applications that Workflows make easy to implement.
- If the query is of sufficient quality, 3 simultaneous events are generated: a `NaiveRAGEvent`, a `HighTopKEvent`, and a `RerankEvent`. These three events trigger 3 associated steps in parallel, which each run a different RAG strategy.
- Each of the query steps generates a `ResponseEvent`. A `ResponseEvent` triggers a step called `judge_response` which will wait until it has received all 3 responses.
- `judge_response` will then pick the “best” response and return it to the user via a `StopEvent`.
![[Pasted image 20251015181225.png]]

Other frameworks and LlamaIndex itself have attempted to solve this problem previously with directed acyclic graphs (DAGs) but these have a number of limitations that workflows do not:

- Logic like loops and branches needed to be encoded into the edges of graphs, which made them hard to read and understand.
- Passing data between nodes in a DAG created complexity around optional and default values and which parameters should be passed.
- DAGs did not feel natural to developers trying to developing complex, looping, branching AI applications.
The event-based pattern and vanilla python approach of Workflows resolves these problems.

For simple RAG pipelines and linear demos we do not expect you will need Workflows, but as your application grows in complexity, we hope you will reach for them.

#### Single step workflow
```python
class Myworkflow(Workflow):
    @step
    async def my_step(self,ev:StartEvent) -> StopEvent:
        print("Hello, this is my custom workflow step!")
        return StopEvent(result = "Hello, World!")

async def main():
    w = Myworkflow(timeout=10, verbose=False)
    result = await w.run()
    print(result)
```

## Type annotations for steps

The type annotations (e.g. `ev: StartEvent`) and `-> StopEvent` are essential to the way Workflows work. The expected types determine what event types will trigger a step. Tools like the visualizer (see below) also rely on these annotations to determine what types are generated and therefore where control flow goes next.

Type annotations are validated at compile time, so you will get an error message if for instance you emit an event that is never consumed by another step.

## Start and Stop events

`StartEvent` and `StopEvent` are special events that are used to start and stop a workflow. Any step that accepts a `StartEvent` will be triggered by the `run` command. Emitting a `StopEvent` will end the execution of the workflow and return a final result, even if other steps remain un-executed.

## Running a workflow in regular python

Workflows are async by default, so you use `await` to get the result of the `run` command. This will work fine in a notebook environment; in a vanilla python script you will need to import `asyncio` and wrap your code in an async function, like this:
```python
if __name__ == "__main__":
    asyncio.run(main())
    
    draw_all_possible_flows(
		    Myworkflow,
		    filename= "basic_workflow.html")
```

![[Pasted image 20251015182753.png]]
#### Multiple Step Workflow
Now we define the workflow itself. We do this by defining the input and output types on each step.

- `step_one` takes a `StartEvent` and returns a `FirstEvent`
- `step_two` takes a `FirstEvent` and returns a `SecondEvent`
- `step_three` takes a `SecondEvent` and returns a `StopEvent`

```python
from llama_index.core.workflow import (
    StartEvent,
    StopEvent,
    Workflow,
    step,
    Event,
)
from llama_index.utils.workflow import draw_all_possible_flows

class FirstEvent(Event):
    first_output : str

class SecondEvent(Event):
    second_output : str

class Myworkflow(Workflow):
    @step
    async def step_one(self,ev:StartEvent) -> FirstEvent:
        print(ev.first_input)
        return FirstEvent(first_output= "First step complete")
    
    @step
    async def step_two(self,ev:FirstEvent) -> SecondEvent:
        print(ev.first_output)
        return SecondEvent(second_output= "Second step complete")
    
    @step
    async def step_three(self,ev:SecondEvent) -> StopEvent:
        print(ev.second_output)
        return StopEvent(result= "Workflow complete")
    
async def main():
    wf = Myworkflow()
    result = await wf.run(first_input="Start the workflow")
    draw_all_possible_flows(Myworkflow, file_name = "workflow_diagram.html")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

![[Pasted image 20251015184121.png]]

#### Loops in workflows
```python
class LoopEvent(Event):
    loop_output: str
```

```python
class Myworkflow(Workflow):
    @step
    async def step_one(self,ev:StartEvent | LoopEvent) -> FirstEvent | LoopEvent:
        if random.randint(0,1) == 0:
            print("Bad thing happend")
            return LoopEvent(loop_output = "Back to step one")
        else:
            print("Good thing happend")
            return FirstEvent(first_output= "First step complete")
    
    @step
    async def step_two(self,ev:FirstEvent) -> SecondEvent:
        print(ev.first_output)
        return SecondEvent(second_output= "Second step complete")
    
    @step
    async def step_three(self,ev:SecondEvent) -> StopEvent:
        print(ev.second_output)
        return StopEvent(result= "Workflow complete")
    
async def main():
    wf = Myworkflow()
    result = await wf.run(first_input="Start the workflow")
    draw_all_possible_flows(Myworkflow, filename= "workflow_diagram.html")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

![[Pasted image 20251015185105.png]]

##### Branching
```python
class FirstEvent(Event):
    first_output:str

class SecondEvent(Event):
    second_output:str

class LoopEvent(Event):
    loop_output:str

class BranchA1Event(Event):
    payload:str

class BranchA2Event(Event):
    payload:str

class BranchB1Event(Event):
    payload:str

class BranchB2Event(Event):
    payload:str

class BranchWorkflow(Workflow):
    @step
    async def start(self, ev: StartEvent) -> BranchA1Event | BranchB1Event:
        if random.randint(0,1) == 0:
            print("Go to branch A")
            return BranchA1Event(payload="Branch A")
        else:
            print("Go to branch B")
            return BranchB1Event(payload="Branch B")
        
    @step
    async def step_a1(self, ev: BranchA1Event) -> BranchA2Event:
        print(ev.payload)
        return BranchA2Event(payload=ev.payload)

    @step
    async def step_b1(self, ev: BranchB1Event) -> BranchB2Event:
        print(ev.payload)
        return BranchB2Event(payload=ev.payload)

    @step
    async def step_a2(self, ev: BranchA2Event) -> StopEvent:
        print(ev.payload)
        return StopEvent(result="Branch A complete.")

    @step
    async def step_b2(self, ev: BranchB2Event) -> StopEvent:
        print(ev.payload)
        return StopEvent(result="Branch B complete.")

    
async def main():
    wf = BranchWorkflow()
    result = await wf.run(first_input="Start the workflow")
    draw_all_possible_flows(BranchWorkflow, filename= "workflow_diagram.html")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

#### Maintaining State
we have passed data from step to step using properties of custom events. This is a powerful way to pass data around, but it has limitations. For example, if you want to pass data between steps that are not directly connected, you need to pass the data through all the steps in between. This can make your code harder to read and maintain.

To avoid this pitfall, we have a `Context` object available to every step in the workflow. To use it, declare an argument of type `Context` to your step. Here’s how you do that.
```python
from llama_index.core.workflow import (
    StartEvent,
    StopEvent,
    Workflow,
    step,
    Event,
    Context,
)
```

Now we define a `start` event that checks if data has been loaded into the context. If not, it returns a `SetupEvent` which triggers `setup` that loads the data and loops back to `start`.

```python
class SetupEvent(Event):
    query:str

class StepTwoEvent(Event):
    query:str

class StatefulFlow(Workflow):
    @step
    async def start(self,
                    ctx:Context,ev:StartEvent) -> SetupEvent | StepTwoEvent:
        db = await ctx.store.get("some_database",default = None)

        if db is None:
            print("Need to load data")
            return SetupEvent(query = ev.query)
        
        return StepTwoEvent(query = ev.query)
    
    @step
    async def setup(self,ev:SetupEvent,ctx:Context) -> StartEvent:
        #load data
        await ctx.store.set("some_database",[1,2,3])
        return StartEvent(query = ev.query)
    
    @step 
    async def step_two(self,ctx:Context,ev:StepTwoEvent) -> StopEvent:
        print("Data is",await ctx.store.get("some_database"))
        return StopEvent(result = await ctx.store.get("some_database"))
    
async def main():
    wf = StatefulFlow()
    result = await wf.run(query="Some query")
    draw_all_possible_flows(StatefulFlow, filename= "workflow_diagram.html")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

## Handling Concurrent State Changes

When multiple agents are running in parallel, it’s possible that they will try to modify the same state at the same time. This can lead to race conditions and unexpected behavior.

To avoid this, you can use a `with` statement to edit the state. This will ensure that the state is updated atomically.

```python
async with ctx.store.edit_state() as state:    
	state["some_key"] = "some_value"
```

This will ensure that only one step/task can access and edit the state at a given time. If other steps/tasks need to access the state, they will wait until the current edit operation exits.

## Adding Typed State

Often, you’ll have some preset shape that you want to use as the state for your workflow. The best way to do this is to use a `Pydantic` model to define the state. This way, you:

- Get type hints for your state
- Get automatic validation of your state
- (Optionally) Have full control over the serialization and deserialization of your state using [validators](https://docs.pydantic.dev/latest/concepts/validators/) and [serializers](https://docs.pydantic.dev/latest/concepts/serialization/#custom-serializers)

**NOTE:** You should use a pydantic model that has defaults for all fields. This enables the `Context` object to automatically initialize the state with the defaults.

Here’s a quick example of how you can leverage workflows + pydantic to take advantage of all these features:
```python
from pydantic import BaseModel, Field, field_validator, field_serializer
from typing import Union

from llama_index.core.workflow import (
    Context,
    Workflow,
    StartEvent,
    StopEvent,
    step,
)


# This is a random object that we want to use in our state
class MyRandomObject:
    def __init__(self, name: str = "default"):
        self.name = name


# This is our state model
# NOTE: all fields must have defaults
class MyState(BaseModel):
    model_config = {"arbitrary_types_allowed": True}
    my_obj: MyRandomObject = Field(default_factory=MyRandomObject)
    some_key: str = Field(default="some_value")

    # This is optional, but can be useful if you want to control the serialization of your state!

    @field_serializer("my_obj", when_used="always")
    def serialize_my_obj(self, my_obj: MyRandomObject) -> str:
        return my_obj.name

    @field_validator("my_obj", mode="before")
    @classmethod
    def deserialize_my_obj(
        cls, v: Union[str, MyRandomObject]
    ) -> MyRandomObject:
        if isinstance(v, MyRandomObject):
            return v
        if isinstance(v, str):
            return MyRandomObject(v)

        raise ValueError(f"Invalid type for my_obj: {type(v)}")


class MyStatefulFlow(Workflow):
    @step
    async def start(self, ctx: Context[MyState], ev: StartEvent) -> StopEvent:
        # Allows for atomic state updates
        async with ctx.store.edit_state() as state:
            state.my_obj.name = "new_name"

        # Can also access fields directly if needed
        name = await ctx.store.get("my_obj.name")

        return StopEvent(result="Done!")


w = MyStatefulFlow(timeout=10, verbose=False)

ctx = Context(w)
result = await w.run(ctx=ctx)
state = await ctx.store.get_state()
print(state)
```

#### Streaming Events
In `step_one` and `step_three` we write individual events to the event stream. In `step_two` we use `astream_complete` to produce an iterable generator of the LLM’s response, then we produce an event for each chunk of data the LLM sends back to us — roughly one per word — before returning the final response to `step_three`.

To actually get this output, we need to run the workflow asynchronously and listen for the events, like this:
```python
class FirstEvent(Event):
    first_output:str

class SecondEvent(Event):
    second_output:str
    response:str

class ProgressEvent(Event):
    msg:str

class MyWorkflow(Workflow):
    @step
    async def step_one(self,ctx:Context,event:StartEvent) -> FirstEvent:
        ctx.write_event_to_stream(ProgressEvent(msg = "Step one is happening"))
        return FirstEvent(first_output="First Step completed")
    
    @step
    async def step_two(self,ctx:Context,ev:FirstEvent) -> SecondEvent:
        generator = await llm.astream_complete(
            "Please give me the first 3 paragraphs of Moby Dick, a book in the public domain."
        )
         
        async for response in generator:
            # Allow the workflow to stream this piece of response
            ctx.write_event_to_stream(ProgressEvent(msg=response.delta))
        return SecondEvent(
            second_output="Second step complete, full response attached",
            response=str(response),
        )
        
    @step 
    async def step_three(self,ctx:Context,ev:SecondEvent) -> StopEvent:
        ctx.write_event_to_stream(ProgressEvent(msg="Step three is happening"))
        return StopEvent(result="Workflow complete.")
    
async def main():
    wf = MyWorkflow()
    handler = wf.run(first_input = "Start the workflow.")

    async for ev in handler.stream_events():
        if isinstance(ev, ProgressEvent):
            print(ev.msg)

    final_result = await handler
    print("Final result",final_result)

    draw_all_possible_flows(MyWorkflow,filename = "streaming.html")

if __name__ == "__main__":
    asyncio.run(main())
```

`run` runs the workflow in the background, while `stream_events` will provide any event that gets written to the stream. It stops when the stream delivers a `StopEvent`, after which you can get the final result of the workflow as you normally would.

#### Concurrent execution of Workflows
In addition to looping and branching, workflows can run steps concurrently. This is useful when you have multiple steps that can be run independently of each other and they have time-consuming operations that they `await`, allowing other steps to run in parallel.
##### Emitting multiple events
In our examples so far, we’ve only emitted one event from each step. But there are many cases where you would want to run steps in parallel. To do this, you need to emit multiple events. You can do this using `send_event`:
```python
class StepTwoEvent(Event):
    query: str

class ParallelFlow(Workflow):
    @step
    async def start(self, ctx: Context, ev: StartEvent) -> StepTwoEvent | None:
        ctx.send_event(StepTwoEvent(query="Query 1"))
        ctx.send_event(StepTwoEvent(query="Query 2"))
        ctx.send_event(StepTwoEvent(query="Query 3"))

    @step(num_workers=4)
    async def step_two(self, ctx: Context, ev: StepTwoEvent) -> StopEvent:
        print("Running slow query ", ev.query)
        await asyncio.sleep(2)

        return StopEvent(result=ev.query)


async def main():
    wf = ParallelFlow()
    result = await wf.run()
    print("Final result",result)

    draw_all_possible_flows(ParallelFlow,filename = "streaming.html")

if __name__ == "__main__":
    asyncio.run(main())
```

In this example, our `start` step emits 3 `StepTwoEvent`s. The `step_two` step is decorated with `num_workers=4`, which tells the workflow to run up to 4 instances of this step concurrently (this is the default).

## Collecting events

If you execute the previous example, you’ll note that the workflow stops after whichever query is first to complete. Sometimes that’s useful, but other times you’ll want to wait for all your slow operations to complete before moving on to another step. You can do this using `collect_events`:
```python
class StepTwoEvent(Event):
    query: str

class StepThreeEvent(Event):
    result: str

class ConcurrentFlow(Workflow):
    @step
    async def start(self, ctx: Context, ev: StartEvent) -> StepTwoEvent | None:
        ctx.send_event(StepTwoEvent(query="Query 1"))
        ctx.send_event(StepTwoEvent(query="Query 2"))
        ctx.send_event(StepTwoEvent(query="Query 3"))

    @step(num_workers=4)
    async def step_two(self, ctx: Context, ev: StepTwoEvent) -> StepThreeEvent:
        print("Running query ", ev.query)
        await asyncio.sleep(2)

        return StepThreeEvent(result=ev.query)

    @step
    async def step_three(self,ctx:Context,ev: StepThreeEvent) -> StopEvent | None:
        #wait untill we recievve 3 events
        result = ctx.collect_events(ev,[StepThreeEvent] * 3)
        if result is None:
            return None

        print(result)
        return StopEvent(result="Done")


async def main():
    wf = ConcurrentFlow()
    result = await wf.run()
    print("Final result",result)

    draw_all_possible_flows(ConcurrentFlow,filename = "streaming.html")

if __name__ == "__main__":
    asyncio.run(main())
```

The `collect_events` method lives on the `Context` and takes the event that triggered the step and an array of event types to wait for. In this case, we are awaiting 3 events of the same `StepThreeEvent` type.

The `step_three` step is fired every time a `StepThreeEvent` is received, but `collect_events` will return `None` until all 3 events have been received. At that point, the step will continue and you can do something with all 3 results together.

The `result` returned from `collect_events` is an array of the events that were collected, in the order that they were received.

## Multiple event types
Of course, you do not need to wait for the same type of event. You can wait for any combination of events you like, such as in this example:
```python
class StepAEvent(Event):
    query:str

class StepBEvent(Event):
    query:str

class StepCEvent(Event):
    query:str

class StepAComplete(Event):
    result:str

class StepBComplete(Event):
    result:str

class StepCComplete(Event):
    result:str

class ConcurrentFlow(Workflow):
    @step
    async def start(self,ctx:Context,ev:StartEvent) -> StepAEvent | StepBEvent | StepCEvent | None:
        ctx.send_event(StepAEvent(query = "Query 1"))
        ctx.send_event(StepBEvent(query = "Query 2"))
        ctx.send_event(StepCEvent(query = "Query 3"))

    @step
    async def step_a(self,ctx:Context,ev:StepAEvent) -> StepAComplete:
        print("Doing step A")
        return StepAComplete(result = ev.query)

    @step
    async def step_b(self,ctx:Context,ev:StepBEvent) -> StepBComplete:
        print("Doing Step B")
        return StepBComplete(result = ev.query)
    
    @step
    async def step_c(self,ctx:Context,ev:StepCEvent) -> StepCComplete:
        print("Doing Step C")
        return StepCComplete(result = ev.query)

    @step
    async def end(self,ctx:Context,ev:StepAComplete | StepBComplete | StepCComplete) -> StopEvent:
        print("All steps complete",ev.result)
        
        #wait to get the return of the 3 events
        if ctx.collect_events(ev,[StepAComplete,StepBComplete,StepCComplete]) is None:
            return None

        return StopEvent(result = "All steps done")

async def main():
    wf = ConcurrentFlow()
    result = await wf.run()
    print("Final result",result)

    # draw_all_possible_flows(ConcurrentFlow,filename = "streaming.html")

if __name__ == "__main__":
    asyncio.run(main())
```

There are several changes we’ve made to handle multiple event types:
- `start` is now declared as emitting 3 different event types
- `step_three` is now declared as accepting 3 different event types
- `collect_events` now takes an array of the event types to wait for

Note that the order of the event types in the array passed to `collect_events` is important. The events will be returned in the order they are passed to `collect_events`, regardless of when they were received.

The visualization of this workflow is quite pleasing:
![[Pasted image 20251015232938.png]]

#### Subclassing workflows
Another great feature of workflows is their extensibility. You can take workflows written by others or built-ins from LlamaIndex and extend them to customize them to your needs. We’ll look at two ways to do that.

The first is subclassing: workflows are just regular Python classes, which means you can subclass them to add new functionality. For example, let’s say you have an agentic workflow that does some processing and then sends an email. You can subclass the workflow to add an extra step to send a text message as well.

Our base workflow:
```python
class Step2Event(Event):
    query: str

class Step3Event(Event):
    query: str

class MainWorkflow(Workflow):
    @step
    async def start(self,ctx:Context,ev:StartEvent) -> Step2Event:
        print("Starting up")
        return Step2Event(query = ev.query)

    @step
    async def step_two(self,ctx:Context,ev:Step2Event) -> Step3Event:
        print("Sending an email")
        return Step3Event(query = ev.query)

    @step
    async def step_three(self,ctx:Context,ev:Step3Event) -> StopEvent:
        print("Finishing up")
        return StopEvent(result = ev.query)


async def main():
    wf = MainWorkflow()
    result = await wf.run(query = "Initial query")
    print("Final result",result)

    # draw_all_possible_flows(MainWorkflow,filename = "streaming.html")

if __name__ == "__main__":
    asyncio.run(main())
```

We get:

```text
Starting up
Sending an email
Finishing up
Initial query
```

Now let’s subclass this workflow to send a text message as well:
```python
class Step2BEvent(Event):
    query: str

class CustomWorkflow(MainWorkflow):
    @step
    async def step_two(self, ev: Step2Event) -> Step2BEvent:
        print("Sending an email")
        return Step2BEvent(query=ev.query)

    @step
    async def step_two_b(self, ev: Step2BEvent) -> Step3Event:
        print("Also sending a text message")
        return Step3Event(query=ev.query)
```

Which will instead give us

```
Starting up
Sending an emai
lAlso sending a text message
Finishing up
Initial query
```

![[Pasted image 20251015234623.png]]
#### Resources

Resources are external dependencies such as memory, LLMs, query engines or chat history instances that will be injected into workflow steps at runtime.

Resources are a powerful way of binding workflow steps to Python objects that we otherwise would need to create by hand every time. For performance reasons, by default resources are cached for a workflow, meaning the same resource instance is passed to every step where it’s injected. It’s important to master this concept because cached and non-cached resources can lead to unexpected behaviour, let’s see it in detail.
```python
from llama_index.core.workflow.resource import Resource
from llama_index.core.workflow import (
    Event,
    step,
    StartEvent,
    StopEvent,
    Workflow,
)
```

`Resource` wraps a function or callable that must return an object of the same type as the one in the resource definition, let’s see an example:

```python
from typing import Annotated
from llama_index.core.memory import Memory


def get_memory(*args, **kwargs) -> Memory:
    return Memory.from_defaults("user_id_123", token_limit=60000)


resource = Annotated[Memory, Resource(get_memory)]
```

In the example above, `Annotated[Memory, Resource(get_memory)` defines a resource of type `Memory` that will be provided at runtime by the `get_memory()` function. A resource defined like this can be injected into a step by passing it as a method parameter:
```python
import random

from typing import Union
from llama_index.core.llms import ChatMessage

RANDOM_MESSAGES = [
    "Hello World!",
    "Python is awesome!",
    "Resources are great!",
]


class CustomStartEvent(StartEvent):
    message: str


class SecondEvent(Event):
    message: str


class ThirdEvent(Event):
    message: str


class WorkflowWithMemory(Workflow):
    @step
    async def first_step(
        self,
        ev: CustomStartEvent,
        memory: Annotated[Memory, Resource(get_memory)],
    ) -> SecondEvent:
        await memory.aput(
            ChatMessage.from_str(
                role="user", content="First step: " + ev.message
            )
        )
        return SecondEvent(message=RANDOM_MESSAGES[random.randint(0, 2)])

    @step
    async def second_step(
        self, ev: SecondEvent, memory: Annotated[Memory, Resource(get_memory)]
    ) -> Union[ThirdEvent, StopEvent]:
        await memory.aput(
            ChatMessage(role="assistant", content="Second step: " + ev.message)
        )
        if random.randint(0, 1) == 0:
            return ThirdEvent(message=RANDOM_MESSAGES[random.randint(0, 2)])
        else:
            messages = await memory.aget_all()
            return StopEvent(result=messages)

    @step
    async def third_step(
        self, ev: ThirdEvent, memory: Annotated[Memory, Resource(get_memory)]
    ) -> StopEvent:
        await memory.aput(
            ChatMessage(role="user", content="Third step: " + ev.message)
        )
        messages = await memory.aget_all()
        return StopEvent(result=messages)
```

As you can see, each step has access to the `memory` resource and can write to it. It’s important to note that `get_memory()` will be called only once, and the same memory instance will be injected into the different steps. We can see this is the case by running the workflow:

```python
wf = WorkflowWithMemory(disable_validation=True)

async def main():
    messages = await wf.run(
        start_event=CustomStartEvent(message="Happy birthday!")
    )
    for m in messages:
        print(m.blocks[0].text)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
```

A potential result for this might be:

```text
First step: Happy birthday!
Second step: Python is awesome!
Third step: Hello World!
```

This shows that each step added its message to a global memory, which is exactly what we were expecting!

Note that resources are preserved across steps of the same workflow instance, but not across different workflows. If we were to run two `WorkflowWithMemory` instances, `get_memory` would be called one time for each workflow and as a result their memories would be separate and independent:

```python
wf1 = WorkflowWithMemory(disable_validation=True)
wf2 = WorkflowWithMemory(disable_validation=True)


async def main():
    messages1 = await wf1.run(
        start_event=CustomStartEvent(message="Happy birthday!")
    )
    messages2 = await wf1.run(
        start_event=CustomStartEvent(message="Happy New Year!")
    )
    for m in messages1:
        print(m.blocks[0].text)
    print("===================")
    for m in messages2:
        print(m.blocks[0].text)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
```

This is a possible output:

```
First step: Happy birthday!
Second step: Resources are great!
===================
First step: Happy New Year!
Second step: Python is awesome!
```

## Disable resource caching

If we pass `cache=False` to `Resource` when defining a resource, the wrapped function is called every time the resource is injected into a step. This behaviour can be desirable at times, let’s see a simple example using a custom `Counter` class:
```python
class Counter(BaseModel):
    counter: int = Field(description="A simple counter",default = 0)

    async def increment(self) -> None:
        self.counter += 1

def get_counter() -> Counter:
    return Counter()

class SecondEvent(Event):
    count: int


class WorkflowWithCounter(Workflow):
    @step
    async def first_step(
        self,
        ev: StartEvent,
        counter: Annotated[Counter, Resource(get_counter, cache=False)],
    ) -> SecondEvent:
        await counter.increment()
        return SecondEvent(count=counter.counter)

    @step
    async def second_step(
        self,
        ev: SecondEvent,
        counter: Annotated[Counter, Resource(get_counter, cache=False)],
    ) -> StopEvent:
        print("Counter at first step: ", ev.count)
        await counter.increment()
        print("Counter at second step: ", counter.counter)
        return StopEvent(result="End of Workflow")
    
async def main():
    wf = WorkflowWithCounter(disable_validation = True)
    res = await wf.run()
    print(res)


if __name__ == "__main__":
    asyncio.run(main())
```

If we now run this workflow, we will get out:

```
Counter at first step:  1
Counter at second step:  1
```

## A note about stateful and stateless resources

As we have seen, cached resources are expected to be **stateful**, meaning that they can maintain their state across different workflow runs and different steps, unless otherwise specified. But this doesn’t mean we can consider a resource **stateless** only because we disable caching. Let’s see an example:

```python
global_mem = Memory.from_defaults("global_id", token_limit=60000)

def get_memory(*args, **kwargs) -> Memory:    
	return global_mem
```

If we disable caching with `Annotated[Memory, Resource(get_memory, cache=False)]`, the function `get_memory` is going to be called multiple times but the resource instance will be always the same. Such a resource should be considered stateful not regarding its caching behaviour.

#### Observability
Debugging is essential to any application development, and Workflows provide you a number of ways to do that.

## Visualization

The simplest form of debugging is visualization, which we’ve already used extensively in this tutorial. You can visualize your workflow at any time by running the following code:

```python
from llama_index.utils.workflow import draw_all_possible_flows

draw_all_possible_flows(MyWorkflow, filename="some_filename.html")
```

This will output an interactive visualization of your flow to `some_filename.html` that you can view in any browser.
![[Pasted image 20251016005516.png]]
## Verbose mode
When running any workflow you can always pass `verbose=True`. This will output the name of each step as it’s executed, and whether and which type of event it returns. Using the `ConcurrentWorkflow` from the previous stage of this tutorial:
```python
class ConcurrentFlow(Workflow):
    @step
    async def start(
        self, ctx: Context, ev: StartEvent
    ) -> StepAEvent | StepBEvent | StepCEvent:
        ctx.send_event(StepAEvent(query="Query 1"))
        ctx.send_event(StepBEvent(query="Query 2"))
        ctx.send_event(StepCEvent(query="Query 3"))

    @step
    async def step_a(self, ctx: Context, ev: StepAEvent) -> StepACompleteEvent:
        print("Doing something A-ish")
        return StepACompleteEvent(result=ev.query)

    @step
    async def step_b(self, ctx: Context, ev: StepBEvent) -> StepBCompleteEvent:
        print("Doing something B-ish")
        return StepBCompleteEvent(result=ev.query)

    @step
    async def step_c(self, ctx: Context, ev: StepCEvent) -> StepCCompleteEvent:
        print("Doing something C-ish")
        return StepCCompleteEvent(result=ev.query)

    @step
    async def step_three(
        self,
        ctx: Context,
        ev: StepACompleteEvent | StepBCompleteEvent | StepCCompleteEvent,
    ) -> StopEvent:
        print("Received event ", ev.result)

        # wait until we receive 3 events
        if (
            ctx.collect_events(
                ev,
                [StepCCompleteEvent, StepACompleteEvent, StepBCompleteEvent],
            )
            is None
        ):
            return None

        # do something with all 3 results together
        return StopEvent(result="Done")
```

You can run the workflow with verbose mode like this:

```python
w = ConcurrentFlow(timeout=10, verbose=True)
result = await w.run()
```

And you’ll see output like this:

```text
Running step start
Step start produced no event
Running step step_a
Doing something A-ish
Step step_a produced event StepACompleteEvent
Running step step_b
Doing something B-ish
Step step_b produced event StepBCompleteEvent
Running step step_c
Doing something C-ish
Step step_c produced event StepCCompleteEvent
Running step step_three
Received event  Query 1
Step step_three produced no event
Running step step_three
Received event  Query 2
Step step_three produced no event
Running step step_three
Received event  Query 3
Step step_three produced event StopEvent
```

## Visualizing most recent execution

If you’re running a workflow step by step, or you have just executed a workflow with branching, you can get the visualizer to draw only exactly which steps just executed using `draw_most_recent_execution`:

```python
from llama_index.utils.workflow import draw_most_recent_execution

draw_most_recent_execution(w, filename="last_execution.html")
```

Note that instead of passing the class name you are passing the instance of the workflow, `w`.

----
### Basic Workflow
```python
import os
import asyncio
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.llms.google_genai import GoogleGenAI
import os
from typing import Optional, List,Annotated
from datetime import datetime
from pydantic import BaseModel, Field
from llama_index.llms.groq import Groq
from llama_index.core import VectorStoreIndex, get_response_synthesizer, Settings
from llama_index.core.workflow import (
    StartEvent,
    StopEvent,
    Workflow,
    step,
    Event,
)
import json
from pydantic import ValidationError

# os.environ["GOOGLE_API_KEY"] = "AIzaSyD7uibWj-CX1j7ljL_jTI1ZkpRniROzk1o"

# llm = GoogleGenAI( # Use the new class name
#     model="models/gemini-2.0-flash",
#     api_key = os.getenv("GOOGLE_API_KEY")
# )

os.environ["GROQ_API_KEY"] = "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"
llm = Groq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))

Settings.llm = llm

class EmailResponse(BaseModel):
    response:str = Field(...,description = "The generated email response content")

class ParsedEmail(Event):
    sender: Optional[str]
    content: str
    subject: Optional[str]
    email_date: Optional[datetime]
    deadline: Optional[datetime]

class MyWorkflow(Workflow):
    @step
    async def parse_email(self, ev: StartEvent) -> ParsedEmail:
        """Parse structured info from raw email text."""
        prompt = f"""
        Extract the following structured data from the email below:
        - sender
        - subject
        - content
        - email_date
        - deadline (if any mentioned)

        Email:
        {ev.email_text}

        Return the result as a **valid JSON** following this schema:
        {ParsedEmail.model_json_schema()}
        """

        result = await llm.acomplete(prompt)
        text_output = result.text.strip()

        try:
            json_start = text_output.find("{")
            json_end = text_output.rfind("}") + 1
            json_str = text_output[json_start:json_end]
            data = json.loads(json_str)
            return ParsedEmail(**data)
        except (json.JSONDecodeError, ValidationError) as e:
            print("⚠️ JSON parsing failed.\nRaw output:\n", text_output)
            print("Error:", e)
            return ParsedEmail(
                sender=None,
                subject=None,
                content=text_output,
                email_date=None,
                deadline=None,
            )

    @step
    async def step_2(self, ev: ParsedEmail) -> StopEvent:
        """Print parsed email info."""
        print("\n✅ Parsed Email:")
        print("Sender:", ev.sender)
        print("Subject:", ev.subject)
        print("Content:", ev.content)
        print("Email Date:", ev.email_date)
        print("Deadline:", ev.deadline)
        return StopEvent(result="Workflow completed.")


# ──────────────────────────────
# Runner
# ──────────────────────────────
async def main():
    email_text = """
    From: Sarah Collins <sarah.collins@techwave.ai>
    To: Ahmed Elkassrawy <ahmed.elkassrawy@example.com>
    Subject: Project Update and Upcoming Submission Deadline
    Date: October 15, 2025, 10:42 AM

    Hi Ahmed,

    I hope you’re doing well. I wanted to check in regarding the AI Agent Research Report you’ve been preparing. 
    As discussed in our last meeting, we’re aiming to include your section on Retrieval-Augmented Generation (RAG) 
    pipelines in the final document.

    Please make sure to:

    - Submit your completed draft to the shared Google Drive folder.
    - Review the integration notes I sent last week.

    The final deadline is October 20, 2025 (EOD), so we can compile all contributions before our internal review.

    Let me know if you need any additional resources or time extensions.

    Best regards,
    Sarah Collins
    Project Manager – TechWave AI
    📞 +1 (415) 555-2083
    ✉️ sarah.collins@techwave.ai
    """

    wf = MyWorkflow()
    result = await wf.run(email_text=email_text)
    print("\n🏁 Final result:", result)


if __name__ == "__main__":
    asyncio.run(main())
```