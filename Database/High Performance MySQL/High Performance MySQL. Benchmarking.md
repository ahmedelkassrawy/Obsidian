The problem with benchmarking is that it's not real as the workload used benchmarking is as we mentioned before "fictional" which is usually very simple compared to real life workloads that are by nature

There are many factors that make benchmarking unrealistic, for example:
- The **data size** as it might not be easy to emulate a production load during benchmarking.
-  The **distribution of data** and the **varying nature of operations** performed as benchmarking data might lead to an **uneven distribution of executed queries** which might not match what really happens on production and thus yields misleading results.
-  The **pace at which queries are sent** to the system as a **naive benchmarking tool might send queries to the system as fast as it can** in an unrealistic time window which will cause the system to unnecessarily behave badly.

It's very tricky to do capacity planning using benchmarking. The book mentions an example of a benchmark that might lead you to think that if you benchmark your current database server and then you benchmark a new server and you **find out that the new server can do 40 times more transactions per second** than the old one and then **foolishly draw** the conclusion that the **new server will support 40 folds business growth.** This is unrealistic because as the business grows 40 folds, **its complexity is expected to grow way beyond that factor as queries get more complex**, you will have more features and so on.

### Benchmarking Strategies

- Whole Application (Full-stack) Benchmarking
- Benchmarking MySQL only

you would want to **benchmark the application as a whole** because you care more about the entire application's performance than just MySQL.
*this includes the web server itself, networking, any application level optimizations, etc.*

Before we design the benchmark suite:
- what is the question we are trying to answer.
- Do we want to know what's the best CPU for that server?
- Or do we want to know what's the best design of a schema to use?

There are common metrics that we would usually want to measure, for example:
- **Throughput**
- **Response time**
- **Concurrency
- **Scalability**

**Throughput**: **It's usually defined as the number of transactions per unit time**
- there are very common benchmarks like the TPC-C that many database vendors work hard to do well on.
- Those benchmarks measure OLTP (best for multi user interactive apps)

**Response time**: **Measures the time a task takes to complete in any unit time as it fits the application.**
- raw response time measurements not **useful** , 
- need to do some aggregations like max, min, average, median, percentiles to get any insights.
- **Max** &  **min** response time are quire **useless** as they are the easiest to get affected by intermittent events like a temporary lag or a cache hit.
- **Average** is also quite **misleading** because a few outliers will end up skewing the average.
- **Percentiles** are a **good** way to get a reasonable idea of the response time
- example, if the 95th percentile is 200ms, this means that the task finishes in 200ms or less 95% of the time.

**Concurrency**: **Measures how many concurrent tasks can be run at the same time.**
- ex, if you wish to measure **how many concurrent users can browse a web page at the same time,** it's **misleading** to consider the **number of concurrently running queries** on the server since thousands of users might incur only a very moderate number of concurrent queries which is the nature of the usage pattern of a web page (users take time to perform actions, they are not automatic).
- But, if you are measuring the **concurrency of a worker which inserts data** into the database, it makes sense to assume that an automatic workload will be sent to the database.
-  A more **accurate** way of measuring concurrency is to only **consider the number of threads that are doing work at a time** (which doesn't really reflect how many end users can use the system concurrently, it just gives an idea on what is the maximum number of concurrent users given that all users performed some database action at the same).


**Scalability**: **Measures how the system would perform under a changing workload**.

### Benchmarking Tactics

Very common mistakes that might render an entire benchmark results useless and possibly lead to making the wrong decisions:
- Using only a subset of the real data, such as using 1GB of data to benchmark an application that's expected to handle 10GBs of data. This might seems like a good option to cut corners but it will not reflect the real system behavior.
- Using biased data while benchmarking, such as using random data which will cause results to be skewed.
- Using irrelevant scenarios, such as using a single-user scenario for a multi-user system or benchmarking a distributed system on a single machine, etc.

The next step after setting the goal for a benchmark, is to decide whether to use a standard benchmark or design one of your own.

 ex, don't use a **TPC-H benchmark** which is an adhock, decision support benchmark to measure an **OLTP** (online transactions processing) system.

the following is a somewhat general process of setting up the benchmark:
- **Take a snapshot of production data** (make sure to have it ready for future restores in case the benchmark needed to be repeated.)
- Instead of **just running a set of queries** against this dataset, it's a **good idea to log queries on production for a long period** or for multiple periods **during representative time** **windows** to cover all system activities and use this log to simulate a normal production load.
- **Record** results and **plot** them to make it easier to draw conclusions.
- Try to **automate the process or record it** to be able execute it in exactly the same way in case you needed to repeat the benchmark for a different setting.

**How long should a benchmark runs?**
For a benchmark to be useful it has to run for a meaningful period of time that allows the system to reach its steady state which could take a lot of time.

**Before a benchmark starts**, you would probably need to **warm up the system**, during the warm up process, you might see fluctuations that will eventually start to diminish and the system would start exhibiting a consistent behavior.

As a **rule of thumb**, keep running the benchmark until the system looks like it has been steady for at least how long the initial warm up appeared to take.

**What data to capture during a benchmark?** 
It's always a good idea to record as much data as you can in the rawest form possible during a benchmark.
Recording raw data is a good idea because you can manipulate it in many different ways and still have the raw data if you get any new ideas.

### Benchmarking Tools
it's called `mysqlslap` which is a single-component benchmarking tool (only benchmarks MySQL). `mysqlslap` let's you create a test schema, specify the number of connections, run a test load of sql queries or even let it generate random `SELECT`s based on the provided schema and it reports time information.