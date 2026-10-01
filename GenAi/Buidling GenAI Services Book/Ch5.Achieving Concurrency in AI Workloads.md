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

