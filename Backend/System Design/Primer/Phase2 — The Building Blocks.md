---
tags: [backend, system-design, dns, cdn, load-balancer, reverse-proxy, networking]
domain: backend
type: lesson-note
status: digested
source: System Design Primer — Phase 2 (Building Blocks); Kassra growth-track session 2026-09-16
---
# The Building Blocks

One story: **what happens between a user typing a URL and your code running.** Each box does one job. We follow a request from the browser inward.

```text
User → DNS → CDN → Load Balancer → Reverse Proxy → App servers → DB
```

## 1. DNS — the phone book

> [!definition] DNS
> Domain Name System: turns a name (`shutterabia.com`) into an IP address (`1.2.3.4`). The browser can't dial a name, only a number.

- The browser asks a DNS resolver "what's the IP for this name?" → gets back an address → *then* connects.
- **Why it matters for design:** DNS can also **load-balance** — return different IPs to different users (round-robin, or geo-based: send a user to the nearest data center).
- **Cost:** the first lookup adds latency (~tens of ms), so results are **cached** (OS, browser, resolvers) with a **TTL** (time-to-live). Change your IP and old clients keep hitting the stale one until TTL expires.
- **Shutterabia tie:** the name that points at the Mac server resolves through DNS; Cloudflare sits on that name.

## 2. CDN — copies near the user

> [!definition] CDN
> Content Delivery Network: a global network of edge servers that cache your **static** content (images, JS, CSS, video) physically close to users.

- A user in Cairo hits a Cairo edge, not the Mac across the world → much lower latency.
- **Two flavors:**
  - **Pull** — the CDN fetches from your server on the first request for a file, then caches it. Lazy, self-managing. Most common.
  - **Push** — you upload files to the CDN yourself. You control what's there; good for large, rarely-changing files.
- **Only for static/cacheable content.** A personalized API response or a live tool call can't be cached at the edge — that goes to your app.
- **Shutterabia tie:** Cloudflare is the CDN/edge layer. Static dashboard assets are cached; the actual `/mcp` tool calls pass through to the Mac.

## 3. Load Balancer — the traffic cop

> [!definition] Load Balancer
> Sits in front of your app servers and spreads incoming requests across them, so no single server is overwhelmed.

- **Why it exists:** this is the *parallel redundancy* from the nines lesson. Multiple app servers behind an LB = you're down only if all fail, and you can add servers to scale horizontally.
- **How it picks a server:** round-robin (next in line), least-connections (least-busy), or by response time.
- **L4 vs L7** — the one real design distinction:

| | Layer | What it sees | Trade-off |
|---|---|---|---|
| **L4** | transport | IP / port only | fast, dumb, can't read the request |
| **L7** | application | the actual HTTP | can route `/api` vs `/images`, SSL terminate, read headers; slightly slower |

- **Health checks:** the LB pings each server; a dead one is pulled from rotation automatically.
- **It needs redundancy too** — a single LB is a single point of failure, so production runs **active-passive** (a standby LB takes over if the primary dies).

## 4. Reverse Proxy — the front door

> [!definition] Reverse Proxy
> A server that receives requests and forwards them to your backend, then returns the backend's response — the client never talks to your app directly.

- Overlaps with a load balancer — **a load balancer is one kind of reverse proxy.** The distinction:
  - **Load balancer** = "spread load across *many* servers" (its whole point is multiple backends).
  - **Reverse proxy** = "a single front door" — useful **even with one backend**: SSL termination, compression, caching, hides your server's real IP, blocks bad requests.
- **nginx** is the classic example — often does both jobs at once.
- **Shutterabia tie:** Cloudflare also acts as a reverse proxy — hides the Mac's real IP and terminates HTTPS before traffic reaches you.

## 5. App Layer — your actual code

> [!definition] App Layer
> Where your business logic runs — the FastAPI/MCP handlers, the tool calls. The layer everything else exists to protect and feed.

- **Keep it stateless** — no session data on the server itself (put it in a DB or Redis). If every server is identical and stateless, the LB can send a request to *any* of them and you can add/remove servers freely. This is what makes horizontal scaling *work*.
- **Microservices vs monolith:** one big app (simple — what Shutterabia is) vs many small services each owning one job (scales teams + independent deploys, but adds network hops and complexity).
- **Service discovery:** when you split into services, they need to find each other's addresses — a registry (like Consul) tracks "which service is at which IP right now."

> [!tip] The through-line
> Every box exists for one of two reasons: **get closer to the user** (DNS geo-routing, CDN edge) or **survive a server dying** (LB + stateless app + redundant proxy).

## How to trace a request (the method)

At each box ask 4 questions:
1. **Static or dynamic?** Static (image/CSS) → the CDN can answer it. Dynamic (an *action* like approving a draft) → must reach your code. This one decision skips or keeps whole boxes.
2. **Does it need a name resolved?** Only the *first* hop to a new domain hits DNS; after that it's cached.
3. **Does it need to survive a server dying / pick a server?** → load balancer / reverse proxy.
4. **Where does the work happen?** → app layer → DB.

Then walk the boxes in order and label each **HITS / SKIPS + why**.

## Worked trace — SMM approves a draft (Gate 2, passed 2026-09-16)

Approving a draft is a **dynamic action that changes data (a write)** — so a CDN edge can't cache it; it must run the code on the Mac.

```text
Browser
 → DNS (resolve name → Cloudflare IP; cached after 1st request)
 → Cloudflare CDN (PASS-THROUGH — dynamic write, nothing to cache)
 → Cloudflare reverse proxy (HTTPS terminate, hide Mac IP, forward)
 → [no LB — single Mac server]
 → App on Mac (MCP tool: approve draft)
 → DB app.db (write: status = approved)
 → response back up the same chain
```

| Box | This request | Why |
|---|---|---|
| DNS | HITS (once) | need the IP behind the domain; cached after |
| CDN | PASS-THROUGH | dynamic write — nothing to cache, just forward |
| Load balancer | SKIPPED | only one Mac server; no load to spread |
| Reverse proxy | HITS | Cloudflare: SSL terminate, hide Mac IP, forward |
| App (Mac) | HITS | MCP tool flips the draft to approved |
| DB (`app.db`) | HITS | the write lands here |

> [!warning] The trap
> The same box behaves differently per request. Cloudflare **caches** a dashboard logo but **passes through** an approve-draft click. Always ask "static or dynamic?" first — it decides whether the CDN *works* or just *forwards*.

> [!success] Phase 2 done
> Own: the request path box-by-box, L4-vs-L7, reverse-proxy-vs-load-balancer, stateless app layer, and how to trace a real request (static-vs-dynamic decides everything). **Next: Phase 3 — data at scale (replication, federation, sharding, SQL vs NoSQL).**
