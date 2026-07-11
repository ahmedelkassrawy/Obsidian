AI workloads are computationally expensive. In production, services must handle simultaneous requests from multiple users. However, GenAI models and external system interactions (databases, filesystems, internet) introduce operations that block program execution.

## Blocking Operations

Blocking operations generally fall into two categories:

1. **Input/Output (I/O) Bound:**
* **Definition:** The process waits for data input/output operations.
* **Sources:** User input, reading/writing files to disk, network requests, API calls, database transactions.
* **Status:** The CPU is often idle while waiting for the external system to respond.

2. **Compute Bound:**
* **Definition:** The process waits for intensive calculations to complete.
* **Sources:** AI model inference/training, data processing, 3D rendering, simulations.
* **Status:** CPU or GPU cores are pushed to their limits, preventing other tasks from running.

## Strategies for Serving Multiple Users

To handle concurrent users effectively, three primary strategies are used:

* **System Optimization:** Best for **I/O-bound** tasks (fetching data, network requests).
* **Model Optimization:** Best for **memory- and compute-bound** tasks (model loading, inference).
* **Queuing Systems:** Best for managing long-running inference tasks to prevent response delays.

---
## Concurrency vs. Parallelism

Understanding the difference between these two concepts is critical for selecting the right architecture.

### Concurrency

Concurrency is the ability of a service to handle multiple tasks at the same time by interleaving their execution. Tasks may overlap, starting and ending at different times, but they are not necessarily executing at the exact same nanosecond.

* **Mechanism:** Time Slicing. The CPU switches between tasks (context switching) to give the illusion of simultaneous execution.
* **Python Context:** In Python, the **Global Interpreter Lock (GIL)** allows only one thread to control the Python interpreter at a time. Therefore, single-core concurrency involves the CPU quickly switching tasks whenever one task is paused (e.g., waiting for I/O).

### Parallelism

Parallelism involves executing multiple tasks simultaneously, typically across multiple CPU cores.

* **Mechanism:** Tasks are split among independent workers (multiprocessing).
* **Resource Usage:** Each worker runs in its own process with isolated resources.

### Python Execution Models

| Model | Description | Hardware Usage |
| --- | --- | --- |
| **No Concurrency (Synchronous)** | A single process executes tasks sequentially. | Single Core |
| **Concurrent & Non-Parallel** | Multiple threads in a single process handle tasks concurrently. Limited by GIL. | Single Core |
| **Concurrent & Parallel** | Multiple processes perform tasks in parallel. | Multiple Cores |

---

## Comparison of Concurrency Strategies

| Strategy | Features | Challenges | Use Cases |
| --- | --- | --- | --- |
| **No Concurrency (Synchronous)** | Simple, readable, easy to debug. Single CPU core/thread. | **Long wait times.** A blocking operation halts the entire process. Cannot serve multiple users simultaneously. | Scripts or applications where waiting is acceptable. |
| **Async IO (Asynchronous)** | Single CPU core/thread. Multitasking managed by an **event loop**. Maximizes CPU utilization. | Harder to implement and debug. Requires async-compatible libraries. Blocking the event loop freezes the app. | Applications with heavy I/O blocking (APIs, DBs). |
| **Multithreading** | Single CPU core, multiple threads within one process. Threads share memory/resources. | **Race conditions, deadlocks, and starvation.** Thread safety is difficult to manage. Creating threads is computationally expensive. | Services needing blocking I/O but shared memory. |
| **Multiprocessing** | Multiple processes on several CPU cores. Isolated resources. True parallelism. | **Complex data sharing.** High memory overhead (cannot easily share loaded AI models). Inter-process communication is complex. | CPU-bound tasks (heavy computation). |

---
## Asynchronous Programming for I/O Optimization

Asynchronous programming allows a program to initiate a task and move on to another task before the first one finishes. This is particularly effective for I/O-bound operations.

### Performance Statistics: Sync vs. Async

In a benchmark comparing synchronous execution against asynchronous execution using `time.sleep()` to simulate a 5-second I/O block repeated 3 times:

* **Synchronous Execution:** Took **15.01 seconds**. The process waited sequentially (5s + 5s + 5s).
* **Asynchronous Execution:** Took **5.00 seconds**. The tasks ran concurrently, reducing the total time by approximately **66%**.

### How `asyncio` Works
Python uses the `asyncio` package (introduced in Python 3.5) to manage concurrency.

* **Keywords:** `async` defines a coroutine; `await` pauses execution until the awaited task is done, yielding control back to the loop.
* **The Event Loop:** A central execution construct that watches for events and switches between functions. When a function hits a blocking I/O operation (flagged by `await`), the event loop pauses it and runs another function until the I/O is complete.
* **Coroutines:** Specialized functions that can be paused and resumed without losing their state.

### Optimization for GenAI Workloads

* **Self-Hosted Models:** Running a large model (inference) is **Compute-Bound**. Using standard FastAPI multiprocessing is inefficient because you cannot share the loaded model in memory across processes (RAM usage explodes). **Solution:** Use specialized inference servers (vLLM, Ray Serve, NVIDIA Triton) to handle the compute, while your web server handles the requests.
* **Third-Party APIs:** When using APIs (like OpenAI), the workload becomes **I/O-Bound**. The heavy compute happens on the provider's servers. **Solution:** Use Async IO to handle thousands of concurrent API requests without blocking your server.

**Note on Rate Limits:** When scaling async requests to external APIs, services must implement **exponential backoff**. If rate-limit errors occur, the service should wait for increasing durations before retrying.

---
## FastAPI Concurrency Implementation

FastAPI uses the ASGI (Asynchronous Server Gateway Interface) standard to handle concurrency.

### The Two Execution Modes

1. **Thread Pool (Synchronous):** If a route is defined with standard `def`, FastAPI runs it in a separate thread from a thread pool. This prevents blocking I/O in that route from freezing the main server, but it has the overhead of thread management.
2. **Event Loop (Asynchronous):** If a route is defined with `async def`, FastAPI runs it directly on the main event loop. This is highly efficient for I/O tasks.

### The "Blocking" Pitfall

A critical error in FastAPI development is defining a route with `async def` but including synchronous blocking code (e.g., a standard `time.sleep` or a synchronous API client) inside it.

* **Result:** Because the function is marked `async`, FastAPI does not send it to the thread pool. The blocking operation stops the **entire event loop**.
* **Consequence:** The server freezes and cannot process *any* other requests until that single operation completes.

**Rule of Thumb:** Only use `async def` if you are `await`-ing truly asynchronous libraries (like `AsyncOpenAI` or `aiohttp`). If you must use a synchronous library, define the route with standard `def`.

![[Pasted image 20260122223314.png]]
![[Pasted image 20260122223337.png]]

![[Pasted image 20260122223349.png]]

![[Pasted image 20260122223406.png]]

![[Pasted image 20260122223424.png]]