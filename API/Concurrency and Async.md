1. **Synchronous vs. Asynchronous Execution**:
    - **Synchronous (Sync)**: Code that runs sequentially and blocks the thread until complete (e.g., execute method). Useful for simple scripts or when called from non-async code.
    - **Asynchronous (Async)**: Uses Python's asyncio library for concurrency. Allows multiple tasks (e.g., scraping multiple URLs) to run "in parallel" without blocking, using an **event loop** (a scheduler that manages coroutines). This is ideal for I/O-bound tasks like web scraping, where waiting for HTTP responses is the bottleneck.
        - **Coroutine**: A special async function (defined with async def) that can be paused and resumed. It returns a coroutine object, which must be "awaited" or scheduled to run.
        - **Event Loop**: The "heart" of asyncio. It runs coroutines concurrently by switching between them when one is waiting (e.g., for a network response). You get it with asyncio.get_event_loop() or asyncio.get_running_loop().
        - **await**: Pauses execution of the current coroutine until the awaited one completes.
        - **asyncio.run()**: Starts a new event loop and runs a coroutine to completion (for top-level sync calls).
        - **loop.run_until_complete()**: Runs a coroutine in an existing loop until it finishes.
        - **asyncio.ensure_future()**: Schedules a coroutine to run in the current loop without blocking (returns a Future object, which is like a promise of a result).
        - **Future**: A placeholder for a result that will be available later. asyncio.iscoroutine() checks if something is a pending coroutine.

```python
def execute(self, input_data: List[SearchResult],
            context: Optional[Dict[str,Any]] = None) -> List[ScrapedContent]:
    self.logger.info(f"Starting web scraping for {len(input_data)} URLs")

    try:
        loop = asyncio.get_running_loop()
        if loop.is_running():
            scraped_results = asyncio.ensure_future(
                self.ascrape_all(input_data)
            )
        else:
            scraped_results = loop.run_until_complete(
                self.ascrape_all(input_data)
            )
    except RuntimeError:
        scraped_results = asyncio.run(
            self.ascrape_all(input_data)
        )
```

**Async Detection Logic**:
- asyncio.get_running_loop(): Gets the current event loop if one is already running (e.g., in an async web server like FastAPI).
    - If running (loop.is_running()): Use asyncio.ensure_future(self.ascrape_all(input_data)) to schedule the coroutine (ascrape_all) as a Future in the existing loop. This doesn't block; the caller must await it later.
    - If not running but a loop exists: Use loop.run_until_complete(...) to run the coroutine synchronously in that loop until it finishes.
- If no loop exists (raises RuntimeError, e.g., in a plain sync script): Use asyncio.run(...) to create a new loop, run the coroutine, and close it. This is the simplest way to run async code from sync.

```python
    if not asyncio.iscoroutine(scraped_results):
        #if its not a coroutine, it means it was run to completion
        successful_scrapes = sum(1 for r in scraped_results if r.success)
        failed_scrapes = len(scraped_results) - successful_scrapes

        self.logger.info(f"Completed web scraping. Successful: {successful_scrapes}, Failed: {failed_scrapes}")
        return scraped_results
    else:
        #if its a coroutine it means it needs to be awaited by the caller
        ## If it is a coroutine, it needs to be awaited by the caller
        # This path is taken when called from an async context that awaits the result of `run`
        # which in turn calls this `execute` method.
        # To make this work synchronously, we must run the loop.
        loop = asyncio.get_event_loop()
        final_results = loop.run_until_complete(scraped_results)

        successful_scrapes = sum(1 for r in final_results if r.success)
        failed_scrapes = len(final_results) - successful_scrapes

        self.logger.info(f"Completed web scraping. Successful: {successful_scrapes}, Failed: {failed_scrapes}")
        return final_results
```

- - asyncio.iscoroutine(scraped_results): Checks if the result is still a pending coroutine (from ensure_future).
        - If not (already run): It's the final list of ScrapedContent. Count successes (using sum with generator expression) and log.
        - If yes (pending): Get the loop with asyncio.get_event_loop() (fallback if get_running_loop failed earlier) and run it with run_until_complete to get the results synchronously. Then log and return.
- This ensures execute always returns the completed results, even if called from mixed sync/async environments. The comments explain the rationale for async contexts.

# Asynchronous Code in Python

## Overview

Modern Python supports **asynchronous code** using **coroutines** with `async` and `await` syntax, ideal for I/O-bound tasks like web APIs. This enables **concurrency** (not to be confused with **parallelism**) for efficient handling of tasks that involve waiting.

### Key Takeaways
- **Asynchronous Code**: Allows programs to handle waiting tasks (e.g., network I/O) without blocking, switching to other work.
- **Concurrency**: Tasks progress "together" by switching during waits (single-threaded).
- **Parallelism**: Tasks run simultaneously on multiple processors (multi-threaded or multi-process).
- **FastAPI**: Leverages async for high performance, comparable to Node.js and Go, with optional parallelism for CPU-bound tasks.

## Asynchronous Code
- **Definition**: Code that tells the program to wait for slow operations (e.g., network, disk, database) while doing other tasks.
- **I/O-Bound Tasks**: Operations dominated by waiting (e.g., HTTP requests, database queries). Async shines here.
- **Synchronous vs. Asynchronous**:
    - **Synchronous (Sequential)**: Waits for each task to finish before moving to the next, blocking the thread.
    - **Asynchronous**: Pauses tasks during waits, allowing other tasks to run, then resumes when ready.
- **Why Async?**: Avoids wasting CPU time during I/O waits, improving efficiency for web apps with many users.

### Example Scenario

- **Synchronous**: Waiting in line at a bank, doing nothing until your turn.
- **Asynchronous**: Ordering burgers, then chatting with your crush while waiting, checking periodically for your order.

## `async` and `await` Syntax

- **Purpose**: Simplifies asynchronous code, making it look sequential while handling concurrency under the hood.
- **Rules**:
    - Use `async def` to define a function that can pause (coroutine).
    - Use `await` inside `async def` to pause and wait for another coroutine to complete.
    - You can't use `await` outside `async def` or call `async def` without `await`.

### Path Operation Functions in FastAPI

- **When to Use `async def`**:
    - If using libraries that support `await` (e.g., `results = await some_library()`).
    - Example:
        
        ```python
        @app.get('/')
        async def read_results():
            results = await some_library()
            return results
        ```
        
- **When to Use `def`**:
    - If the library doesn't support `await` (e.g., most database libraries).
    - Example:
        
        ```python
        @app.get('/')
        def results():
            results = some_library()
            return results
        ```
        
- **No I/O?**: Use `async def` for consistency, even without `await`, for potential FastAPI optimizations.
- **Mixing**: FastAPI supports mixing `async def` and `def` as needed. It handles both correctly.

### Key Notes

- **FastAPI's Role**: Automatically manages async for path operations, so you don't need to handle the event loop manually.
- **Performance**: FastAPI's async handling matches Node.js and Go, thanks to Starlette and AnyIO.

## Concurrency vs. Parallelism

- **Concurrency**: Multiple tasks make progress by switching during waits (single thread, cooperative multitasking).
    - Example: Ordering burgers, then flirting while waiting (task switching).
    - Best for **I/O-bound** tasks (e.g., web servers waiting for client requests).
- **Parallelism**: Multiple tasks run simultaneously on separate processors/cores.
    - Example: Multiple cleaners working on different parts of a house at once.
    - Best for **CPU-bound** tasks (e.g., machine learning, image processing).
- **Burger Analogy**:
    - **Concurrent Burgers**:
        - Order at counter, get a turn number, sit and flirt, check periodically, then pick up burgers.
        - Efficient use of wait time for other tasks (flirting).
    - **Parallel Burgers**:
        - Multiple cashiers/cooks, but you wait at the counter, blocking other tasks (no flirting).
        - Less efficient for waiting-heavy tasks.

## Coroutines

- **Definition**: Functions defined with `async def` that return a coroutine object, which can be paused/resumed.
- **Behavior**: Pauses at `await`, allowing the event loop to switch to other coroutines.
- **Example**:
    
    ```python
    async def get_burgers(number: int):
        # Simulate async work (e.g., network call)
        await asyncio.sleep(1)
        return [f"Burger {i}" for i in range(number)]
    
    @app.get('/burgers')
    async def read_burgers():
        burgers = await get_burgers(2)
        return burgers
    ```
    
- **Why Coroutines?**: Simplifies async code compared to older methods (threads, callbacks, Gevent).

## Concurrency + Parallelism in FastAPI

- **Concurrency**: Handles I/O-bound tasks (e.g., HTTP requests) efficiently with async.
- **Parallelism**: Can be added for CPU-bound tasks (e.g., machine learning) using multiprocessing in deployment.
- **Use Case**: FastAPI for Data Science APIs (e.g., ML model serving) benefits from both:
    - Async for handling client requests.
    - Parallelism for model inference.

## Writing Async Code

- **Event Loop**: Manages coroutines, switching between them during waits. FastAPI/Starlette handles this for you.
- **Libraries**:
    - **AnyIO**: Underpins FastAPI/Starlette, supports `asyncio` and `Trio` for structured concurrency.
    - **Asyncer**: Enhances AnyIO with better type annotations for writing custom async code.
- **Without FastAPI**:
    - Use `asyncio.run()` for top-level sync calls:
        
        ```python
        import asyncio
        
        async def main():
            burgers = await get_burgers(2)
            print(burgers)
        
        asyncio.run(main())
        ```
        
## Historical Context

- **Before `async/await`**:
    - Python: Used threads or Gevent (complex, hard to debug).
    - JavaScript: Used callbacks ("callback hell").
- **Modern Advantage**: `async/await` makes async code intuitive, similar to JavaScript's adoption in Node.js.

#### asyncio.Semaphore
- **asyncio.Semaphore**: A synchronization primitive that limits the number of concurrent coroutines (e.g., API calls) to prevent overloading resources. It acts like a “ticket system” where only a fixed number of tasks can run simultaneously.
- How: async with semaphore acquires a “slot”; when done, it releases it, allowing another coroutine to proceed.
```python
semaphore = asyncio.Semaphore(2)  # Allow 2 concurrent tasks
async with semaphore:
    await some_api_call()  # Only 2 calls run at once
```
- Prevents overwhelming the Gemini API (e.g., due to rate limits or quotas).
- Acts like a gate: only a fixed number of coroutines can pass at a time.
#### asyncio.gather
- **asyncio.gather**: Runs multiple coroutines concurrently and waits for all to complete, returning their results in order. It’s ideal for batch processing tasks like topic extraction.
- **What**: Runs a list of coroutines concurrently and waits for all to complete.
- **Why**: Efficiently processes all chunks in parallel, respecting the semaphore’s limit.
- **How**: Takes coroutines (tasks), schedules them, and returns their results (or None here, as results are stored in all_topics).
```python
 async def task(i):
    await asyncio.sleep(1)
    return i
results = await asyncio.gather(*[task(i) for i in range(3)])  # Returns [0, 1, 2]
```

**nonlocal Variables**:
- **What**: Allows a nested function (process_chunk) to modify variables in the outer scope (all_topics, required_topics_count).
- **Why**: Enables shared state across concurrent tasks without global variables or complex passing.
- **How**: Declared with nonlocal to bind to the outer scope’s variable.
```python
def outer():
    count = 0
    async def inner():
        nonlocal count
        count += 1
    return count
```

- **Example**

```python
async def process_chunk(chunk):
	nonlocal all_topics
	nonlocal required_topics_count

	async with semaphore:
		if len(set(all_topics)) >= required_topics_count:
			return 
			
		self.logger.debug(f"Processing chunk {chunk.chunk_id} from {chunk.source_url}")
```

**Nested Coroutine: process_chunk**:
- **New: nonlocal**:
    - Declares all_topics and required_topics_count as modifiable variables from the outer scope (execute).
    - Without nonlocal, Python would treat them as local variables, causing errors when updating.
- **Semaphore Usage**:
    - async with semaphore: Acquires a semaphore “ticket” before proceeding, ensuring only TOPIC_EXTRACTION_CONCURRENCY chunks are processed concurrently.
    - Automatically releases the ticket when the block exits (even on errors).
- **Early Exit**: If enough unique topics (len(set(all_topics))) are collected, skips processing to save resources.

```python
try:
	await asyncio.sleep(3)
	chunk_topics = await gemini_service.extract_topics_async(
		chunk.content, language, domain_type
	)

	if chunk_topics:
		all_topics.extend(chunk_topics)
		self.logger.debug(f"Extracted topics from chunk {chunk.chunk_id}: {chunk_topics}")
except Exception as e:
	if hasattr(e, '__class__') and e.__class__.__name__ == 'GeminiQuotaExhaustedError':
		raise
	self.logger.error(f"Error processing chunk {chunk.chunk_id}: {e}")
```

**Processing Logic**:
- await asyncio.sleep(3): Simulates a delay (possibly for rate-limiting or testing; could be removed in production).
- await gemini_service.extract_topics_async(...): Calls the async method to extract topics from the chunk’s content, passing language and domain_type.
- If topics are returned, extends all_topics and logs them.
- **Error Handling**:
    - Catches all exceptions.
    - If it’s a GeminiQuotaExhaustedError, re-raises it (likely to stop the entire process, as quotas are critical).
    - For other errors, logs and continues (fault-tolerant).

```python
tasks = [process_chunk(chunk) for chunk in chunks]
await asyncio.gather(*tasks)
```

**New: asyncio.gather**:
- Creates a list of coroutines (tasks) by calling process_chunk for each chunk.
- asyncio.gather(*tasks): Runs all coroutines concurrently, waiting for all to complete (or fail). Returns results in order (though here, process_chunk returns None since it modifies all_topics directly).
- Combined with the semaphore, ensures only a limited number of tasks run at once.
---
### The Problem It Solves

Python’s `asyncio` operates on a single-threaded event loop. This means it handles concurrency by rapidly switching between tasks whenever one is waiting for something (like a network response).

However, if you execute a standard, synchronous blocking function inside this loop—such as `time.sleep()`, a heavy file read, or a synchronous API call using the `requests` library—**the entire event loop stops**. No other async tasks can run until that blocking function finishes.

### The Solution

`asyncio.to_thread(func, *args, **kwargs)` takes your blocking function and offloads it to a worker thread.

- It returns a coroutine.
    
- Because it is running in a different thread, your main `asyncio` event loop is free to continue executing other tasks.
    
- When you `await` the coroutine, it pauses that specific execution path until the worker thread finishes and returns the result.

Under the hood, it uses a `ThreadPoolExecutor` to manage the threads.

### Code Example
Here is how you use it to prevent a blocking I/O operation from freezing your async program:
```python
import asyncio
import time

# 1. A standard, synchronous blocking function
def blocking_io_task(name, delay):
    print(f"Task {name}: Starting blocking operation...")
    time.sleep(delay) # This normally freezes the whole program
    print(f"Task {name}: Finished blocking operation!")
    return f"{name} is done."

async def main():
    print("Main: Starting...")
    
    # 2. Offload the blocking function to a separate thread
    # Notice we don't call the function directly; we pass it and its arguments.
    task1 = asyncio.to_thread(blocking_io_task, "A", 3)
    task2 = asyncio.to_thread(blocking_io_task, "B", 2)
    
    # 3. Run them concurrently
    results = await asyncio.gather(task1, task2)
    
    print("Main: All tasks finished.")
    print("Results:", results)

# Run the async program
asyncio.run(main())
```

### When to use it (and when NOT to)

- **DO use it for I/O-bound tasks:** It is perfect for interacting with older synchronous libraries (like `requests`, `sqlalchemy`, or standard file I/O) within a modern async codebase.
    
- **DO NOT use it for CPU-bound tasks:** Because of Python's Global Interpreter Lock (GIL), multiple threads cannot execute Python bytecode at the exact same time. If you have a heavy mathematical computation or data-processing task, `to_thread` will not actually speed it up. It will just move the CPU bottleneck to another thread.

For heavy CPU-bound tasks, you should use a `ProcessPoolExecutor` to spin up entirely separate processes instead of threads.