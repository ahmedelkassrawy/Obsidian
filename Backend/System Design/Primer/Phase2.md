This phase is one story:
**what happens between a user typing a URL and your code running.**

Each box does one job , we follow a request from the browser inward
```
User → DNS → CDN → Load Balancer → Reverse Proxy → App servers → DB
```

1. DNS - the phone book
Domain Name System: turns a name (`shutterabia.com`) into an IP address (`1.2.3.4`). Your browser can't dial a name, only a number.

- The browser asks a DNS resolver "what's the IP for this name?" → gets back an address → _then_ connects.

- Why it matters for design:
		DNS can also **load-balance** — return different IPs to different users (round-robin, or geo-based: send a user to the nearest data center).

- **Cost:** the first lookup adds latency (~tens of ms), so results are **cached** (in your OS, browser, and resolvers) with a **TTL** (time-to-live)
	- Change your IP and old clients keep hitting the stale one until TTL expires.
	
- **Shutterabia tie:** the name that points at your Mac server resolves through DNS; Cloudflare sits on that name.

2. CDN - copies near the user
Content Delivery Network: a global network of edge servers that cache your **static** content (images, JS, CSS, video) physically close to users.

A user in Cairo hits a Cairo edge, not your Mac across the world → much lower latency.

- **Pull** — the CDN fetches from your server on the first request for a file, then caches it. Lazy, self-managing. Most common.
- **Push** — you upload files to the CDN yourself. You control what's there, good for large rarely-changing files.

**Only for static/cacheable content.** 
A personalized API response or a live tool call can't be cached at the edge — that goes to your app.

**Shutterabia tie:** Cloudflare is your CDN/edge layer.
Static dashboard assets are cached; the actual `/mcp` tool calls pass through to the Mac.

3. Load Balancer - the traffic cop
Sits in front of your app servers and spreads incoming requests across them, so no single server is overwhelmed.

**Why it exists:** 
- This is the _parallel redundancy_ from the nines lesson.
- Multiple app servers behind an LB = you're only down if all fail, and you can add servers to scale horizontally.

**How it picks a server:** 
- round-robin (next in line) 
- least-connections (send to the least-busy) 
- or by response time.

**L4 vs L7** — the one real design distinction:
- **L4** (transport layer) routes by IP/port only. Fast, dumb, doesn't look inside the request.
- **L7** (application layer) reads the actual HTTP — can route `/api` to one pool and `/images` to another, do SSL termination, inspect headers. Smarter, slightly slower.

Health checks
the LB pings each server; a dead one gets pulled out of rotation automatically.

**It needs redundancy too** — a single LB is a single point of failure, so production runs **active-passive** (a standby LB takes over if the primary dies).

4. Reverse Proxy — the front door
a server that recieves reqeuests and forwards them to the backend , then returns the backend's response -- the client never talks to your app directly

- Sounds like a load balancer, and they overlap
a load balancer is one kind of reverse proxy.
- **Load balancer** = "spread load across _many_ servers" (its whole point is multiple backends).
- **Reverse proxy** = "a single front door" — useful **even with one backend**: it does SSL termination, compression, caching, hides your server's real IP, and blocks bad requests.

- nginx is the classic example - often does both jobs
- **Shutterabia tie:** Cloudflare also acts as a reverse proxy — it hides your Mac's real IP and terminates HTTPS before traffic reaches you.

5. App Layer -- your actual code
- Where your business logic runs — the FastAPI/MCP handlers, the tool calls.
- The layer everything else exists to protect and feed.

**Keep it stateless** — no session data stored on the server itself (put that in a DB or Redis).
	Why?
	if every server is identical and stateless, the LB can send a request to _any_ of them, and you can add/remove servers freely. 
	This is what makes horizontal scaling _work_.

**Microservices vs monolith:**
	one big app (simple, what Shutterabia is) 
	vs 
	many small services each owning one job (scales teams + independent deploys, but adds network hops and complexity).

**Service discovery:** when you _do_ split into services, they need to find each other's addresses — a registry (like Consul) tracks "which service is at which IP right now."

[!tip]
The through-line  
Every box exists for one of two reasons: **get closer to the user** (DNS geo-routing, CDN edge) or **survive a server dying** (LB + stateless app + redundant proxy). That's the whole layer.