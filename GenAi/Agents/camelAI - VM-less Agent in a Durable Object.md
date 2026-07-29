---
date: 2026-07-29
type: reference
project: learning
tags: [genai, agents, cloudflare, durable-objects, code-mode, sandbox, architecture, beginner]
description: A beginner-friendly walkthrough of how camelAI moved a coding agent off VMs into a Cloudflare Durable Object (with pi, R2, Artifacts, Code Mode) — every term explained simply, and compared to Archil serverless sandboxes.
---

# camelAI — VM-less Agent in a Durable Object (Beginner's Walkthrough)

---
## First, the 30-second picture (no jargon)

Imagine you build a product where an **AI coding agent** writes and runs code *for your users*. Every user chats with the AI, and the AI needs somewhere to actually *do* things — save files, run commands, build an app.

The obvious way: give each user their **own computer in the cloud** that's always switched on. That works, but it's like **renting a whole apartment for every customer and leaving the lights on 24/7** even when they're asleep. Wildly expensive once you have lots of customers.

camelAI's story is: *"We stopped renting apartments. We figured out how to give each user just a locker and a workbench they can use for a few seconds at a time — and it turned out the AI barely noticed the difference."*

That's the whole post. The rest is **how**.

---

## The cast of characters (learn these 6 words and the rest is easy)

Before the story, here are the building blocks. Don't memorize — just get the *vibe*, and refer back.

| Term | Dead-simple meaning | Analogy |
|---|---|---|
| **VM (Virtual Machine)** | A whole computer, rented in the cloud, running Linux. Boots up, has a hard disk, stays on. | Renting a full apartment. |
| **Container** | A lighter-weight "mini computer" — faster to start than a VM, but still a real Linux environment. | A hotel room instead of an apartment. |
| **bash** | The command-line language Linux uses (`ls`, `cd`, `mkdir`, `rm`...). It's *how* you talk to a Linux computer. | The native language spoken inside the apartment. |
| **Cloudflare** | A company that runs computers all over the world, very close to users. You rent tiny slices of them. | A global chain of shared workspaces. |
| **Worker** | Cloudflare's tiny, super-fast unit of compute. Runs a bit of code, then vanishes. Very cheap. No Linux, no bash. | A hot-desk you use for 2 minutes and leave. |
| **Agent** | The AI itself — the thing that thinks, decides "I'll write this file / run this command," and loops until the task is done. | The worker (person) doing the job. |

Keep this table in the back of your mind. The whole article is about **swapping the expensive "apartment" (VM) for cheap "hot-desks" (Workers), without the AI getting confused.**

---

## Why they wanted to change (the problem)

The old setup gave **every user a full VM (apartment) with an attached disk (hard drive), always on.** Three problems:

1. **💸 Cost.** You pay for the machine *and* the fast disk, all day, even while the user is offline.
2. **📈 Scaling.** More users = renting more real machines with real disks. This gets very expensive very fast.
3. **🔓 Security.** Here's the subtle one. To *do* anything useful (call an API, fetch data), the AI needs **credentials** — passwords / API keys / tokens. In the old setup those secrets had to sit *inside* the user's machine where the AI could touch them. That's risky: if the AI (or its code) misbehaves, the secrets are right there.

> **Why is this so hard to fix?** Because coding AIs are **trained to use bash.** They've read millions of examples where the solution is "run this Linux command." And bash only exists on a real Linux machine (a VM). So "AI needs bash" → "bash needs Linux" → "Linux needs a VM" → "we're stuck renting apartments." camelAI's whole trick is **breaking that chain.**

---

## The journey: 3 rebuilds, each fixing one thing

They didn't get here in one jump. It took **three redesigns**, and it's clearest if you see what each one fixed and what it *didn't*.

---

### 🟦 Step 1 — Move the *thinking* out of the VM (but keep the VM for *doing*)

**The idea:** separate the AI's **brain** from its **hands**.
- **Brain** = the part that thinks and decides ("I should create a file called `app.js`").
- **Hands** = the part that actually runs the command on a real machine.

> Anthropic uses this exact phrase — *"brain separated from the hands"* — for its own managed agents. It's a common, powerful pattern.

**How they did it:**
- They needed their own **harness**. (A **harness** = the wrapper program that runs the AI in a loop: send the AI a message → it replies with an action → run the action → send it the result → repeat. The [[Core Architecture|Claude Code harness]] is one example, but it was glued to a VM and they couldn't separate them.)
- So they built a new harness on top of **pi** — an open-source coding-agent toolkit by Mario Zechner. The neat thing about pi: it's built in **layers.** The *top* layer assumes "I'm running on a normal computer with bash." But the *lower* layers just give you the raw agent machinery — the loop, the memory of the conversation — **without caring what machine it runs on.** camelAI grabbed only the lower layers.
- They ran those lower layers inside a **Durable Object.**

> **🧱 New term — Durable Object (DO).** This is the single most important word in the article. A Durable Object is a **tiny cloud computer that (a) remembers things between visits and (b) lives on Cloudflare's edge, physically close to the user.**
> - *"Durable"* = it has memory that survives. A normal Worker forgets everything the moment it finishes. A Durable Object **keeps its state** — like a hot-desk that somehow remembers your stuff is still in the drawer next time you sit down.
> - *"Edge"* = Cloudflare has machines in hundreds of cities. Your DO runs in the one **nearest the user**, so responses feel snappy.
> - **Each chat thread gets its own Durable Object.** One conversation = one little brain with its own memory.

At this stage the **VM still existed**, but the AI no longer *lived* inside it. The brain (in the DO) would just **phone the VM** whenever it needed hands to run a command.

**What this bought them (nice side-effects of splitting brain and hands):**
- The AI can **start replying instantly**, before the VM has even finished booting up. (The brain doesn't wait for the hands to wake.)
- If a message doesn't need any commands run, the **VM can stay asleep entirely.**
- **One brain can control several hands at once** — a single AI could juggle multiple machines.

They named each "hands" unit a **project** — a VM plus a git repository (version history) created on the fly.

> **🧱 New term — git repository / version history.** Git is the system programmers use to save snapshots of their code over time (so you can undo, see history, etc.). A **repository** ("repo") is one project's worth of that history.

> **🧱 New term — Cloudflare Artifacts.** Normally, to have git history you'd run a **git server** (a machine that stores everyone's code history — extra infrastructure to babysit). Artifacts is Cloudflare's ready-made, git-compatible storage you can create instantly from code, so you get git history **without running your own git server.**

⚠️ **What Step 1 did NOT fix:** *cost.* There was still **one VM per user.** They'd made things faster, but they were still renting an apartment for everybody. On to Step 2.

---

### 🟩 Step 2 — Get rid of the VM entirely (turn the "hard drive" into a database)

Now the bold move: **delete the VM behind each project.** But a coding agent needs a **filesystem** — a place to save files. If there's no computer, where do the files live?

**Their answer: fake the filesystem using a database + cloud storage.** The AI still *thinks* it's reading and writing normal files. Underneath, it's something else entirely.

Here's the clever part — remember a **Durable Object has its own built-in memory.** That memory is actually a **SQLite database.**

> **🧱 New term — SQLite.** A database is just an organized way to store data in tables (rows and columns). **SQLite** is a tiny, self-contained database — the same one inside your phone apps and browser. Here, Cloudflare gives each Durable Object its own SQLite database, up to **10 GB**.

But databases are bad at holding **big files** (a database row can only hold so much). So they added a second storage place for the large stuff:

> **🧱 New term — R2.** R2 is Cloudflare's **object storage** — think "a giant cheap folder in the cloud for big files" (like Dropbox or Amazon S3). Good for large things, not for tiny frequent reads.

**The filesystem trick, spelled out:**
- **Small file** (say, a 3 KB `app.js`)? → stored **directly as a row in the SQLite database.**
- **Big file** (over ~**1.5 MB**)? → the actual bytes go to **R2**, and the database row just stores a **pointer** (a note saying *"the real file is over there in R2"*).

> **🧱 Term — pointer.** Just an address/reference. Instead of keeping the whole heavy file in the database, you keep a little sticky-note that says where to find it. Like a library catalog card that tells you which shelf the book is on, instead of stuffing the book into the card drawer.

To the AI, all of this looks like **one normal filesystem.** It writes `save file` and reads `open file` like always — it has no idea it's really talking to a database and a cloud bucket.

They built this by **reusing Cloudflare's "Shell"** — an experimental project from Cloudflare's team that already implements "a filesystem + a way to run things" for Workers. camelAI didn't reinvent it; they borrowed heavily.

**The big mental shift of Step 2:**
> Before: persistence = **a machine you keep switched on** (infrastructure to maintain).
> After: persistence = **data sitting in a database and a bucket** (nothing to keep alive).
> Files don't need a running computer to exist — they just *sit there* as stored data until someone asks for them. **That's what makes it cheap.**

Version history still runs through **Artifacts** (from Step 1), so projects keep their git history with no git server.

⚠️ **What Step 2 did NOT fix yet:** the AI could still run **bash**, which meant they still needed *some* Linux around, plus that lingering **security problem** (credentials inside the sandbox). Step 3 tackles that.

---

### 🟥 Step 3 — Remove bash (the scary one)

This is the boldest change, and the author admits it *"felt drastic."* Coding AIs **love** bash — it's their default tool for everything. Taking it away is like taking a chef's knives.

**Why remove it anyway?** Two reasons:
1. **Security.** An AI with bash + internet needs live credentials to be useful — and those secrets end up inside the sandbox where the code runs. Their attempts to work around this (routing traffic through special proxy URLs) were getting *"hacky and hard to enforce."*
2. **Cost.** bash needs Linux; Linux needs a machine; machines cost money.

**What they replaced bash with:** instead of writing Linux commands, **the AI now writes small JavaScript programs**, which run in a **super-lightweight sandbox**.

> **🧱 New term — sandbox.** A **sandbox** is a safe, walled-off space to run code so it can't damage anything outside it. Like a child's sandbox: they can build and knock down castles, but the mess stays inside the box.

> **🧱 New term — V8 isolate.** V8 is the engine (from Google Chrome) that runs JavaScript. An **isolate** is one tiny, sealed instance of it. The magic numbers:
> - Boots in **milliseconds** (a VM takes *seconds* to *minutes*).
> - Uses just **a few megabytes** of memory.
> - Every time the AI runs some code, it gets a **brand-new, clean isolate** — used once, thrown away.

> **🧱 New term — Code Mode + dynamic Workers.** "Code Mode" is the approach of letting the AI **write code as its way of taking actions** (instead of picking from a menu of buttons). Cloudflare's **dynamic Worker loaders** are the machinery that spins up a fresh Worker/isolate on demand to run that code. Put together: *the AI writes JavaScript → Cloudflare instantly runs it in a throwaway isolate → returns the result.*

**Now here's the elegant security fix:** the sandbox comes **pre-loaded with methods** — ready-made functions the AI can call, like `getData()` or `deployProject()`. The AI calls the method; **the actual login/authentication happens on camelAI's side, outside the sandbox.** So:

> 🔑 **The credentials never enter the sandbox.** The AI says *"please fetch the data"* by calling a method; camelAI's own trusted code attaches the secret key and does the real request. The AI never sees the key. Problem solved.

> **🧱 New term — method.** In programming, a **method** is just a named, reusable function that does one specific job — e.g. `deployProject()`. Instead of "here's a whole Linux, figure it out," the AI gets "here's a labeled button for each thing you're allowed to do."

**"But wait — bash did a LOT of things. Didn't you lose all of that?"** Less than you'd think:

- **Most bash use is just file operations** (create, read, edit, search files). The AI got **native tools** for those: `read`, `write`, `edit`, plus custom `grep` (search inside files) and `glob` (find files by name pattern). That covers the **80/20** — the vast majority of real usage.
- **The rest** — specific commands for specific jobs — became **explicit methods**, one per job:
  - Deploying an app (`wrangler deploy` in Linux terms) → a controlled **`deploy_project`** method. Bonus: because camelAI now *knows the exact moment* a deploy happens, it can automatically pop open a **live preview** for the user. (Before, with bash, they had to *snoop on network traffic* to even guess when someone deployed. Much uglier.)
  - **Building the user's app** and **running Python notebooks** → their own methods.

> **🧱 New term — deploy.** "Deploying" = publishing your app so it's live on the internet at a real URL.
> **🧱 New term — notebook.** A Python **notebook** (Jupyter) is an interactive document where you run code in chunks and see results inline — popular for data work.

**The one place they kept real Linux — and why:**
App builds and notebooks *genuinely* need a real Linux environment (e.g. running `bun install` to download an app's dependencies; the tiny Workers have only **128 MB of memory and a fraction of a CPU**, too small for a real build). So for *just those jobs*, camelAI:
1. Spins up a **short-lived container** (a mini Linux, via Cloudflare's **Sandbox SDK**),
2. Copies the project in, runs the build,
3. Returns the result, and **shuts the container down immediately.**

> They use full Linux **only for the few seconds of work that truly need it** — not 24/7 per user. That's the key difference from the old "apartment always on" model.

**The honest trade-offs of removing bash:**
- ❌ **You have to predict what the AI will need.** With bash, the AI could improvise *any* command. Now, if a capability is missing, **the humans have to build it as a new method** first.
- ✅ But that pressure turned out to be *good*: it forces the team to notice what users actually do and build a **proper, first-class feature** for it, instead of the AI hacking around.
- ✅ **Surprise win: cheaper/smaller AI models perform BETTER.** Why? bash is *open-ended* — infinite possibilities — and weaker models get lost with too much freedom. Give them a **short menu of clear methods** and they shine. Since keeping costs low is the whole point, this was a happy accident. (This echoes [[Context Engineering]] and [[Agents Best Practice]]: narrowing an agent's choices often *improves* it.)

---

## The finished stack (all the pieces together)

| What it does | The piece they use | In plain English |
|---|---|---|
| The AI's brain + loop | **Durable Object** running **pi** | A tiny, memory-keeping cloud brain near the user |
| Storing files | **SQLite** (small) + **R2** (big) | A database pretends to be a hard drive |
| Version history | **Cloudflare Artifacts** | Git history with no git server to run |
| Running the AI's actions | **Code Mode** + **dynamic Workers** | AI writes JS → runs in a throwaway isolate |
| Builds & notebooks | Short-lived **containers** (Sandbox SDK) | Real Linux, but only for a few seconds |
| Publishing apps | a **`deploy_project`** method | One controlled button instead of raw commands |

**💰 The payoff (why they did all this):**
- **Billing is per-execution, not per-second-of-uptime.** You pay only when code actually *runs*, not for idle time. The author says **thousands of executions cost about the same as a few minutes** of the old container services.
- **Low latency** — everything runs on the edge, near the user.
- **Scaling is now Cloudflare's problem, not theirs.**
- **From the user's point of view, nothing changed** — they still build and deploy full apps to live URLs.

---

## Comparison: camelAI vs. Archil Serverless Sandboxes

You asked me to check how this stacks up against **[Archil](https://docs.archil.com/compute/serverless-sandboxes)**. Both are solving the *same* headline problem — *"give an AI agent a place to run code + save files, without paying for always-on VMs"* — but they choose **opposite strategies.**

**The simplest way to hold the difference in your head:**
- **camelAI = "take bash AWAY."** Give the AI a short list of safe, custom buttons (methods). Cheapest and safest, but you must build each button.
- **Archil = "keep bash, make it serverless."** Give the AI a *real* Linux command line, but only spin it up when needed, and put it right next to the data. Most flexible, least "surprising" for a bash-trained AI.

> **🧱 New term — microVM.** A **microVM** is a stripped-down, very fast-booting virtual machine — lighter than a full VM but still a *real* isolated Linux, unlike a JavaScript isolate. Archil is built on these.

| Question | **camelAI** | **Archil** |
|---|---|---|
| What actually runs the code? | JavaScript in **V8 isolates**; real Linux only for builds/notebooks | **microVMs** running real bash / Python / Node |
| bash — kept or removed? | **Removed** (replaced by typed methods) | **Kept** (you get a real Unix shell) |
| Where do files live? | **SQLite** (small) + **R2** (big) + Artifacts for git | An **Archil disk** you mount at `/mnt/archil` (a real folder path) |
| Trick for speed | Runs on the **edge, near the user** | microVM sits **right next to your data** ("data cohabitation") — cuts latency + data-transfer fees |
| Handling secrets | **Never enter the sandbox** — auth done outside | Standard sandbox; you manage credentials yourself |
| How much runs at once | One brain → many executions | **Hundreds** of parallel commands (thousands by contract) |
| How you pay | **Per execution** | **Per invocation, 100ms minimum**; free tier: 1,000 sandbox-minutes/month per TB of stored data |
| Known limits | Workers cap at 128 MB RAM (why builds use containers) | Commands **time out after 5 min**; output capped at **128 KiB** (write bigger output to disk) |
| The catch | You must **pre-build every capability** as a method | You keep full Unix power, but manage disks + "check-out/check-in" rules before editing shared data |

**How to read the two philosophies:**
- **Archil** bets that *"agents want a real filesystem and real Unix, so just make that cheap and elastic and glue it to the data."* Least friction for an AI trained on bash. The innovation is **microVMs that appear on demand right beside your stored data.**
- **camelAI** bets that *"bash is the liability — remove it, and there's no machine to keep alive at all."* The innovation is **there's literally no VM**, plus secrets never touch the AI's code.
- **Where they secretly agree:** both bill **per-use, not per-uptime**, and both obsess over **keeping compute close to data** to cut latency and transfer costs. And notice — camelAI *still* reaches for real Linux containers exactly where Archil lives full-time (builds, dependency installs, notebooks). Neither escapes Linux entirely; they just disagree on *how often* you need it.

**A rule of thumb for choosing:**
- Your AI mostly **edits files + does a known, fixed set of actions** → camelAI's "no bash, explicit methods" style is cheaper, safer, and easier for small models.
- Your AI needs **open-ended, unpredictable Linux work on big datasets** → Archil's "serverless microVM next to your disk" saves you from building a hundred methods up front.

---

## The 5 ideas actually worth remembering

If you forget everything else, keep these:

1. **Separate the brain from the hands.** The thinking part and the doing part don't have to live on the same machine. Splitting them makes the AI faster and more flexible. (See also [[AWS Bedrock Agent Core]].)
2. **A "filesystem" can secretly be a database.** Small files in a database, big files in cloud storage, hidden behind a normal-looking file interface. Turns "a machine you must keep running" into "data that just sits there." Cheap.
3. **Constraining the AI can make it *better*, not worse.** Removing open-ended bash actually helped cheaper models — a short menu beats infinite freedom. (Ties to [[Context Engineering]].)
4. **Keep secrets OUT of the sandbox.** Don't hand the AI the keys. Give it labeled *methods* to call, and do the real authentication on your own trusted side. (Relates to how tools work in [[Function Calling]] and [[MCP Arch]].)
5. **Use heavy infrastructure only for the seconds that need it.** Real Linux for the 10-second build, throwaway isolates for everything else. Don't leave the apartment lights on all night.

---

## 📚 Glossary (quick reference)

- **Agent** — the AI that thinks, decides on actions, and loops until a task is done.
- **Harness** — the wrapper program that runs the agent loop (message → action → result → repeat).
- **VM (Virtual Machine)** — a full rented cloud computer running Linux. Slow to boot, stays on, costs money.
- **Container** — a lighter "mini computer," faster than a VM but still real Linux.
- **microVM** — an even lighter, fast-booting real VM (what Archil uses).
- **bash** — the Linux command-line language (`ls`, `cd`, `rm`…); needs a real Linux machine.
- **Cloudflare** — company running lots of small computers worldwide, close to users.
- **Edge** — those many local locations; running "on the edge" = running near the user for speed.
- **Worker** — Cloudflare's tiny, cheap, fast unit of compute. No Linux, forgets everything when done.
- **Durable Object (DO)** — a Worker that *remembers* its state between calls; each chat gets its own. The agent's home.
- **SQLite** — a small self-contained database; each DO has one (up to 10 GB) used here as the filesystem.
- **R2** — Cloudflare's cheap cloud storage for big files (like S3 / Dropbox).
- **Pointer** — a small reference/address saying where the real (big) file lives.
- **Artifacts** — Cloudflare's ready-made git storage: version history with no git server to run.
- **git / repo** — the system (and per-project store) for saving code history and snapshots.
- **sandbox** — a walled-off, safe space to run code so it can't harm anything outside.
- **V8 isolate** — one tiny sealed JavaScript engine instance; boots in ms, uses a few MB, used once and discarded.
- **Code Mode** — letting the AI take actions by *writing code*, rather than picking from a fixed menu.
- **dynamic Workers** — Cloudflare machinery that spins up a fresh Worker/isolate on demand to run that code.
- **method** — a named, reusable function for one specific job (e.g. `deploy_project()`).
- **credentials** — secrets (passwords, API keys, tokens) needed to access things. Kept *outside* the sandbox here.
- **deploy** — publish an app so it's live on the internet at a URL.
- **notebook** — an interactive Python document (Jupyter) where you run code in chunks.
- **Sandbox SDK** — Cloudflare's toolkit for spinning up short-lived containers on demand.
- **pi** — the open-source, layered coding-agent toolkit camelAI built its harness on.

## Related notes
- [[Deep Agents]] · [[Agent Patterns]] · [[AI Workflows VS AI Agent]]
- [[Function Calling]] (methods ≈ tools) · [[MCP Arch]] (another "expose safe capabilities" model)
- [[Core Architecture]] (the Claude Code harness camelAI started on) · [[AWS Bedrock Agent Core]] (another brain/hands split)
- [[Context Engineering]] · [[Agents Best Practice]] (why fewer choices can beat more freedom)
