## Overview
Consistent hashing is a distributed hashing technique used to distribute data across multiple servers (nodes) in a way that **minimizes data redistribution when nodes are added or removed**. **It’s widely used in distributed systems like caches, databases**, and CDNs to ensure scalability and fault tolerance.

---
## Problem It Solves
- **Scalability Issue with Simple Hashing**:
  - In a simple hashing approach (e.g., `hash(event_id) % N` where `N` is the number of servers), data is mapped to servers using modulo arithmetic.
  - **Problem**: Adding or removing a server changes `N`, causing almost all data to be redistributed (e.g., an event previously on server 2 may move to server 3 when `N` changes from 3 to 4).
  - **Impact**: Massive data movement causes performance issues, increased latency, or system downtime.

- **Consistent Hashing Solution**:
  - Minimizes data redistribution when servers are added or removed.
  - Ensures even data distribution across servers, especially with virtual nodes.

---
## How Consistent Hashing Works
1. **Create a Hash Ring**:
   - A fixed-size ring (e.g., 0 to 2³² or simplified to 0–100 for illustration).
   - Represents the hash space where both servers and data (e.g., event IDs) are mapped.

2. **Place Servers on the Ring**:
   - Each server is hashed (e.g., using server ID or name) and placed at specific points on the ring.
   - Example: For 4 databases, place them at points like 0, 25, 50, 75 on a 0–100 ring.

3. **Map Data to Servers**:
   - Hash the data key (e.g., event ID) to get a point on the ring.
   - Move clockwise from that point to find the first server encountered.
   - Example: Event ID hashing to 16 lands on the server at 25 (if servers are at 0, 25, 50, 75).

4. **Adding/Removing Servers**:
   - **Adding a Server**: Place the new server on the ring (e.g., at 90). Only data between the previous server (e.g., 75) and the new server (90) needs to move.
   - **Removing a Server**: Remove the server (e.g., at 25). Data previously assigned to it moves to the next server clockwise (e.g., 50). Minimal redistribution occurs.

5. **Virtual Nodes**:
   - To prevent uneven data distribution (e.g., one server getting all data from a removed server), each physical server is assigned multiple points on the ring (virtual nodes).
   - Example: Database 1 at points 0, 20, 40, 60, 80; Database 2 at 5, 25, 45, 65, 85.
   - When a server is removed, its data is spread across multiple other servers, balancing the load.

---

## When to Use in System Design Interviews
- **Relevant Technologies**:
  - Used in distributed systems like Redis, Cassandra, DynamoDB, MongoDB, CDNs, and message queues.
  - Mention consistent hashing when discussing these technologies to show awareness of their scalability mechanisms.

- **Deep Dive Scenarios**:
  - Required when designing scalable backend components, such as:
    - Distributed cache (e.g., Memcached, Redis).
    - Distributed database (e.g., Cassandra, DynamoDB).
    - Distributed message queue or similar systems.

- **Interview Tip**:
  - Briefly mention consistent hashing when discussing sharding or scaling.
  - Be prepared to explain the algorithm in detail if asked to design a distributed system component.

---

## Diagram: Consistent Hashing Ring
Below is a visual representation of a consistent hashing ring with 4 databases and virtual nodes. The ring spans 0–100, with databases placed at specific points and an event mapped to illustrate data assignment.

### Text Description of Diagram
- **Ring**: A circular structure representing the hash space (0–100).
- **Databases**: Four databases (DB1, DB2, DB3, DB4) at points 0, 25, 50, 75.
- **Virtual Nodes**: Additional points for DB1 (20, 40, 60, 80) and DB2 (5, 45, 65, 85).
- **Event Example**: Event ID hashing to 16, assigned to DB2 (next clockwise server at 25).
- **Scenario**: Removing DB2 shows data redistribution to DB3, DB1, and DB4 via virtual nodes.

![[Pasted image 20251029143833.png]]

---
## Key Takeaways
- **Minimizes Redistribution**: Only data in affected ring segments moves when adding/removing servers.
- **Virtual Nodes**: Ensure even data distribution by assigning multiple points per server.
- **Scalability**: Enables systems to handle dynamic server changes without significant performance impact.
- **Interview Relevance**: Essential for discussing or designing distributed systems like caches or databases.

---