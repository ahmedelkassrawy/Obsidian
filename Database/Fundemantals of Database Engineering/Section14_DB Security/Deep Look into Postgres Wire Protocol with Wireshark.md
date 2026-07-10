# Wiresharking PostgreSQL: Behind the Scenes of a Node.js Client Connection

## Episode Overview
- **Host**: Hassan from "Wireshark Them All"
- **Topic**: Analyzing PostgreSQL database connections using Wireshark
- **Setup**: Node.js client connecting to a cloud-based PostgreSQL instance (ElephantSQL)
  - Database has a table called "Employees" with sample rows (e.g., Rec, Edmund, Hussein)
  - Client action: Connect, query `SELECT * FROM employees`, print results, close connection
- **Key Focus**: Unencrypted connection for learning purposes (emphasizes importance of encryption in production)
- **Related Resources**: Check Hassan's video on connecting Node.js to Postgres

**Learning Goal**: Understand the packet-level flow of PostgreSQL protocol over TCP, including authentication, query execution, and termination.

## Tools and Preparation
- **Client**: Node.js with `pg` library (built by Brian, last name not recalled)
- **Server**: PostgreSQL 11.8 on Ubuntu (inferred from packet data)
- **Wireshark Filter**: Based on client and server IP addresses (obtained via ping)
- **Why Unencrypted?**: To inspect packets clearly; in real scenarios, use SSL/TLS to protect passwords and data.

## Normal Connection Flow

### 1. TCP Three-Way Handshake
PostgreSQL uses TCP for reliable communication. The connection starts with the standard TCP SYN, SYN-ACK, ACK sequence.

- Client sends SYN
- Server responds with SYN-ACK
- Client sends ACK

No TCP Fast Open here (as mentioned, Hassan has a video on that).

![[Pasted image 20251016033156.png]]

### 2. Startup Message (Client to Server)
- Client sends initial parameters:
  - Protocol version (e.g., major 3, minor 0)
  - `user`: Username
  - `database`: Database name
  - `client_encoding`: UTF-8
- Notably, **no password** sent initially (despite being in the connection string)
- Server acknowledges (ACK)

### 3. Authentication Request (Server to Client)
- Server responds with authentication challenge:
  - Requests MD5-hashed password (not plain text)
  - Checks if user exists, IP access allowed, etc.
- Client sends MD5 hash (prefixed with 'p', 41 characters total)
- Server authenticates successfully and sends:
  - Authentication OK
  - Parameter status: Data types (integers, dates), superuser status (none here), server version (11.8 on Ubuntu)
  - Ready for query ("I'm ready to receive your queries")

**Security Note**: MD5 is weak; unencrypted connections expose hashes. Always encrypt!

![[Pasted image 20251016033145.png]]

### 4. Query Execution
- Client sends query as plain text: `Q` (query marker) + `SELECT * FROM employees`
- If query is long, it may span multiple packets (depends on TCP window size)
- Server acknowledges receipt (ACK)
- Server sends results:
  - Data rows (e.g., employee names as ASCII/UTF-8 strings)
  - Wireshark decodes fields, showing content (237 bytes of actual data)
- Client acknowledges results

![[Pasted image 20251016033133.png]]

### 5. Connection Termination
- Client sends termination (`X` marker)
- Client initiates close with FIN-ACK
- Server responds with FIN-ACK
- Potential design note: To avoid TCP TIME_WAIT on client, server could initiate close (but depends on protocol/client impl)

**Packet Summary**:
```
[Client] -> Startup (version, user, db, encoding)
[Server] -> Auth Request (MD5)
[Client] -> MD5 Hash
[Server] -> Auth OK + Parameters + Ready
[Client] -> Query (SELECT * FROM employees)
[Server] -> Results
[Client] -> Terminate
TCP Close (FIN/ACK exchange)
```

## Error Case: Bad Credentials
- Similar initial flow: TCP handshake, startup message
- Server detects issue and sends error (`E` marker):
  - Fatal error code (e.g., FATAL 28P01)
  - Message: "password authentication failed for user [bogus user]"
  - Includes file/line number (Hassan notes this is shady for security; avoid exposing stack traces)
- Server initiates close (FIN)
- Client acknowledges, but may send extra data (potential bug in `pg` library)
- Results in TCP reset (RST) due to out-of-sync packets

**Security Best Practice**:
- Return ambiguous errors (e.g., "Invalid credentials") to avoid giving hints to attackers
- Never distinguish between wrong user vs. wrong password

**Packet Summary (Error)**:
```
[Client] -> Startup
[Server] -> Error Response
TCP Close (Server-initiated FIN, potential Client bug leading to RST)
```

## Key Learnings and Notes
- **Protocol Insights**:
  - PostgreSQL frontend/backend protocol is message-based over TCP.
  - Messages have markers (e.g., 'p' for password, 'Q' for query, 'X' for terminate).
  - Data is sent in binary/ascii format; Wireshark dissects it nicely.
- **Security Takeaways**:
  - Encrypt connections (SSL/TLS) to protect hashes and queries.
  - MD5 is insecure; use stronger methods like SCRAM-SHA-256.
  - Ambiguous errors enhance security but may hurt UX.
- **Potential Improvements**:
  - In client libs: If error received, don't attempt terminate (avoids RST).
  - Design protocols to have server close connections to manage TIME_WAIT.
- **Questions for Review**:
  - Why is the password not sent initially?
  - What risks does an unencrypted connection pose?
  - How does Wireshark help in debugging database issues?
- **TODO**: Practice by setting up your own Postgres + Node.js + Wireshark capture.

## References
- Transcript from Hassan's "Wireshark Them All" episode.
- PostgreSQL Docs: [Protocol Overview](https://www.postgresql.org/docs/current/protocol.html)
- Node.js `pg` Library: [GitHub Repo](https://github.com/brianc/node-postgres)
- ElephantSQL: Free tier for quick Postgres setup.

Save this as `Wireshark-Postgres-Notes.md` in your Obsidian vault for interactive linking and embedding!