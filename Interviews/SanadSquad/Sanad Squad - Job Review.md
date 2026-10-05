---
description: "Everything about the Sanad Squad AI Engineer opportunity: what the company does, the founders, the first interview and its recap, the pay, the advice on whether to take it as a second job, and how to pass the two-week trial."
domain: career
type: interview
status: digested
tags:
  - domain/career
  - type/interview
  - status/digested
  - topic/interviews
hubs:
  - "[[Interviews]]"
---
# Sanad Squad: Job Review

> [!info] Where this came from
> A prep and debrief conversation with Claude, 4–5 October 2026. The detailed cheat sheet for the first interview is in [[Sanad-Squad-Interview-Prep]].

## Timeline
- **2026-10-03:** Ahmed Al-Qa'qa' invited me to a first interview for the **AI Engineer** role.
- **2026-10-04:** Prep day. Researched the company, read my own repos, rehearsed answers.
- **2026-10-05, 2:00 PM Cairo:** First interview with both founders. They sent a written recap afterwards.
- **Next:** the two-week unpaid trial (goals to be written down before it starts).

---

## What the company does (in simple words)

Sanad Squad is a team of security experts who get paid to **find bugs before hackers do**, in code that holds money.

1. **Smart contracts.** A smart contract is a small program on a blockchain that holds money and follows fixed rules, like a vending machine. Once it's live, a bug can't easily be fixed, and whoever finds it first can drain the money. Companies pay Sanad to **audit** the code before launch. Sanad finds the bugs, shows how they could be exploited, and suggests the fix. The client applies it, and Sanad checks the fix works. 100+ audits so far.
2. **AI agents that pay for things (the new market).** Agents are starting to pay for services by themselves. **x402** and **MPP** are the rules for how those payments happen, like a card terminal for robots. That opens new ways to cheat (reusing one payment many times, tricking the agent with sneaky messages). Sanad wants to be the firm that builds these paying agents and secures them.

Their pitch: *"Blockchain security and agentic payments are now one problem."*

**How they make money:** fixed-price audits; custom AI tools for clients (bug detectors, AI code reviewers, monitoring agents); and their own products, which is where the project share comes from.

### What they want from me
They're two very skilled auditors, and their time limits how much they can earn. They want **AI to multiply their expertise**: turn what they know about bugs into tools that find them automatically, both to speed up their own audits and to sell as products. I'm the builder for that, not another auditor.

> "You audit smart contracts and now agentic payments, finding the holes before hackers do. You want AI tools that turn your audit knowledge into software, to speed up your own reviews and to sell as products. I'd be the person building those."

---

## The founders
- **Mohamed Aboyounes = 0xFrankCastle (CEO).** Rust/Solana security researcher: 60+ Rust audits, 50+ Solana audits, 300+ critical/high findings (Pump.fun, Synthetix, Lido, GMX, LayerZero, Anchor). Built **safe-solana-builder**, a Claude skill for writing secure Solana programs. Runs **Solana Audit Arena**, a free weekly bug-hunting contest. **Studied at Tanta University, AI Department, same as me.**
- **Ahmed Khalid = Al-Qa'qa' (CTO).** EVM/Solidity auditor: 50+ audits, 250+ high/medium findings, active on Code4rena, Sherlock and CodeHawks. Wrote their x402 post (the blog link was broken as of 2026-10-04).

---

## x402 and MPP in one minute
- **x402** (Coinbase): the server replies "402 Payment Required" with a price, the agent pays in USDC, a "facilitator" checks and settles the payment, and the server returns the result. One payment per request.
- **MPP** (Stripe + Tempo, launched March 2026): same idea, but the agent approves a **spending limit once (a session)** and then streams small payments against it. Works with cards and crypto.

**The coffee-shop version of replay protection.** A payment proof is a paid receipt with a serial number. A cheater photocopies one receipt ten times. The fix is to keep a notebook of used serial numbers: check the receipt is real, write its number down, **then** make the coffee, and never serve the same number twice. Write it down *before* serving, otherwise two copies arriving at the same moment both get coffee. Also tie the receipt to the item ("5 cents, for coffee") so a cheap payment can't buy a cake.

---

## What happened in the interview (from their recap)
- **Background:** I walked through four previous roles working on AI agents and the tools I've used, including LangGraph.
- **Harness vs multi-agent:** I argued that an **orchestration approach is better than a free-form multi-agent system**, with examples.
- **Solana vulnerability agent:** we discussed an agent that detects Solana vulnerabilities, using several agents under an orchestrator to find more issues, plus **token consumption** and **harness design** tradeoffs. **This is probably what they want built, and a likely trial project.**
- **x402:** how agents can pay each other.
- **Resources they sent:** Awesome Agentic Commerce, x402.org, x402scan (analytics on agents paying with x402), mppscan (the same for MPP).

### My self-assessment, and the honest read
I felt my projects came out weak because it was all improvised on camera with no notes. But the recap shows they spent the time going deep on design questions with me and then sent pay details and reading material. People don't do that with candidates they've ruled out. It probably felt worse than it looked. Thinking out loud without notes is close to the real job anyway.

### My open technical worries
Token budgets, orchestrator vs harness, keeping agents under control, deploying agents on AWS, and whether I can build this agent. These are learnable and are exactly what the trial tests. I already work inside an agent harness daily (Claude Code with subagents, skills and limits). What's missing is applying it to *their* problem. **Sketch the Solana agent design on one page before the trial starts.**

---

## The offer
| Item | Detail |
|---|---|
| Months 1–3 | 7,500 EGP / month |
| Months 4–6 | 10,000 EGP / month |
| Months 7–9 | 12,500 EGP / month |
| Month 10 onward | 15,000 EGP / month |
| Yearly bonus | Up to 25,000 EGP, after completing 12 months |
| Project share | A percentage of the projects I work on. **The percentage will be discussed later.** |
| Trial | Two weeks, **unpaid**. Either side can stop with nothing owed. |
| Hours | Deadline-based. **Core hours 12:00–16:00 Cairo**: online and reachable (like office hours, so anyone can talk without scheduling). Flexible for a valid reason like a lecture. |

Year one salary adds up to **135,000 EGP**, plus a bonus of up to 25,000 EGP, plus the project share.

**Still open:** the project share percentage and how it's calculated (get it in writing), and what decides the bonus amount.

---

## Should I take it as a second job?

**My situation:** Shutterabia (deadline-based, meetings only when needed, fine with me having another job but makes no exceptions for it), final year at Tanta, and my own career study.

**The real cost is time, not skill.** Being reachable 12–4 on working days plus delivering the work, on top of Shutterabia, university and self-study, means something will give, usually grades or sleep first. The 7,500 EGP start alone doesn't justify that load.

**What justifies it:** daily work with two serious auditors in a rare combination (AI agents + security + payments), a salary that doubles within a year, a project share, and real new learning. Shutterabia has become routine delivery: replacing backend/frontend work on fast deadlines, nothing new. Sanad is where I'd grow.

**Decision: try the trial, with conditions.**
1. **Shutterabia is the one to shrink over time**, but **not before** Sanad is real. Keep it as steady income until there's an offer and a month or two of seeing how Sanad runs.
2. **Keep both jobs' deadlines in one calendar** so two big deliveries don't land in the same week.
3. **Tell Sanad about Shutterabia in writing before the trial.** It isn't betrayal. Their own job post requires it ("tell us in writing before you start"), and hiding it is what would break trust. No confidential details needed:
   > "Before the trial starts, I want to mention that I also work part-time, with flexible hours, as an AI/backend engineer for a social media agency, and I'm in my final year at university. I've planned my time so I can meet your deadlines and be reachable during core hours."
4. **Two checkpoints, not one.** The trial is enough for them to judge my work and for me to test the workload. It's not enough to judge the company. **Second checkpoint at the 3-month mark**, when the salary first steps up: are real projects and shares coming in, and am I still learning?

---

## How to pass the two-week trial

**Code with AI, but understand everything.** The line that matters isn't "AI wrote it" vs "I wrote it." It's understood vs not understood. They *want* heavy Claude/Codex use and speed. Typing everything by hand would make me too slow.
- **I design first:** what the orchestrator does, what each agent checks, how it's measured. That part is mine, and it's what they'll test.
- **AI writes in small pieces.** I read, run and test each piece before the next.
- **I write it myself where I'm learning something new** (orchestrator logic, the first Solana checks). AI handles setup, API calls and formatting.
- **I can explain every line** if Ahmed or Mohamed asks.

**What makes a trial candidate stand out:**
- On day one, confirm exactly what "done" looks like.
- Ship something small and working in the **first few days**, not one big thing on day 14.
- Send a **short written update every day** during core hours: done, next, stuck. Writing matters to them.
- **Ask good questions early** instead of guessing for two days.

**Ideas for the Solana vulnerability agent:**
- An orchestrator that splits the work across specialist agents, one per bug type (missing signer/owner checks, non-canonical PDA bumps, stale data after a cross-program call, duplicate mutable accounts, unchecked arithmetic).
- Feed it their past findings as the checklist (the safe-solana-builder idea).
- Require a failing test or proof of concept before reporting, to cut false alarms.
- **Measure it on Solana Audit Arena programs, where the bugs are already known**: count the real bugs caught versus false alarms, and the token cost per run.

---

## Lessons from rehearsing answers
- **Finish the thought:** say what the fix *is*, in order, and what happens to the attacker or the loser.
- **Don't say "schema validation"** for identity or replay problems. It checks the *format* of data, not who someone is or whether something was already used.
- **The one technical idea:** *let the database enforce "only once," and record it before doing the work.* It covers double bookings, x402 replay and duplicate retries.
- **Identity comes from verification, never from the chat.** The check lives in code, not in the prompt, because a prompt can be tricked.
- **Limit damage:** limit what an attacker can do, notify the real owner, make it reversible.
- **Raise the flaws in your own projects yourself.** Auditors respect it, because it's what they do all day.
- Hospital agent holes to own: anyone can claim any patient ID (broken access control), and two callers can book the same slot (fix: a unique rule on doctor + date + time; the cinema analogy).
- CV corrections: Multi-Tenant RAG uses **one shared table filtered by organization**, not dedicated per-org stores. Say "designed for full isolation," not "100%." No repo has tests.
- Fixed the missing `BaseModel` import in the hospital repo: [PR #1](https://github.com/ahmedelkassrawy/AI-Powered-Hospital-Management/pull/1) (merged 2026-10-04).

---

## Links
- Company: https://sanadsquad.com/
- Frank: https://github.com/Frankcastleauditor · https://x.com/0xcastle_chain
- Al-Qa'qa': https://github.com/Al-Qa-qa · https://code4rena.com/@Al-Qa-qa
- x402: https://x402.org · Alchemy explainer: https://www.alchemy.com/overviews/agentic-payments-x402-explained
- x402 vs MPP: https://workos.com/blog/x402-vs-stripe-mpp-how-to-choose-payment-infrastructure-for-ai-agents-and-mcp-tools-in-2026
- Five Attacks on x402: https://arxiv.org/html/2605.11781v1
