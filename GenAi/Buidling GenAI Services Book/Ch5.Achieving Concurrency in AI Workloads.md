---
tags: [genai, fastapi, async, concurrency, llm-serving]
source: "Building Generative AI Services with FastAPI — Chapter 5"
related: "[[Code Patterns Worth Stealing]]"
---

## What this chapter covers

- Why async programming boosts performance and scalability.
- How to handle many users at once, and how to talk to external systems like databases.
- How to deal with I/O-bound vs CPU-bound operations.
- How FastAPI uses its event loop to run background tasks.

---

## Optimizing GenAI services for multiple users

Your service has to serve requests **concurrently**: several overlapping tasks running at the same time instead of one after the other.

> [!definition] Blocking operation
> A long-running task that halts the program until it finishes. There are two kinds:
> - **I/O-bound**: waiting on something outside the CPU (network, disk, database).
> - **Compute-bound**: waiting because the CPU/GPU is busy with heavy computation (e.g., model inference).

There are three strategies for serving many users:

| Strategy | Solves |
|---|---|
| System optimization | I/O-bound tasks |
| Model optimization | Model loading and inference |
| Queueing system | Long-running inference, so users don't wait on a response |

The chapter builds three features to practice these:

1. **A web scraper**: fetches and parses URLs pasted in the chat, so you can ask the LLM about web pages.
2. **A RAG module**: uses a self-hosted vector database (Qdrant) so you can upload documents and talk to them.
3. **A batch image generator**: runs image generation as background tasks.

### Concurrency vs parallelism

> [!definition] Concurrency
> A service's ability to handle multiple requests or tasks at the same time, **without finishing one before starting the next**. Task timelines overlap; they can start and end at different times.

On a **single CPU core**, you get concurrency by:

- switching between tasks on **one thread** (async programming), or
- switching across **several threads** (multithreading).

> [!definition] Time slicing
> The scheduling trick used by both multithreading and async: the CPU gives each task a small slice of time in turn, which creates the illusion that they run at the same time.

> [!definition] GIL (Global Interpreter Lock)
> A lock in Python that lets only **one thread** control the interpreter at any moment. So only one thread is actually executing at a time.

The GIL was added to keep Python simpler and to favor single-threaded performance. The cost is that **true parallel threads inside one Python process are impossible**.

That's fine for I/O. When a task waits on I/O, the CPU switches to another task. The paused task saves its state and resumes when the I/O finishes.

> [!definition] Parallelism
> A subset of concurrency that needs **multiple cores**. Tasks are split among workers, each running at the same time in its own process with its own resources.

The two are related but not the same:

- **Concurrency** interleaves tasks. Best for **I/O-bound** work.
- **Parallelism** runs tasks at the same time on multiple cores. Best for **CPU-bound** work.

![[Pasted image 20261001171207.png]]

- **No concurrency (synchronous)**: one process on one core runs tasks in order.
- **Concurrent, not parallel**: multiple threads in one process (on one core) take turns, because of the GIL.
- **Concurrent and parallel**: multiple processes on multiple cores run tasks truly in parallel, making full use of a multicore CPU.

![[Pasted image 20261001171347.png]]

### Multiprocessing trade-offs

In multiprocessing, each process has **its own memory and resources** and works in isolation.

- **Upside:** more stable. One process crashing doesn't take down the others.
- **Downside:** communication between processes is harder than between threads.

Multithreading and async cut waiting time on I/O because the CPU does other work while it waits. They **don't help with heavy computation**.

> [!warning] "Just run more FastAPI workers" doesn't work for models
> Your first instinct with a slow model might be to start several copies of your FastAPI service. But separate worker processes **don't share memory**, so each one loads its **own copy of the model**. That eats your hardware fast.
>
> The real fix isn't parallelism on its own. It's **external model serving**: run the model in its own server and call it.

> [!note]
> The only time AI inference counts as **I/O-bound** instead of CPU-bound is when you call a **third-party API**. The heavy compute happens on their side.

### The four execution models

| Model | How it works | Watch out for |
|---|---|---|
| **Sync** | One CPU core, one thread | Long waits on any I/O or CPU blocking |
| **Async** | Multitasking managed by an event loop | Gets the most out of one core |
| **Multithreading** | One core, many threads in the same process; threads share data and resources | Deadlocks (threads blocking each other), race conditions on shared data |
| **Multiprocessing** | Many processes, one CPU core each | Harder communication between processes |

---

## Optimizing I/O tasks with async programming

The goal here: use async so I/O-bound work doesn't block the main server process during AI workloads.

**Sync** means tasks run in order, each waiting for the previous one. If you want concurrency, and want to get the most out of each core without blocking, use **async**.

### Sync example

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

Takes **15 seconds** (3 × 5).

### Async example

```python
import time
import asyncio

async def task():
    print("Start of async task")
    await asyncio.sleep(5)
    print("Task resumed after 5 secs")

async def spawn_tasks():
    await asyncio.gather(task(), task(), task())

start = time.time()

asyncio.run(spawn_tasks())

duration = time.time() - start
print(f"Process completed in: {duration} seconds")
```

Takes only **5 seconds**:

- `task()` was called three times **concurrently**.
- The functions ran inside asyncio's **event loop**, which kept things moving instead of waiting.

### Deep dive into asyncio

> [!definition] Event loop
> The core object of asyncio. It handles I/O and system events. Think of it as a `while True` loop that watches for events from coroutines in the Python process and switches between them whenever one is waiting on I/O.

![[Pasted image 20261001175229.png]]

> [!definition] Coroutine function
> A special function (`async def`) that can **pause** its execution, save its state, and **resume** later from where it left off.

### Why self-hosted models block the server

In the earlier chapters, you noticed long waits before each request was processed. That's because the model was loaded and running **in the same Python process and CPU core as the server**.

When the first request arrives, the whole server blocks until inference finishes. Inference pushes the CPU to its limit, so it's a **CPU-bound blocking operation**. It doesn't have to be.

When you use a **provider's API**, the CPU-bound work moves to the provider and becomes **I/O-bound** for you. That's why it pays to know how to call the provider's API concurrently with async.

> [!warning] Rate limits
> Concurrent requests to external APIs need to be **throttled** to stay within the provider's rate limits.

### Event loop and thread pool in FastAPI

FastAPI handles both async and sync code. It runs **sync handlers in a thread pool**, so their blocking operations don't stop the event loop.

- At **startup**, FastAPI creates a pool of threads up front, so it doesn't pay the cost of creating threads during requests.
- It then hands **background tasks and sync workloads** to that pool, so they can't block the event loop.
- The **event loop** orchestrates the async processing of requests.

> [!tip] More from this part of the chapter
> The pages on blocking the main server, the web scraper, and RAG are mostly code. Their reusable patterns live in [[Code Patterns Worth Stealing]].

---

## Model optimization techniques

Model **compression** techniques that improve inference performance:

- **Quantization**: compress the model.
- **Pruning**: trim the model's parameters.
- **Distillation**
- **Fine-tuning small models**

If you're serving a **transformer-based** model, you can optimize inference further with:

- **Fast attention**: speeds up attention-map calculations on GPUs.
- **KV caching**
- **Paged attention**: optimizes KV-cache memory use after the attention computation.
- **Request batching**: static and continuous batching, to maximize GPU use.

> [!definition] Latency
> Time from sending a request to the model until the **first response** arrives. Measured in seconds of delay.

> [!definition] Throughput
> How many requests the LLM can process in a given time. Shows the server's capacity. Measured in **tokens per minute (TPM)**.

vLLM combines these: quantization-style compression, continuous batching, paged attention, memory sharing to shrink the GPU footprint, and streaming outputs. The result is lower latency and higher throughput.

### How LLMs generate: autoregressive prediction

LLMs predict the next token **autoregressively**.

![[Pasted image 20261001190834.png]]

- The LLM runs **several inference iterations in a loop**. Each iteration produces **one output token**.
- Each new token is appended to the input, and the longer sequence goes back into the model for the next step.
- The loop stops when the model produces an **end-of-sequence (stop) token** or hits the **maximum sequence length**.

For every token in the sequence, the LLM has to compute **attention maps**. GPUs can compute these in parallel for each iteration. But attention maps (which capture each token's meaning and context) are **expensive**.

> [!definition] KV caching
> Saving the already-computed attention **keys and values** in GPU memory so they're reused on the next iteration instead of recalculated. It's the model's working memory during generation.

### The GPU memory problem

Keeping that cache on the GPU eats a lot of memory:

- A **13B-parameter model** uses almost **1 MB of state per token**, on top of its 13B parameters.
- On an **A100 with 40 GB**, the parameters take about **26 GB**, leaving room for only about **14K tokens** at once.
- So GPU memory use grows with **model size + sequence length**.

Serving several users at once makes it worse. The batch **shares** that memory, so you have to trade off:

- **Longer context window** → fewer concurrent users.
- **More concurrent users** → shorter context window.

> [!example]
> With a sequence length of **2048**, the batch is capped at **7 concurrent requests**. That's an upper bound. It leaves no room for intermediate computations, so the real number is lower.

**Bottom line:** LLMs **underuse the GPU**. Much of the GPU's memory bandwidth goes to **loading model parameters** instead of processing inputs.

Two fixes:

1. **Use the most efficient model that does the job.** Smaller, compressed models often perform about as well as their bigger versions.
2. **Batch requests.** The model processes several inputs as a group, so the cost of loading parameters is shared. You get better bandwidth use, higher compute use, higher throughput, and cheaper inference.

vLLM uses **batching + fast attention + KV caching + paged attention** to maximize throughput. (Figure 5-14 in the book compares latency and throughput with and without batching.)

### Static vs continuous batching

| | Static batching | Dynamic / continuous batching |
|---|---|---|
| Batch size | Fixed | Set by demand: request lengths and free GPU memory |
| When it starts | Waits for a set number of requests | Requests keep flowing in |
| When a request finishes | It waits for the **whole batch** to finish | A **new request takes its slot** right away |
| GPU use | Low: short sequences leave idle GPU time | High: GPU stays saturated |

**Why static batching hurts:**

- Every response is delayed until the whole batch is done, so **latency goes up**.
- Freeing GPU resources mid-batch is tricky, because sequences finish at different times.
- Chat users don't send fixed-length prompts or expect fixed-length answers. That variation causes **massive GPU underuse**. In the book's Figure 5-15, only one sequence keeps the GPU busy for the whole batch; the rest is idle "white blocks".

**Continuous batching** drops the fixed-length assumption. While the model parameters stay loaded, the server keeps **inserting new requests into the batch** as old ones complete. The result is higher throughput and lower latency (Figure 5-16).

> [!tip]
> You don't have to build this yourself. **vLLM's server ships continuous batching out of the box**, plus paged attention, which sets it apart from other inference frameworks.

### Paged attention

Fast inference depends on the KV cache, and the KV cache grows as input sequences get longer. For a 13B model it can reach **40 GB**, which is hard to store and access on limited hardware.

> [!definition] Paged attention
> A way to cut the KV cache's memory needs by splitting it into small, fixed-size chunks called **pages**. Each page holds the KV vectors for a set number of tokens.

It works like **virtual memory in an operating system**: the *logical* layout of data is separate from where it *physically* lives. A **block table** maps logical blocks to physical ones, so memory is allocated on the fly as new tokens arrive. That avoids **memory fragmentation**.

The four steps:

1. **Partition the KV cache** into fixed-size pages, each holding part of the key-value pairs.
2. **Build a lookup table** that maps keys to their pages, for fast allocation and retrieval.
3. **Load selectively**: only the pages the current sequence needs are loaded, which shrinks the memory footprint.
4. **Compute attention** using the key-value pairs from the loaded pages.

This is how vLLM gets the most out of GPU memory, and it makes LLMs usable on more modest hardware.

> [!success] Measured impact
> An Anyscale benchmark of LLM-serving frameworks found that paged attention + continuous batching let vLLM cut **latency by about 4×** and raise **throughput by up to 23×**.

---

## Managing long-running AI inference tasks

Once your models run in a separate process outside FastAPI's event loop, the remaining problem is tasks that simply **take a long time**.

Some models, like **Stable Diffusion XL**, can take **minutes** even on a GPU.

- If many users hit one model at once, the server has to **queue** their requests.
- Generative work is iterative: users send several requests to steer the model toward what they want.
- So a **big backlog** builds up, and users at the back wait a long time before seeing anything.

> [!definition] Background tasks (FastAPI)
> A FastAPI feature that lets you **respond to the user immediately** and keep processing the request after the response is sent. You already used it in the RAG module to fill the vector database from uploaded PDFs.

Users can keep working instead of waiting. To get the results back to them, you can:

- **Save results** to disk or a database for later retrieval.
- Offer a **polling** endpoint the client pings for updates.
- Open a **live connection**, so the UI updates as soon as results are ready.

### Example 5-18: batch image generation in the background

```python
# main.py
from fastapi import BackgroundTasks
import aiofiles

...

async def batch_generate_image(prompt: str, count: int) -> None:
    images = generate_images(prompt, count)
    for i, image in enumerate(images):
        async with aiofiles.open(f"output_{i}.png", mode="wb") as f:
            await f.write(image)

@app.get("/generate/image/background")
def serve_image_model_background_controller(
    background_tasks: BackgroundTasks, prompt: str, count: int
):
    background_tasks.add_task(batch_generate_image, prompt, count)
    return {"message": "Task is being processed in the background"}
```

- `generate_images` calls an **external model-serving API** (like Ray Serve) to make a batch of images.
- Each image is saved with **aiofiles**, so file writes don't block. In production, save to cloud storage that clients fetch from directly.
- The handler takes a `BackgroundTasks` parameter and passes it the function and its arguments with `add_task`.
- It returns a generic message **right away**, so the user doesn't wait.

You can queue several background tasks, like generating image batches and sending notification emails. They run **one after another** without blocking the user. Then add an endpoint where clients can **poll** for status and fetch the results.

> [!warning] Background tasks are not parallelism
> - They run on the **same event loop**. You get concurrency, not true parallelism.
> - **Heavy CPU-bound work** (like AI inference) inside a background task **blocks the event loop** until it finishes.
> - Async background tasks that don't `await` their blocking I/O also **block the main server**, even though they run "in the background".
> - FastAPI runs **non-async** background tasks in its internal **thread pool**.

> [!note] When to outgrow background tasks
> They're great for simple batch jobs, but they **don't scale** and are weak at **error handling and retries**.
> - Model-serving frameworks like **Ray Serve, BentoML, and vLLM** handle serving at scale better, e.g. with request batching.
> - For a robust inference pipeline, combine **Celery** (task queue), **Redis** (cache), and **RabbitMQ** (message broker).

---

## Summary

- **Concurrency vs parallelism**, and the blocking operations that stop you from serving users at the same time.
- **Multithreading, multiprocessing, and async**: how they differ, and when each one fits.
- **Thread pool and event loop in FastAPI**: how they serve requests concurrently, and how a wrongly declared handler can block the server.
- **Async for I/O**: hands-on with web content and databases by building a **web scraper** and a **RAG module**.
- **Memory-bound blocking**: why large models are memory-hungry, and how **continuous batching** and **paged attention** reduce those bottlenecks.
- **Long-running inference**: keeping the service responsive with background tasks.

**Next chapter:** streaming with **server-sent events (SSE)** and **WebSockets**, so users see results in near real time.
---

Reusable code from this chapter: [[Code Patterns Worth Stealing]]
