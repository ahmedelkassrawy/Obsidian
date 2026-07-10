#### Basics of asyncio
- Event loop : The event loop handles the scheduling and execution of sync operations. It countinously checks for and executes tasks(coroutines). All async operations run by this loop, THERE can be only one event loop per thread.
-  **`asyncio.run()`**: This function is the entry point for running an asynchronous program. It creates and manages the event loop and cleans up after it completes. Remember that it is designed to be called once per thread. Some frameworks like FastAPI will run the event loop for you, others will require you to run it yourself.

#### Concurrency Explained
-  **Cooperative Concurrency**: Although you can schedule multiple async tasks, only one task runs at a time. This is different from true parallelism, where multiple tasks run at the same time. When a task hits an `await`, it suspends its execution so that another task may run. This makes async programs excellent for I/O-bound tasks where waiting is common, such as API calls to LLMs and other services.
-  **Not True Parallelism**: Asyncio enables concurrency but does not run tasks in parallel. For CPU-bound work requiring parallel execution, consider threading or multiprocessing. LlamaIndex typically avoids multiprocessing in most cases, and leaves it up to the user to implement, as it can be complex to do so in a way that is safe and efficient.

#### Handling Blocking (Synchronous) Code

- **`asyncio.to_thread()`**: Sometimes you need to run synchronous (blocking) code without freezing your async program. `asyncio.to_thread()` offloads the blocking code to a separate thread, allowing the event loop to continue processing other tasks. Use it cautiously, as it adds some overhead and can make debugging more challenging.
    
- **Alternative: Executors**: You might also encounter the use of `loop.run_in_executor()` to handle blocking functions.