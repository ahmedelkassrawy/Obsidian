- For role and benefits async programming in boosting perf and scalability.
- Learning to manage concurrent user interactions and interface with external sys such as DB
- How to deal with I/O , CPU bound operations

FastAPI event loop for background tasks execution

## Optimizing GenAI services for multiple users
services will be expected to serve requests concurrently such that nultiple overlapping tasks can be executed

Long running tasks that can halt the program are called `blocking`

These Blocking operations can be:
- I/O Bound
- Compute Bound (where a process has to wait because of compute intensive operation on CPU/GPU)

How to serve multiple users:
- System Optimization -> For I/O bound tasks
- Model Optimization -> For model loading and inference
- Queueing System -> for handling long running inference tasks to avoid delays in responding

We will add features to ensure these strategies
- Building a web page scraper for bulk fetching and parsing of HTTP URLs pasted in the chat, so that you can ask your LLM about the content of web pages 

- Adding a retrieval augmented generation (RAG) module to your service with a self-hosted vector database such as qdrant so that you can upload and talk to your documents via your LLM service 

- Adding a batch image generation system so that you can run image generation workloads as background tasks

Concurrency ->  ability of a service in handling multiple requests or tasks at the same time , WITHOUT COMPLETING ONE AFTER THE OTHER

During the concurrent operations , the timeline of multiple tasks can overlap and may start and end at diff times

Implement concurrency with a single CPU core by:
- switching between tasks on a single thread (via asynchronous programming) 
or 
- across different threads (via multithreading)

Time slicing -> scheduling mechanism in multithreading and async where a process allocates CPU time between tasks to give the illusion of concurrent solutions

In python , the CPU time can be allocated ton only 1 task at any moment because of GIL (Global Interperter Lock)

Python GIL allows only 1 thread (execution flow in python process) to control the python interperter for executin code

This means that only one thread can be in state of execution at any point in time 

GIL was implemented to simplify Python dev, and pritorize the perf of single threaded programs

However, the addition of the GIL to Python also means that true parallel execution of threads in a single Python process is not possible. When a task is waiting for an I/O operation to finish, the CPU can quickly switch to another task to avoid blocking other operations. The paused tasks save their state and can resume once the I/O operations are done.

With multiple cores , we can implement subset of concurrency called parallelism, where tasks are split among several workers, with each executing tasks simultaneously on their isolated resources and separate processes

Concurrency and parallelism have similarities , they arent execatly the same concept

Concurrency can help you manage multiple tasks by interleaving their execution , useful for I/O bounds

Parallelism is involving executing multiple tasks typically on multi core machines , useful for CPU bounds

![[Pasted image 20261001171207.png]]

No concurrency (synchronous) 
	A single process (on one core) executes tasks sequentially.
	
 Concurrent and non-parallel 
	 Multiple threads in a single process (on a core) handle tasks concurrently but not in parallel due to Python’s GIL. 
	 
 Concurrent and parallel 
	 Multiple processes on multiple cores perform the tasks in parallel, making the most of multicore processors for maximum efficiency.

![[Pasted image 20261001171347.png]]

In multiprocesing , each process has access to its own memory space and resources to complete a task in isolation from other processes

this isolation can make process more stable , it wont affect others but makes inter-process communication more complex compared to threads

multi threading and async reduce wait time in I/O tasks because the processor can do other work while wainting for I/O

Howeveer that doesnt help with tasks that require heavy computation

The first idea when working with slow models may be to adopt parallelism by creating multiple instansts of your fastapi service

Unforuaontly multiple workers running in seperate process will not ahve access to a shared memory space.Sadly, a new instance of your model will also need to be loaded, which will significantly eat up your hardware resources.

The solution is not parallelism on its own, but to adopt the external model-serving strategy

The only isntrance where you can treat AI inference as I/O bound instead of CPU Bound is when relying on third party API

Sync -> a single CPU core and thread 
	Long waiting times depending on I/O or CPU blocking operations

Async -> multitasking managed by event loop , max CPU utilization rate 

Multi threading -> Single CPU core but multiple threads within same process
	Threads share the same data and resources
	Threads can block each other (deadlocks)
	Concurrent access to resources can cause race conditions

Multiprocessing -> Multiple processes running on several CPU cores
	Each process allocated a CPU core

## Optimizing for I/O Tasks with Asynchronous Programming
the use of asynchronous programming to prevent blocking the main server process with I/O-bound tasks during AI workloads.

Sync is when tasks are performed in a sequential order with each task waiting for the previous one

if you need concurrency and want effiency of your services to be maximized on each core and not block operations so we use Async

Sync exmaple
```python
import time

def task():
    print("Start of sync task")

    time.sleep(5)

    print("After 5 sec of sleep")

start = time.time()

for i in range(3):
    task()

duration = time.time() - start
print(f"Total time taken for 3 tasks: {duration} seconds")
```

15 secs = 3 * 5

Async
```python
import time
import asyncio 

async def task():
    print("Start of async task")
    await asyncio.sleep(5)
    print("Task resumed after 5 secs")

async def spawn_tasks():
    await asyncio.gather(
        task(),task(),task()
    )

start = time.time()

asyncio.run(spawn_tasks())

duration = time.time() - start
print(f"Prcoess completed in: {duration} seconds")
```
5 secs only

- task() function was concurrently called three times
- The async function ran inside the asyncio ’s event loop, which was responsible for executing the code without waiting

Deep DIve into ASyncio
at the heart of asyncio lies a first class object called an event loop -> responsible for handling of I/O events or sys events

![[Pasted image 20261001175229.png]]

the event loop can be compared to a while True loop that watches for events or messages emitted by coroutine functions in python process and dispatch events to switch between functions while waiting for I/O blocking 

Coroutine function -> special type of function that can pause its execution , save its sate and resume later from where it left off

you will notice long waiting times before each request is processed. This is because you were preloading and hosting the model in the same Python process and CPU core that the server is running on. When you send the first request, the whole server becomes blocked while the inference workload is complete. Since during inference the CPU is working as hard as it can, the inference/generation process is a CPU-bound blocking operation. However, it doesn’t have to be. 

When you use a provider’s API, you no longer have CPU-bound AI workloads to worry about since they become I/O-bound for you, and you offload the CPU-bound workloads to the provider. Therefore, it makes sense to know how to leverage async programming to concurrently interact with the model provider’s API

Managing rate limites becuase concurrent requests to external APIs will need to be throttled 

### Event loop and Thread pool
FastAPI can handle async and sync , it does this by running sync handlers in its thread pool so that blocking operations dont stop the event loop from executing tasks

FastAPI setups thread pool by instiating collection of threads at startup to reduce the runtime -> it then delegates background tasks and sync workloads to prevent event loop being blocked by any blocking operations

Event loop responsible for orchestrating the async processing of requests