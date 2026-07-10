![[Pasted image 20250427235914.png]]

- The topmost layer handles **connection pooling, security, authentication,..**
- This layer not specifically to DBMS, but a layer that **any client/server system** would probably need to implement.

- Second layer -> **brains of MySQL** 
- Layer responsible for the query parsing, analysis, query optimization, caching, etc. + stored procedures, views, triggers, etc. 

- Third Layer -> **storage engines** 
- Layer is responsible for storing/retrieving data. It basically acts the file system in the database.
- **Storage engines layer is not considered part of the MySQL server** 
- The server can communicate with a variety of storage engines via a storage engine API which allows the storage engine to receive explicit commands to perform certain operations, such as, fetch this record, insert this record without the need to parse queries (with a few exceptions)
- Another key insight here is that the **server components are global to all databases within that server**, but the **storage engine is a per table configuration**
- You can configure which table uses which storage engine based on the needs and the trade offs you are willing to take.

### Connection Management and Security

A MySQL server is expected to process multiple queries from multiple clients.
- **Each client** gets its **own thread** within the server process through which all queries from that client are processed.
- When a **client** initializes a **database connection it's assigned a thread** within the server process.
- **Creating** and **destroying** threads is an expensive process,
- That's why most systems that need to **handle connections implement "Connection Pooling"** where the system **caches** those threads in a pool of connections and **re-uses** the threads for multiple clients.
- also helps **limiting** the number of concurrent clients at the system's desired capacity.

Any connection to MySQL needs to be authenticated via a variety of authentication methods including passwords, hosts, usernames, SSL certificates, etc.
- Once a connection is **authenticated**, that **doesn't mean** that all queries can be processed from that connection
- MySQL implements a **privileges system** that allows **database administrators** to grant certain permissions to certain users, such as, **preventing non-root** users from deleting tables or giving a certain user a read-only access, etc.

### Optimization and Execution

When a connection to MySQL sends a query -> it gets **parsed** and internal structure called a **parse tree** is created.
MySQL applies a wide range of optimizations to that structure including:
 - **re-writing** the query
 - **re-arranging** certain operations
 - **deciding** which **indexes** to use and much more
Query hints can be passed to MySQL to affects its decision making process, like forcing it to use a specific index and so on.

The Query Optimizer is storage engine independent in the sense that it doesn't really care which storage engine is used -> but it communicates with storage engines to ask for its capabilities and get metrics on how much certain operations cost which affects its decision making process.
This guarantees that the Optimizer would **generate a** **suitable execution plan** for any storage engine.

- MySQL also has a **Query Cache** that it refers to **before executing** the query.
- The cache can only have `SELECT` statements along with their corresponding result set and it can directly return that result without further steps (if the entry is in the cache, it means that it's still valid).

### Concurrency Control
MySQL must handle **multiple queries concurrently** while ensuring **data integrity** and **high performance**. Using the analogy of a shared mailbox file, concurrent access by multiple clients can lead to **data corruption** if not managed properly.

## Concurrency Challenges
- **Single client** adding entries to the mailbox is fine, but **multiple clients** inserting simultaneously risks corruption.
- **Reads** are generally safe for concurrent access, but **inconsistent data** can occur if a client is reading while another is writing or deleting.

## Locking Mechanisms
- **Read Lock (Shared Lock)**: Allows multiple clients to read simultaneously but is blocked by write operations.
- **Write Lock (Exclusive Lock)**: Prevents any other read or write operations until released, ensuring exclusive access for writes.

## Lock Granularity
Lock granularity balances **performance** and **concurrency** by determining what portion of the resource to lock:
- **Table Locks**:
  - Simplest, least overhead.
  - Write lock blocks all reads and writes; read lock allows other reads but blocks writes.
  - Write locks have priority over read locks; read locks can be upgraded to write locks in the same connection.
  - Managed at the **server level**.
- **Row Locks**:
  - Locks specific rows, enabling higher concurrency but with more overhead to identify rows.
  - Common in **InnoDB**; used for operations like inserts.
  - May lock more than one row (e.g., **next-key locking** for unique indexes to prevent **phantom reads**), potentially causing **deadlocks** if overlapping gaps are locked.
  - Managed at the **storage engine level**.

## Example: Row Locking in InnoDB
For a table with a unique index on the `name` column:
```
+----+------+
| id | name |
+----+------+
| 1  | ggg  |
| 2  | jjj  |
+----+------+
```
Inserting a record with `name = 'ppp'` requires locking the index gap between `jjj` and `ppp`. Concurrent inserts may lock overlapping gaps, risking deadlocks.

## Table vs. Row Locks
- **Table Locks**: Used for operations like `ALTER TABLE`.
- **Row Locks**: Preferred for most operations (e.g., `INSERT`, `UPDATE`) due to better concurrency.
- MySQL supports both, depending on the operation and engine.

## Key Considerations
- **Lock Contention**: Excessive locking slows the system; careful lock selection is critical.
- **Performance vs. Overhead**: Fine-grained row locks improve concurrency but increase overhead compared to table locks.
- **Deadlocks**: Can occur with row locks, especially with next-key locking in InnoDB.
- **MySQL Reference**: A reliable source for up-to-date details, as locking behavior evolves across releases.

> **Note**: The book presents table and row locks as alternatives, but both are used in practice. Further chapters or the MySQL Reference may clarify additional details.
### Transactions
A transaction allows you to **group certain operations** that are **not atomic by default into an atomic construct** that implements an **all or nothing functionality** either the transaction succeeds and all its operations are performed or the transaction fails and none of its operations is performed.

The most common example here, which is also the example that the book uses is a bank transaction that takes a certain amount of money from a checking account and deposits it into a savings account. It looks something like this:

```MySQL
1: START TRANSACTION;
2: SELECT balance FROM checking WHERE customer_id = 1;
3: UPDATE checking SET balance = balance - 200.00 WHERE customer_id = 1;
4: UPDATE savings SET balance = balance + 200.00 WHERE customer_id = 1;
5: COMMIT;
```

So what's is an ACID transaction?
- **A**tomcity: Means that a **transaction should work as indivisible unit** that **either completes to success or gets rolled back** on failures (this is the all or nothing we discussed above).
    
- **C**onsistency: Means that **the database only moves from one consistent state to another** so any changes done by a transaction don't reflect unless that transaction is committed.
    
- **I**solation: Means that there **should be a level of control of on when changes done by a transactions are visible to other transactions.** Let's consider the case when a bank statement summary query runs to get the user checking account details and it runs between statement 3 and 4. In this case it makes sense that as long as the transaction didn't yet complete, the checking account shouldn't show up missing $200. Isolation has many levels that we will discuss later.
- - **D**urability: Means that **once a transaction is committed, the changes are permanent and no data is lost during a crash.** Of course, nothing is 100% durable, and durability is implemented differently to offer different guarantees. For example, in some system, a change has to be applied to a subset of replicas before it's acknowledged, **this guarantees that if a replica crashes, the data is available on another replica.** It's easy to see that the more durability guarantees a system provides, the more overhead it incurs on performance.
## Isolation Levels

1. **READ UNCOMMITTED**
    - **Behavior**: Transactions can read **uncommitted changes** from other transactions (known as **dirty reads**).
    - **Issues**: Rarely used due to problematic behavior and minimal performance benefits.
    - **Use Case**: Not practical for most applications due to data inconsistency risks.
2. **READ COMMITTED**
    - **Behavior**: Transactions only see changes from other transactions that were **committed** before the current transaction's query.
    - **Issues**: Allows **non-repeatable reads**, where the same SELECT query within a transaction can return different results if another transaction commits changes in between.
    - **Example**:
        - Transaction 1 reads balance: $200.
        - Transaction 2 updates balance to $250 and commits.
        - Transaction 1 reads balance again: $250 (not $200).
    - **Use Case**: Default in databases like PostgreSQL, but not MySQL.
3. **REPEATABLE READ**
    - **Behavior**: Ensures all queries within a transaction see the **same row data**, regardless of concurrent transaction changes.
    - **Issues**: Introduces **phantom reads**, where a new row inserted by another transaction appears in a subsequent SELECT of the same range.
    - **Solution**: Handled by **multiversion concurrency control (MVCC)**, which maintains row versions.
    - **Use Case**: MySQL's default isolation level, balancing consistency and concurrency.
4. **SERIALIZABLE**
    - **Behavior**: Eliminates phantom reads by **forcing a strict order** on transactions and placing **read locks** on all rows read, preventing conflicts.
    - **Issues**: Most restrictive, leading to frequent **timeouts** and **lock contention**.
    - **Use Case**: Rarely used due to significant performance overhead.

## Key Points

- **Trade-off**: Higher isolation levels (e.g., SERIALIZABLE) ensure greater data consistency but reduce concurrency and performance.
- **Default Levels**:
    - MySQL: **REPEATABLE READ**.
    - PostgreSQL: **READ COMMITTED**.
- **Concurrency Issues**:
    - **Dirty Reads**: Only in READ UNCOMMITTED.
    - **Non-repeatable Reads**: In READ COMMITTED.
    - **Phantom Reads**: In REPEATABLE READ (mitigated by MVCC).
- **Practical Use**: REPEATABLE READ and READ COMMITTED are most common, while READ UNCOMMITTED and SERIALIZABLE are less frequently used due to their extremes in consistency and performance impacts.

![[Pasted image 20250428011410.png]]

A **deadlock** occurs in a database when **two or more transactions** are unable to proceed because each is waiting for a resource (e.g., a lock on a row, table, or gap) that another transaction holds, creating a **circular dependency**. This results in all involved transactions being stuck indefinitely unless resolved.

## Multiversion Concurrency Control (MVCC)

- Row locking is not good enough as a performance improvement, that's why most MySQL transnational storage engines don't solely depend on it.
- Instead a mix of **row locking** + **multiversion concurrency control** (**MVCC**) is used to avoid the need for locking at all in many cases.
- This allows non-blocking reads and only locking necessary rows during writes.
- MVCC in MySQL works by **keeping a snapshot** of the database at a **certain point of time** which allows operations within the same transaction to be served by the same snapshot
- thus have a **consistent view** of how the data was when the transaction began regardless of how long it runs.
- This means that different transactions can see different data from the same table at the same time.

The way InnoDB implements MVCC is by keeping 2 extra hidden columns
- One represents when the version of this row was created
- The other presents when the version of this row expired but rather than saving the actual timestamp, it saves a monotonic system version number that increases when a new transaction begins.

 Each transaction has its own record of the system version number when the transaction began and it uses that number to access the correct version as highlighted below
 - **SELECT**: InnoDB has to find rows with a **creation version number less than or equals to the transaction version number**
	 - this ensures that those records **either already existed before the transaction began** (version number is less than the transaction's version number) or **were inserted/altered by the same transaction** (version number is equal to the transaction's version number).
- **INSERT**: InnoDB records the current system version number as the creation version number of the inserted row.
- **DELETE**: InnoDB records the current system version number as the deletion version number of the deleted row.
- **UPDATE**: InnoDB inserts a new copy of the altered row and it sets its creation version number to the current system version number, it also sets the current system version number as the old record's deletion version number.
It's worth mentioning that MVCC only works with `READ COMMITTED` and `REPEATABLE READ` isolation levels.

## MySQL's Storage Engines
#### InnoDB
- InnoDB is the **default transactional** storage engine for MySQL
- yes, some MySQL storage engines are **not transactional.**
- InnoDB saves its data in a **series of data files** collectively known as **table space.**
 - It defaults to `REPEATABLE READ` isolation level  + **MVCC** to achieve high concurrency.
 - uses a **clustered index structure** which defines the way data is stored in the table **sorted ascendingly by their PK** which results in extremely fast PK look ups.
 - On the other hand, **secondary indexes** will have to contain the **PK** as a part of them 
 - So it's recommended to always use **small PKs** because **if the PK is large**, it will make all other **secondary indexes large** as well.
 -  implements a variety of internal optimizations such as **read-ahead** which **pre-fetches** **data** from disk that it **predicts** it will need to read later, **insert buffers for bulk inserts**, etc.

#### MyISAM
- one of MySQL's **non-transactional** storage engines (it doesn't support transactions)
- provides other useful features such f**ull-text indexing** and **compression**.
- biggest weakness is that it's not remotely crash safe
- Better for **small tables** that won't take much time to repair.
- **locks entire tables** not rows as opposed to InnoDB.
- Readers will have to acquire **shared read locks** on all tables it needs to read data
- writers will acquire **exclusive write locks**.
- ability to support full-text search as it **allows indexing the first 500 characters** of `BLOB` or `TEXT` fields.
- This allows MyISAM to serve some **complex word search queries.**
- Another very interesting feature that's useful for read only systems is **compression**.
- MyISAM allows you to **compress** tables that **don't change**.
- Compressing a table **doesn't allow** you to **alter** it in any way, but you can always **decompress**, **modify** it and **recompress**.

### Storage Engine Selection 
When choosing a MySQL storage engine, consider the following factors:

1. **Transactions**:
   - Use **InnoDB** for applications requiring **transactions**.
   - For simple **SELECT** and **INSERT** operations without transactions, **MyISAM** may suffice.

2. **Backups**:
   - **InnoDB** supports **online backups**, allowing backups without downtime.
   - If downtime for backups is acceptable or backups are unnecessary, other engines like MyISAM can be considered.

3. **Crash Recovery**:
   - **InnoDB** offers robust **crash recovery**, reducing repair time for large datasets.
   - **MyISAM** tables are prone to frequent corruption, making recovery time-consuming.

4. **Special Features**:
   - Each engine provides unique features (e.g., InnoDB’s transactional support, MyISAM’s simplicity).
   - Choose an engine based on the **specific features** required for your application.

**Key Takeaway**: **InnoDB** is often preferred for its transactional support, online backups, and reliable crash recovery, especially for critical applications. **MyISAM** may be suitable for non-transactional, low-maintenance scenarios but is less robust.