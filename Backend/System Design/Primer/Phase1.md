Scalability & Availability

1. Performance vs Scalability
**Performance** = one request is fast (low latency now, with few users).
**Scalability** = it _stays_ fast as load grows.

The test: if adding users makes each request slower, you have a **performance** problem
- If adding **servers** fixes it, you have a scalable system.
- If adding servers _doesn't_ fix it → you hit a shared bottleneck (one DB, one lock).

2. Latency vs Throughput
**Latency** = time for one request (ms).
**Throughput** = requests handled per second

- You want acceptable latency at high throughput
- Batching trades one for the other: your rag **50-chunk embed batch** raised throughput (fewer Cohere calls) at the cost of a little latency per chunk.
- That trade was correct because ingestion is background work — nobody's waiting on a single chunk.

2. CAP
When your data lives on **more than one machine** and the network between them breaks (a **partition** — not "if", _when_), 
you can keep only **two** of these three

**C** — Consistency    every read sees the latest write
**A** — Availability     every request gets an answer (maybe stale)
**P** — Partition      tolerance system keeps working when the network splits

**P is not optional** on a real network — links do drop

- Your data lives on two machines, Node A and Node B, that copy writes to each other. 
- The cable between them breaks. They're both alive, but they can't talk. 
- A user writes to "A". Now B doesn't know about that write. 
- Someone reads from B. 
- **What does B do?** That single decision is the whole choice.

So the real choice is **C vs A during a partition**:
- CP - B refuses
B thinks "I might be stale. I wont guess"
So B returns an error until the cable is back and its caught up
- we lose availability (that read failed) to protect consistency (nobody ever sees old data)
	Problems it fixed: 
	- **Bank balance** — you have $100. You withdraw $100 from A. If B still says "$100 available" and lets a second withdrawal through → you spent $200 you don't have. Better to error: "try again."

	- **Inventory** — 1 concert ticket left. A sells it. If B doesn't know and sells it too → two people, one seat. Better to refuse than oversell.

AP - B answers anyway
B thinks: "I'll give you what I've got. It might be a few seconds old. I'll sync up when the cable's back."

You keep availablity (every read succeeds) and gives up consistency for a short window (some reads are stale until it reconnects again)

Problems it fixes:
- **Social feed** — your friend posted; the cable's down; you don't see it for 5 seconds. Nobody's hurt. Far better than the whole app showing an error.

- **Analytics dashboard** — the view count says 1,000 but it's really 1,003. Fine. You'd rather the dashboard _load_ than throw an error because one counter is behind.

During a network split, does serving _slightly old data_ cause real damage?  
**Yes → CP** (refuse, stay correct).        where the money or soemthing that cant be returned and has to be in real time
**No → AP** (answer, stay up).          availablity is the key becuase its not that important to be consistent

**Tie to your work.** 
The Shutterabia D1 dashboard mirror is **AP** — a post shows "scheduled" for 3 seconds after it really published. Harmless → serve it, stay up. 

raaaaag on **one** Postgres — CP or AP? (Hint: what does CAP require _before_ the choice even exists?)
- **this is the trick, and you walked into it.
- ** raaaaag runs on **one** Postgres. CAP only exists when data is on **more than one machine** — you need at least two copies for a partition to split them. 
- One node = there's nothing to partition = **CAP doesn't apply at all.** 
- It's neither CP nor AP.

The lesson: 
**don't reach for CAP until data is replicated.** 

The moment you add a read replica to that Postgres — which is exactly the URL-shortener scaling fix — _then_ CAP wakes up and you must choose (and pgvector reads would be **AP**: a slightly stale search result is fine).

### Three consistency patterns

All three answer one question:

after a write lands, when do reads see it?
- Picture one primary DB (takes writes) copying to replicas (serve reads).

**1. Strong consistency** — a read _always_ sees the latest write, immediately.
- How: the write isn't "done" until every replica confirms it (or all reads go to the primary). The read waits if needed.
- Cost: **latency** — you pay the round-trip to sync before anyone can read. During a partition it becomes CP (refuse rather than serve stale).
- Use when stale = damage: **billing balance, quota counter, inventory.**

**2. Eventual consistency** — replicas catch up "soon" (usually milliseconds). A read right after a write _might_ be stale.
- How: write returns as soon as the **primary** has it; replicas sync in the background.
- Cost: **a brief stale window.** Cheap and fast and highly available (AP).
- Use when stale-for-a-moment is harmless: 
	**your Shutterabia D1 dashboard mirror**, view counts, search results.

**Read-your-writes consistency** 
the middle ground: **you** always see **your own** writes instantly; _other_ people may lag.

- The problem it fixes: you edit your bio, hit save, the page reloads from a **stale replica** → your change vanished → you panic and save again. Bad UX even though the data was fine.
- How: route _your_ reads to the primary (or the replica that has your write) for a short window after you write; everyone else reads normal replicas.
- It's eventual consistency **plus a personal guarantee**. Cheap win, huge UX improvement.
- Shutterabia fit: SMM approves a draft → their next dashboard load must show it "approved" even if a colleague's screen lags a second.

strong = everyone fresh always (slow)
eventual = everyone fresh soon (fast, stale window)
read-your-writes = _you_ fresh now, others soon (cheap fix for the "my edit disappeared" bug).

----
### The nines (availability)
Availability = **% of time the system answers**.
Measured in "nines" = how many 9s in that percentage.

What matters is the **downtime that percentage allows per year:**
|Availability|Name|Downtime / year|Downtime / day|
|---|---|---|---|
|99%|"two nines"|~3.65 days|~14 min|
|99.9%|"three nines"|~8.75 hours|~86 sec|
|99.99%|"four nines"|~52 min|~8.6 sec|
|99.999%|"five nines"|~5.25 min|~0.86 sec|

- Each extra nine = **~10× less downtime** — and usually a lot more money (redundancy, failover, on-call). 
- You don't chase nines for free.
- series (dependencies) _costs_ you nines; 
- parallel (redundancy) _buys_ them back
