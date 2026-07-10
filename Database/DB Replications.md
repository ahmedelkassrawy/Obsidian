### Master/Backup Replication 
● One Master/Leader node that accepts writes/DDLs
● One or more backup/standby nodes that receive those writes from the master 
● Simple to implement no conflicts

### Multi-Master Replication 
● Multiple Master/Leader node that accepts writes/ddls 
● One or more backup/follower nodes that receive those writes from the masters 
● Need to resolves conflict

### Synchronous vs Asynchronous Replication 
● Synchronous Replication, A write transaction to the master will be blocked until it is written to the backup/standby nodes
● Async Rep, A write transaction is considered successful if it written to the master, then asynchronously the writes are applied to backup nodes

### Pros & Cons
Pros:
- Horizontal Scaling 
- Region Based Queries - DB per region

Cons:
- Eventual Consistency
- Slow writes (synchronous)
- Complex to Implement (Multi Master)

## In Details

### Horizontal Scaling
- **Explanation**: Replication enables horizontal scaling by distributing database workload across multiple servers (replicas). Instead of upgrading a single server's hardware (vertical scaling), you add more servers to handle increased traffic or data volume.
- **Benefit**: This improves performance, allows for handling larger datasets, and supports growing user bases without relying on expensive hardware upgrades.
- **Example**: A web application can distribute read queries across multiple read-only replicas to reduce the load on the primary database.

### Region-Based Queries (Database per Region)
- **Explanation**: Replication allows deploying database replicas in different geographic regions, enabling queries to be served from the closest replica to the user. This is often referred to as geo-replication.
- **Benefit**: Reduces latency for users by serving data from nearby servers and improves user experience. It also supports compliance with regional data residency requirements.
- **Example**: A global e-commerce platform can have a replica in Europe, Asia, and North America to serve customers faster in each region.
## Cons
### Eventual Consistency
- **Explanation**: In many replication setups (e.g., asynchronous replication), changes made to the primary database are propagated to replicas with a delay. This leads to eventual consistency, where replicas may temporarily serve outdated data.
- **Drawback**: Applications requiring immediate consistency (e.g., financial systems) may encounter issues if users query a replica before it’s fully updated.
- **Example**: A user updating their profile on a social media platform might not see the changes immediately if querying a replica that hasn’t yet synced.

### Slow Writes (Synchronous)
- **Explanation**: In synchronous replication, the primary database waits for confirmation from one or more replicas before committing a write operation. This ensures consistency but introduces latency.
- **Drawback**: Write performance can degrade, especially if replicas are geographically distant or network latency is high, impacting applications with frequent write operations.
- **Example**: A banking application using synchronous replication may experience slower transaction processing due to the need to sync with remote replicas.

### Complex to Implement (Multi-Master)
- **Explanation**: Multi-master replication allows multiple database nodes to accept writes simultaneously, increasing availability but introducing significant complexity. Conflict resolution, data synchronization, and maintaining consistency across nodes are challenging.
- **Drawback**: Requires sophisticated mechanisms to handle conflicts (e.g., when two nodes update the same record) and increases the risk of data inconsistencies if not properly managed.
- **Example**: A collaborative document-editing platform using multi-master replication must resolve conflicts when users edit the same document concurrently on different servers.

---
### **1. Concept Overview**

**Database Replication** means **copying data from one database server (the “primary”) to one or more other servers (the “replicas”)** to keep them in sync.

- **Primary (or Master):** Handles all **write** operations (INSERT, UPDATE, DELETE).
- **Replicas (or Slaves / Read Replicas):** Receive updates from the primary and are mainly used for **read** operations (SELECT).

Replication can be **synchronous** or **asynchronous**:
- **Synchronous:** Writes happen only after all replicas confirm. (Strong consistency, but slower.)
- **Asynchronous:** Primary doesn’t wait for replicas. (Faster, but replicas might lag slightly behind.)

---
### **2. Visual Diagram**
#### **Basic Replication Setup**

```
           ┌───────────────────┐
           │   Application     │
           └───────────────────┘
                    │
          ┌─────────┴─────────┐
          │                   │
   (Writes go here)     (Reads go here)
   ┌────────────────┐    ┌────────────────┐
   │ Primary (DB1)  │ => │ Replica (DB2)  │
   │ Handles writes  │    │ Syncs from DB1 │
   └────────────────┘    └────────────────┘
```

➡ The **primary** handles all writes.  
➡ **Replicas** continuously copy data changes to stay updated.  
➡ Reads are distributed to replicas → better performance.

---
### **3. Common Use Cases**

| Use Case              | Description                                                             |
| --------------------- | ----------------------------------------------------------------------- |
| **Load Balancing**    | Spread read queries across replicas to reduce load on the main DB.      |
| **High Availability** | If the primary fails, a replica can be promoted to take over.           |
| **Disaster Recovery** | Keep a replica in another region or data center for backup/failover.    |
| **Analytics**         | Run heavy reporting or analytics on replicas, keeping the main DB fast. |

---
### **4. Example Scenarios**

- **E-commerce Platform:**
    - Primary handles all order placements and updates.
    - Replicas serve read requests like product browsing, order history, etc.
    - Reduces latency for users across different regions.
        
- **Global Services (e.g., YouTube, Netflix):**
    - Replicas deployed in different continents.
    - Each replica serves local users, synchronized periodically with the global primary.
---
### **5. When to Use Database Replication**

Use replication when you need:
- **Scalability:** Too many read requests on a single DB.
- **High Availability:** Want fast recovery from hardware or network failures.
- **Geographic Distribution:** Users around the world need low-latency access.
- **Data Backup:** Extra live copies for protection and maintenance.
---
### **6. Extended Diagram: Multi-Replica Setup**

```
                ┌───────────────────┐
                │   Application     │
                └───────────────────┘
                         │
                         ▼
                  ┌───────────────┐
                  │ Primary (DB1) │
                  │ Writes + Sync │
                  └───────────────┘
                    /       |       \
                   ▼        ▼        ▼
         ┌────────────┐ ┌────────────┐ ┌────────────┐
         │ Replica A  │ │ Replica B  │ │ Replica C  │
         │ (EU Reads) │ │ (US Reads) │ │ (Asia Reads)│
         └────────────┘ └────────────┘ └────────────┘
```

➡ Each region reads from its nearest replica — faster performance and redundancy.

---
**Quick Summary Mnemonic:**

> **“Replicate to Read, Shard to Scale.”**

- **Replication** → Same data copied across nodes (for reliability, speed, availability).
- **Sharding** → Different data split across nodes (for size and parallelization).
---
## **1. Master–Slave (Primary–Replica) Replication**

**(Most common type)**
### **Concept**
- One **primary** database handles all **writes**.
- One or more **replicas** receive updates and handle **reads**.
- Data flows **one way** — from primary → replicas

```
           ┌──────────────┐
           │  Primary DB  │
           │ (Write + Read)│
           └───────┬──────┘
                   │ Replicates changes
          ┌────────┴────────┐
          │                 │
   ┌──────────────┐  ┌──────────────┐
   │ Replica DB 1 │  │ Replica DB 2 │
   │ (Read only)  │  │ (Read only)  │
   └──────────────┘  └──────────────┘
```

### **Use Cases**

- High read traffic applications (e.g., e-commerce catalogs, blogs).
- Safe, simple setup.
- Ideal for **read scaling** and **fault tolerance**.

**Examples:** MySQL replication, PostgreSQL streaming replication.

---
## **2. Master–Master (Multi-Primary) Replication**
**(Bidirectional replication)**
### **Concept**
- Two or more databases act as **masters**.
- Each can handle **writes**, and they **synchronize** with each other.

```
        ┌──────────────┐   ⇄   ┌──────────────┐
        │  Master A    │  ⇄   │  Master B    │
        │ (Read/Write) │      │ (Read/Write) │
        └──────────────┘      └──────────────┘
```

### **Use Cases**

- Systems that need **write availability in multiple regions**.
- Disaster recovery — if one master fails, another continues.
- **Active-active clusters** in distributed environments.

**Challenges:**
- Conflict resolution (when two nodes update the same data).
- More complex setup and maintenance.

**Examples:**  
MySQL Group Replication, PostgreSQL BDR, CouchDB, Cassandra.

---

## **3. Multi-Master (Cluster-Wide Replication)**

### **Concept**
- Many nodes act as peers — all can **read and write**, and data is synchronized across all nodes.
- Common in **distributed NoSQL databases**.

```
    ┌────────────┐ ⇄ ┌────────────┐ ⇄ ┌────────────┐
    │  Node 1    │ ⇄ │  Node 2    │ ⇄ │  Node 3    │
    │ Read/Write │    │ Read/Write │    │ Read/Write │
    └────────────┘    └────────────┘    └────────────┘
```
### **Use Cases**
- Global-scale systems needing **high availability** and **low latency everywhere**.
- **Decentralized apps** where users in different regions write data simultaneously.
**Examples:** MongoDB Replica Sets, Cassandra, CockroachDB, YugabyteDB.
---
## **4. Synchronous vs Asynchronous Replication**

| Type             | Description                                               | Pros                    | Cons                                     |
| ---------------- | --------------------------------------------------------- | ----------------------- | ---------------------------------------- |
| **Synchronous**  | Primary waits for replica confirmation before committing. | Strong data consistency | Slower performance                       |
| **Asynchronous** | Primary doesn’t wait; replicas update later.              | Faster writes           | Possible lag / data loss if crash occurs |

---

## **5. Choosing the Right Replication Type**

| Scenario                                 | Recommended Type             |
| ---------------------------------------- | ---------------------------- |
| High read volume, low write load         | **Master–Slave**             |
| Write availability in multiple locations | **Master–Master**            |
| Global distributed system                | **Multi-Master / Cluster**   |
| Strict data consistency                  | **Synchronous replication**  |
| Performance > consistency                | **Asynchronous replication** |

---
### **Quick Summary Mnemonic**

> **“Slave to scale, Master to share.”**
- **Master–Slave:** Scale reads safely.
- **Master–Master:** Share writes across regions.
- **Multi-Master:** Go global with resilience.
---