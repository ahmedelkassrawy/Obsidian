# Sanad Squad: Interview Prep

**Interview:** Monday 5 October 2026, 2:00 PM Cairo, Google Meet (link in Ahmed's email)
**With:** Ahmed Khalid (Al-Qa'qa', CTO) and Mohamed Aboyounes (0xFrankCastle, CEO)
**Format:** short call about your background and "the agent work you have built," plus your questions.
**Role you applied for:** AI Engineer (not the Blockchain Engineer post).

---

## 0. Tonight's checklist

- [ ] Reply to Ahmed's email to confirm the time (if you haven't).
- [ ] Check your university timetable against **12:00–16:00 Cairo core hours**. Have a plan for any clash.
- [ ] Read Al-Qa'qa''s post on sanadsquad.com: "x402 Agentic payment flow, end to end" (Sept 5, 2026).
- [ ] Skim "Five Attacks on x402": https://arxiv.org/html/2605.11781v1
- [ ] Build the small x402 demo (section 3) and push it to GitHub.
- [ ] Install safe-solana-builder and try it once: https://github.com/Frankcastleauditor/safe-solana-builder
- [ ] Open one of Al-Qa'qa''s audit reports (github.com/Al-Qa-qa/audits) to see what a finding looks like.
- [ ] Walk through the Meta MCP repo (section 6) until you can draw the publish flow on paper.
- [ ] Say your 60-second intro out loud three times.
- [ ] Test Meet, camera, mic. Join 5 minutes early.

---

## 1. The company in one minute

Sanad Squad is a security firm for **blockchain and AI financial systems**. They say they've done 100+ audits.

Five services:
1. **Blockchain security audits**: line-by-line smart contract review, helped by "AI audit agents."
2. **Penetration testing**: web apps, APIs, blockchain infrastructure, SDKs.
3. **Agentic security tooling** (your job), three kinds of tool:
   - **Detectors**: AI agents trained on a client's protocol that catch bugs as they're introduced.
   - **PR reviewers**: review pull requests for new problems.
   - **Monitoring agents**: watch contract transactions live and flag odd activity before money moves.
4. **Agentic payments** (also your job): they build and secure AI agents and MCP servers that get paid per call through **x402** and **MPP**.
5. **Security consulting**: design review before development.

Pricing is fixed-price per scope. Tool engagements include 3 months of support after delivery.

Their whole pitch: *"Build the security layer for agentic finance."*

They're very early. The blog has one post, and the rest says "coming soon." They're hiring four roles at once: Blockchain Engineer, AI Engineer, Growth/BD Lead, and Content Creator.

---

## 2. The founders

### Mohamed Aboyounes = 0xFrankCastle (CEO)
- Rust and Solana security researcher: Anchor, Pinocchio, native Rust programs.
- Track record: 60+ Rust audits, 50+ Solana audits, 300+ critical/high findings. Audited Pump.fun, Synthetix, Lido, GMX, LayerZero and the Anchor framework.
- **Built safe-solana-builder**, "the first Claude skill for writing production-grade, security-first Solana programs" (145 stars). It loads his audit knowledge into Claude before it writes code: framework choice, risk level, security rules from real findings, a project scaffold, and test skeletons with edge cases.
- Runs **Solana Audit Arena**: a free weekly contest where he drops a new Anchor program every Monday and people hunt for bugs.
- Has run 0xCairo CTFs and mentors in Solana security bootcamps.
- **Tanta University, B.Eng., AI Department. Your university and your department.**
- X: @0xcastle_chain · GitHub: Frankcastleauditor

### Ahmed Khalid = Al-Qa'qa' (CTO). Confirmed.
- EVM and Solidity security researcher, "from single contracts to full systems, plus agentic tooling."
- Track record: 50+ audits, 250+ high/medium findings. Active on Code4rena, Sherlock and CodeHawks (2nd place UniStaker, 3rd PoolTogether, 4th DYAD on C4).
- Wrote a web3 security tutorial (107 stars) and Ethernaut CTF solutions in Foundry.
- **Wrote their only blog post: x402 end to end.** He sent your invite.

### How to handle each one
- **Frank:** bring up the Tanta connection *once*, lightly, early. Talk about his Claude skill. Ask how he went from an AI degree to Solana security. Expect sharp questions, because he knows what the department does and doesn't teach.
- **Al-Qa'qa':** talk x402 and payments security. Show you read his post.

---

## 3. x402 and MPP: what you must know

### x402 (Coinbase, 2025)
Named after the HTTP status code **402 Payment Required**. The flow:
1. The agent requests a resource (an API or MCP tool).
2. The server replies **402** with payment requirements: price, token, address, network.
3. The agent signs a payment (USDC, usually an EIP-3009 `transferWithAuthorization`) and resends the request with an `X-PAYMENT` header.
4. A **facilitator** checks the signature, checks the nonce hasn't been used, and settles on-chain.
5. The server returns the resource.

No accounts, no API keys, no checkout page, and it takes well under a second.

### MPP: Machine Payments Protocol (Stripe + Tempo)
- Launched **March 18, 2026**, the same day Tempo's payments blockchain went live. Streaming payments were added April 2026.
- Built on the same 402 handshake, but adds a full lifecycle: price discovery, authorization, subscriptions and reconciliation. It works across stablecoins, cards and buy-now-pay-later.
- **The big idea is sessions.** The agent approves a spending limit once, then streams small payments against it without an on-chain transaction per call.
- Backed by Visa, Mastercard, OpenAI and Shopify. About 30k transactions by August 2026.
- **One-line difference:** x402 means one payment per request, crypto-native. MPP means a session with a spending cap, and it works with cards and crypto.

### What breaks: Sanad's own risk list for paid agents
1. **Replay and unauthorized calls**: the same payment reused to get access twice.
2. **Fake requests**: forged or invalid payment proofs.
3. **Prompt injection**: a paying user manipulates the agent into refusing real work or doing something it shouldn't.
4. **Load and abuse**: one malicious request takes the agent down.
5. **Facilitator integration**: reading on-chain data wrong, or matching a payment to the wrong request.

From the "Five Attacks on x402" paper:
- **Optimistic execution**: the server hands over the resource before the payment is final.
- **Payment not tied to the caller**: someone watching the network uses your payment authorization first.
- **Replay at the HTTP layer**: one `X-PAYMENT` payload unlocks the resource several times if the server doesn't **record the payment ID atomically before releasing the resource**.

**Your bridge:** this is the same bug class you fixed in your Meta MCP (ADR 0014, claim before publish). See section 6.

### The demo to build today (3–4 hours with Claude Code)
- A Python FastAPI or MCP server with **one tool behind x402**, on **Base Sepolia** (a test network).
- One protection from their list: **insert the payment ID under a unique constraint before releasing the resource**, so a replayed payment gets rejected.
- A README listing the attacks you considered and which ones you handled.
- What it lets you say: "I built this yesterday to understand your service."

---

## 4. Security words to recognize (no need to audit)

**EVM / Solidity**
- **Reentrancy**: an external call re-enters your contract before its state is updated. Fix: update state first, then make the external call ("checks-effects-interactions").
- **Access control**: a privileged function that anyone can call.
- **Oracle manipulation**: a price read from an on-chain pool that someone pushes around with a flash loan.
- **Unchecked external calls / rounding / precision loss.**

**Solana / Rust** (Frank's list)
- **Missing signer check**: the program doesn't confirm the account actually signed.
- **Missing owner check**: the program trusts an account owned by the wrong program.
- **Non-canonical PDA bump**: accepts a user-supplied bump, so fake derived addresses get through.
- **Stale account data after a cross-program call (CPI)**: reads data that the other program just changed.
- **Duplicate mutable accounts**: the same account passed twice as two different roles.
- **Unchecked arithmetic**: overflow and underflow.

**What an audit finding contains:** title, severity, description, impact, proof of concept, recommended fix.

---

## 5. Your 60-second intro

> "I'm Ahmed, a final-year AI engineering student at Tanta. For the past two years I've built agents that take real actions, not just chat: a hospital admin agent with a live voice line that reads and writes a Postgres database, a support agent with retries and escalation, a multi-tenant RAG system where keeping each client's data separate was the whole design problem, and, most recently, a publishing and ads system for a social media agency where an agent posts and spends money for real clients behind human approval gates and spending caps. I build in Claude Code and Codex every day with my own skills and MCP servers. Sanad interests me because agents are starting to hold money, and the problems I keep hitting, like what a tool is allowed to do, when a human must approve, and what happens when a request is retried, become security problems with a dollar amount attached."

**Your thesis (come back to it every time):** *agents that touch money need permissions, approval gates and idempotency, and that's what I've been building.*

---

## 6. Your headline project: the Meta MCP server (Shutterabia)

**How to say how it was built (honest and confident):**
> "I designed it and built it by directing Claude Code. I didn't write the code by hand, but every design decision is mine. I wrote them down as 17 decision records."

### What it is
A TypeScript **MCP server** that lets a non-technical Social Media Manager publish and schedule posts for many client brands on Facebook, Instagram (and Google Business, LinkedIn, TikTok, YouTube) through a Claude chat, without ever touching tokens. A separate **Ads module** lets an agent read ad performance and, behind a strict gate, create and edit ads that spend real money.

### Size (as of Aug–Sep 2026)
- About **350 commits**, started **July 2026**, merged through numbered PRs (PR #105 by Aug 12).
- About **28k lines of TypeScript**, **112 test files** (Vitest), **17 decision records** (ADRs) plus numbered plans.
- Runs as two processes on a Mac (the MCP server and a scheduler daemon) on one SQLite database. There's also a **Cloudflare Worker** backup and a **dashboard** (Cloudflare D1 mirror).

Note: it's **TypeScript**, but your CV lists only Python. Say it out loud: "my biggest project is TypeScript."

### How a post gets published
```
stage_draft  ->  human says "yes" in chat  ->  approve_draft  ->  create_post / schedule_post
   (draft)                                       (approved)         refuses unless status = approved
```
- `create_post` and `schedule_post` **refuse** any draft that isn't `approved`.
- Every step is written to an audit log (`publish_log`).

### The five security decisions to explain

**1. Claim before publish (ADR 0014). This is your x402 bridge.**
- *Problem:* the duplicate check read the database and *then* published. The server and the scheduler are two processes on one SQLite file, so two calls could both pass the check and **post twice on a client's page**.
- *Fix:* **insert a row with status `publishing` before any network call.** A **unique index on (draft_id, platform)** for active rows means the database itself enforces "only one." The losing call gets a typed `DuplicatePublishError` and **never contacts Meta.**
- *Detail auditors will like:* a stuck `publishing` row is **never auto-cleared on a timeout**, because "the process died" and "the call is still running" look identical. Auto-clearing would bring the double-post back. A human cancels it instead.
- *How to tell it:* "That's the same bug class as x402 replay: record the payment ID atomically before releasing the resource."

**2. The six-step gate for ad spending (ADR 0012).**
The steps: bind to one ad account, then propose the exact change, then show a **cost preview in real dollars**, then run the **spend ceiling check**, then get an **explicit "yes" for that one action**, then execute, read the result back from Meta, and record it.
- **"No ceiling means no write."** A missing ceiling is a hard refusal, never "unlimited" (`src/ads/ceilings.ts`). Ceilings exist per account and per change, over daily, weekly or monthly rolling windows.
- **One yes = one write.** No standing approval.
- Tools come in tiers. Irreversible deletes need a stronger double confirmation.
- Fixed rules: the agent **never launches spend unattended** and **never drives Ads Manager in a browser.**
- *Bridge:* this is the same idea as **MPP sessions**: a pre-approved spending limit that every action must fit under.

**3. Self-healing ads loop (ADR 0011): the agent decides, a human executes.**
- A human approves a **Campaign Envelope** once (budget cadence, ceiling, target ROAS or CPA, allowed fixes). A loop then detects problems and proposes bounded fixes. The executor (`AttendedAdapter`) **never calls Meta itself.** A human or attended Claude runs it, and the result gets recorded. Failures increase a counter, and too many escalate to a human.
- **You rejected LangGraph** here (and for analytics, ADR 0010): it adds a second LLM layer, needs an always-on Python runtime and a paid API key, and is built for *no-human* loops. You already had a tested loop in TypeScript. Good judgment story: "I know LangGraph, it's on my CV, and I chose not to use it."

**4. Observability (ADR 0008).**
- One wrapper intercepts every tool registration, so **every tool call is traced**: tool, run ID, brand, ok or error, duration, **redacted** arguments. Tracing can never break a tool call.
- You were honest about the limit: the model's reasoning stays inside claude.ai. You can only see the tool calls that hit *your* server. Ads reads go to Meta's own connector, so **a forbidden write by the ads agent would be invisible to you.**
- You chose observability first and put off a full eval harness on purpose.

**5. Secure defaults.**
- The HTTP transport **refuses to start without a bearer token** unless you explicitly set `MCP_ALLOW_UNAUTHENTICATED=true` ("fail closed").
- The Cloudflare backup only publishes if the Mac's heartbeat has gone silent, so the two can't race. On restart, the Mac reconciles what the Worker already published so nothing is published twice.
- Facebook "drift" reconcile: Meta is the source of truth, and the sync only goes Meta → us, never the other way.
- Captions are vision-gated (ADR 0005): Claude must *see* the image (or 3 frames pulled from a video with ffmpeg) before writing a caption.

### Weak spots: raise them yourself before they find them
1. **Approval is behavioral, not structural.** `approve_draft` is a tool the *model* calls after the human says yes. The database enforces the order (no publish without `approved`), but it **can't prove a human actually said yes.** A prompt-injected or confused model could approve on its own.
   *Better design (say this):* approval comes through a channel the model can't reach, like a dashboard button or a signed one-time approval token. The dashboard has an approve command, which is the start of that.
2. **The spend ceiling only covers what's recorded.** Ad writes go through Meta's connector, which your server can't intercept, so the ceiling relies on the agent calling `record_ad_write`. To make it airtight, the write itself would need to go through your server.
3. **The dashboard login is one shared password** with no user roles (noted in ADR 0008).

Saying these out loud is the strongest move you have. It shows you think like an auditor about your own work.

### Know it well enough to draw
Tonight, open the repo in Claude Code and ask it to walk you through:
- `src/tools/approve_draft.ts` → `src/tools/create_post.ts` (the approval check, then the claim row)
- `src/db/index.ts` (look for `DuplicatePublishError`) and the unique index in `schema.sql`
- `src/ads/ceilings.ts` and `src/tools/record_ad_write.ts`
- `src/server.ts` (`resolveAuthMode`)

---

## 7. Your other projects: hooks and traps

| Project | Connect it to their work | Have this answer ready |
|---|---|---|
| **Multi-Tenant RAG** | Keeping tenants separate = access control | "How did you prove 100% isolation?" Was the org ID taken from the JWT on the server, never the request? Separate store per org? A test showing org A can't read org B? **If there's no test, say "designed for full isolation," not "100%."** |
| **Customer Support Agent** | Celery retries → **idempotency** → x402 replay | "How do you stop a retry from doing the action twice?" |
| **Hospital agent** | An LLM with **write access** to a real database | "How did you stop the model from writing a wrong record?" Fixed tool schemas, parameterized SQLAlchemy queries (no SQL written by the model), validation, confirming before writing. If it wasn't complete, say what you'd add now. |
| **Voice pipeline under 500ms** | Less relevant | One sentence. |
| **DEPI internship** | Low priority | One line. They care about what you built yourself. |

**Every number on your CV** (40%, 60%, 30%, 2x, 100%, 50+ users): know how you measured it, or soften it. These two review claims for a living.

---

## 8. Questions they'll probably ask

1. **"Walk us through an agent you built."** Use the Meta MCP: claim before publish, the six-step gate, then the weak spot you'd fix.
2. **"How do you use Claude and Codex day to day?"** Be specific: your own skills, CLAUDE.md rules, subagents, isolated worktrees, **a separate review agent so the model that wrote the code never approves it**, tests before merge, ADRs before code. Your `/ship` loop: issue → grill → plan/ADR → worktree → independent review → tests → PR.
3. **"How would you build an AI PR reviewer or bug detector for us?"** (2-minute sketch)
   - Input: the diff plus the contracts it touches.
   - Check it against a list of bug types drawn from **their own past findings** (the safe-solana-builder idea).
   - **Require a failing test or proof of concept before reporting**, so it doesn't flood them with false alarms.
   - A human sorts the results.
   - **Measure it on Solana Audit Arena programs, where the bugs are already known**, and track how many real bugs it catches versus false alarms.
4. **"What do you know about x402 and MPP?"** Section 3, plus your demo.
5. **"You have no blockchain experience."** Agree. Point to the demo. "My job here is AI tools, and I'll learn the security side the way I learned agents: by building."
6. **"Can you handle the risk: an unpaid trial and pay that's mostly a share?"** Be honest. Then ask what the trial will produce.
7. **"Can you be online 12–16 Cairo every day?"** Have your timetable answer ready.
8. **"Why security / why us?"** Your thesis from section 5.

---

## 9. Your questions for them

1. What exactly should the two-week trial produce? (They promise to write it down. Ask what it usually looks like.)
2. What's the retainer amount, and how is the profit share calculated?
3. Which AI tools exist today, and which are you building next?
4. Is the x402/MPP agent service a product you own, or client work?
5. Which models and what API budget would I have? Are Claude and Codex subscriptions covered?
6. **To Frank:** how did you go from Tanta's AI department to Solana security?
7. **To Al-Qa'qa':** what's the most common bug you see in x402 servers so far?

---

## 10. Things to say in the call (lines to remember)

- "I designed it and built it by directing Claude Code. Every decision is mine. I wrote down 17 of them."
- "Record the ID before releasing the resource. That's my claim-before-publish fix, and it's x402 replay protection."
- "No ceiling means no write."
- "One yes, one write."
- "The weak spot I'd fix first: approval comes from the model calling a tool. It should come through a channel the model can't reach."
- Offer: "During the trial I could write a post like 'Securing an x402 MCP server: what I found building one.'" (Writing matters to them.)

---

## 11. My view of the opportunity

**Good:** the founders are real and their audit records are public and serious. They're already shipping AI tools (Frank's Claude skill). The role fits you well: you'd be the person turning their security knowledge into AI products. Same university as the CEO.

**Risks:** the two-week trial is unpaid, and most of your income would come from a project or profit share, not the retainer. The company looks very early (one blog post, four roles being hired at once). Daily core hours may clash with your final year.

**How to handle it:** go in keen but clear-eyed. Get the retainer number and the written trial goals before you start.

---

## Not verified
- Repo numbers come from the local `main` checkout of `meta-mcp-server` (last commit 2026-08-12). Worktrees from September may have more.
- x402 and MPP facts come from public articles (WorkOS, Eco, Alchemy, arXiv), not from running either protocol.

## Sources
- https://sanadsquad.com/ (services, careers)
- https://github.com/Frankcastleauditor · https://x.com/0xcastle_chain
- https://github.com/Al-Qa-qa · https://code4rena.com/@Al-Qa-qa · https://audits.sherlock.xyz/watson/Al-Qa-qa
- https://workos.com/blog/x402-vs-stripe-mpp-how-to-choose-payment-infrastructure-for-ai-agents-and-mcp-tools-in-2026
- https://eco.com/support/en/articles/14845486-stripe-machine-payments-protocol-mpp
- https://arxiv.org/html/2605.11781v1 (Five Attacks on x402)
- https://www.alchemy.com/overviews/agentic-payments-x402-explained
- Local: `D:\me\Shutterabia\meta-mcp-server` (README, CONTEXT.md, docs/adr 0005/0008/0011/0012/0014, src/tools, src/ads/ceilings.ts, src/server.ts)
