## 1. Between UUID and ULID, which is more convenient for a primary key in a relational database table?

**Answer:** ULIDs, because they are timestamp-based and lexicographically sortable, improving index performance.

- **Explanation:** ULIDs are timestamp-based and maintain lexicographical order, which makes them suitable for use as primary keys in relational databases. This property helps with better index performance since inserts are sorted by timestamp.

## 2. A function modifies a shared variable used across multiple threads but doesn't use any synchronization mechanism. What kind of issue is likely to arise?

**Answer:** Race condition

- **Explanation:** Without synchronization, multiple threads may access and modify the shared variable concurrently, leading to unpredictable results or data corruption, which is known as a race condition.

## 3. What is a webhook?

**Answer:** A webhook is a way for an app to provide real-time information to other systems by sending HTTP callbacks.

- **Explanation:** Webhooks allow one system to send real-time data to another system as soon as a specific event occurs, making them useful for real-time applications.

## 4. Which part of an HTTP request is conventionally used to send authentication data?

**Answer:** Header

- **Explanation:** Authentication data, such as tokens or API keys, is typically sent in the HTTP header under fields like `Authorization`.

## 5. What does the term "stateless" mean in the context of web servers?

**Answer:** It may not be able to detect duplicate requests

- **Explanation:** Stateless means the server does not retain information about previous requests, so it cannot detect or remember duplicate requests.

## 6. What is the purpose of a page table in virtual memory systems?

**Answer:** To translate logical addresses to physical addresses

- **Explanation:** A page table maps virtual memory addresses to physical addresses, enabling the operating system to efficiently use memory.

## 7. Which of the following mechanisms allows multiple readers but only one writer at a time?

**Answer:** Reader-writer lock

- **Explanation:** Reader-writer locks allow multiple threads to read data concurrently but ensure that only one thread can write to the data at a time.

## 8. How can you prevent race conditions between different threads?

**Answer:** By using synchronization tools like locks, mutexes, or synchronized blocks.

- **Explanation:** Synchronization mechanisms such as locks and mutexes control access to shared resources and prevent concurrent modifications by multiple threads, thus avoiding race conditions.

## 9. Why are locks often used with shared memory?

**Answer:** To ensure consistency during access

- **Explanation:** Locks ensure that only one thread can access a shared resource at a time, preventing inconsistent or conflicting changes.

## 10. Which primitive operation can be used to implement higher-level synchronization constructs?

**Answer:** Test-and-set

- **Explanation:** Test-and-set is an atomic operation used for implementing locks and other synchronization constructs, allowing the checking and modification of a value in one step.

## 11. What does "atomic" mean in the context of database transactions?

**Answer:** A transaction must fully complete or have no effect at all

- **Explanation:** Atomicity ensures that a transaction is treated as a single, indivisible unit. If any part of it fails, the entire transaction is rolled back.

## 12. Why might a system prefer Read Committed over Serializable in high-throughput applications?

**Answer:** Read Committed allows higher concurrency with fewer locks

- **Explanation:** Read Committed isolation level allows for more concurrency since it does not lock resources as strictly as Serializable, which can reduce throughput due to heavy locking.

## 13. One aspect where document-based databases are better than relational databases is...

**Answer:** Flexibility to change the schema without complex migrations

- **Explanation:** Document-based databases (e.g., MongoDB) are schema-less or have flexible schemas, making them more adaptable to changes without the need for complex schema migrations.

## 14. Why are B+-trees better than B-trees?

**Answer:** B+-trees support range queries more efficiently due to linked leaf nodes

- **Explanation:** B+-trees store all keys in leaf nodes and link them together, making range queries more efficient compared to B-trees, where range queries require traversing more nodes.

## 15. What is meant by a soft deleted row?

**Answer:** A row that is marked as deleted but not actually removed from the database

- **Explanation:** Soft deletion means marking a row as deleted (e.g., by setting a flag), while the data remains in the database for potential future use or recovery.

## 18. What does the term "idempotency" mean in the context of web APIs?

**Answer:** The system's intended result will be achieved no matter how many times the request is repeated

- **Explanation:** Idempotency ensures that repeated requests will not have side effects, meaning the same result will be achieved even if the request is made multiple times.

## 19. What is the main purpose of a Cache?

**Answer:** Reducing latency and load on primary storage

- **Explanation:** A cache stores frequently accessed data in memory to reduce access times and decrease the load on slower, primary storage systems.

## 20. What is meant by failover?

**Answer:** Switching to a redundant machine upon the failure of a primary machine

- **Explanation:** Failover is a mechanism that ensures system availability by switching to a backup system in case the primary system fails.

## 21. What is the difference between function overriding and overloading?

**Answer:** Overloading is defining multiple methods with the same name but different parameters, while overriding is redefining a method in a subclass.

- **Explanation:** Function overloading refers to defining multiple methods with the same name but different parameter types, while overriding involves a subclass providing a specific implementation for a method already defined in its superclass.

## 22. What is meant by a controller in the context of MVC?

**Answer:** A controller handles user input and updates the model and view accordingly.

- **Explanation:** In the Model-View-Controller (MVC) design pattern, the controller acts as an intermediary between the model (data) and the view (UI), processing user inputs and updating both.

## 23. What does REST stand for?

**Answer:** Representational State Transfer

- **Explanation:** REST is an architectural style for designing networked applications, based on stateless communication and the transfer of resources via standard HTTP methods.

## 24. What does join() do in the context of threads?

**Answer:** Blocks the current thread until the target thread finishes

- **Explanation:** The `join()` method is used to wait for a thread to complete before proceeding with the execution of the main thread.

## 25. What does an OS thread get its own copy of?

**Answer:** Stack memory

- **Explanation:** Each thread in an operating system gets its own stack memory to store local variables and manage function calls.

## 26. What is a race condition?

**Answer:** When the outcome depends on execution order

- **