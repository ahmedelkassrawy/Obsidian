## Introduction to Optimization

Optimizing server performance focuses on reducing response time for queries. Understanding why a server takes a specific amount of time to respond requires detailed analysis of query execution.

### Key Considerations

- **Prioritizing Queries**: Not all queries are equally important for optimization.
    - Example: A query running 5% of the time, even if optimized significantly, will only improve overall performance by up to 5%.
    - Queries running 50% of the time are better candidates for optimization, as minor improvements can yield greater overall impact.

## Profiling

Profiling is more than just measuring total task execution time. It involves breaking down the task into individual child tasks to understand the server's behavior.

### Profiling Structure

- **Call Graphs**: Constructed to visualize what the server does to execute a query.
- **Profile Table Columns** (subset for clarity):
    1. **Rank**: Indicates task importance based on its response time percentage of total response time.
    2. **Total Response Time**: Aggregated response time for all instances of a task.
    3. **Percentage of Total Time**: Determines the task's rank.
    4. **Instance Count**: Number of times the task is executed.
    5. **Average Response Time**: Average time per instance.
    6. **Task Description**: Details of the task itself.

### Types of Profiling

1. **Execution Time Profiling**:
    - Best for **CPU-bound tasks** where queries spend most of their time processing.
2. **Wait Analysis**:
    - Best for **I/O-bound queries** where time is spent waiting for resource access or data read/write.

## Instrumentation

Instrumentation tools provide detailed insights into server performance, helping identify bottlenecks.

### Tools

- **New Relic**:
    - A powerful tool for profiling web servers.
    - Breaks down endpoint response times into finer-grained tasks.
    - Helps determine if slowness is due to database queries or other factors, guiding whether to profile the database directly.

### MySQL Profiling

Profiling MySQL queries can be approached at two levels:

#### 1. Profiling the Server's Workload

- Useful when the application lacks instrumentation, and problematic queries are unknown.
- **MySQL Slow Query Log**:
    - Logs queries slower than a threshold set by `long_query_time`.
    - Setting `long_query_time = 0` logs all queries, creating a server profile.
    - **Considerations**:
        - Logging incurs I/O overhead (negligible for I/O-bound workloads, noticeable for CPU-bound).
        - Logging all queries can consume significant disk space; requires regular log cleanup.
        - Third-party tools can assist with log management.

#### 2. Profiling a Single Query

- Used when problematic queries are identified through instrumentation or server profiling.
- **MySQL Commands**:
    - Enable profiling: `SET profiling = 1;`
    - View all profiles: `SHOW PROFILES;`
    - View specific query profile: `SHOW PROFILE FOR QUERY <id>;`
- **Benefits**:
    - Provides a detailed breakdown of tasks for a query.
    - Highlights issues like:
        - Temporary table creation.
        - Un-indexed reads.
        - Lock contention.
    - Guides optimization by pinpointing specific bottlenecks.

## Optimization Insights

- Query profiles make optimization more targeted but not always "obvious."
- Example: If a profile shows a query creates a temporary table, focus on why it’s created and how to avoid it.
- Profiles direct efforts toward resolving specific issues (e.g., adding indexes, reducing lock contention).