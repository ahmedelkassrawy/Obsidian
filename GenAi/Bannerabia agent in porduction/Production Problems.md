AI Engineering is actually just regular software engineering wrapped around an LLM 

1. User Input (messgae + optional PDF/Photo + wchi app page they are on)
2. Server guardrails (Determinstic Code )
	- Auth and Brand isolation (which brands/workspace can this user touch)
		- Approval check (did the user say "approve" to pending preview?)
3. Context Assembly (Building API Request)
[ Tool Schemas ] + [ System Prompt ] + [ Dynamic Tail ] + [ Chat History ] + [ New Message ]
4. Agent Loop (LLM <-> Tools)
	LLM reads the full request ──► decides to call a tool (e.g. stage_draft)
	 Server runs tool safely ──► returns tool result text back into context 
	 LLM reads result ──► writes reply (or calls another tool)
5. Post-Processing and UI  (Determinstic)
	- Render interactive Cards and safe suggestion chips
	- Persist history & usage metrics
	- Wait for human approval before anything publishes

What was wrong 
- Wasted money 
- Unnecessary back-to-forth turns 
- conflicting instrcuctions
- missing memory

1. Prompt Caching and Prefix Layout
Money and cost leak , since the providers offer prompt caching where if the beginning (prefix) of your request is **byte for byte** identical for a recent request up to a cache breakpoint we pay 0.1% to read instead of 1.25x to write it fresh 

- The golden rule of prompt caching is: 
**static content first, dynamic content last.** 
- If _even one character_ changes early in the prompt, everything after it misses the cache

So what we have to do is we put the static content first and dynamic content at last
and also check the Run Anthropic's `count_tokens` API to measure how much of that 71K prefix is **tool schemas** (estimated ~45–50K tokens!) vs. **system prompt text** (~21K tokens), before trimming anything blindly.

---
2. Context Engineering: Inlining vs Retrieval & Prompt conflicts
**Context engineering** is deciding _what_ information to put straight into the prompt (**inlining**) vs. letting the model fetch on demand via a tool (**just-in-time retrieval / RAG**).

- **Inline** when data is small and needed on almost every turn (0 extra round-trips, 0 tool errors, stays cached).
- **Retrieve via tools** only when data is huge or rarely needed.

Equally important: 
**LLMs struggle with contradictory instructions.** 
As codebases grow, teams keep adding rules in different files ("prompt rot"). 
-> When three sections disagree, the model wastes turns hedging or picks the wrong path.

What we have to do:
- Delete the contradictory instruction
- Self healing tool design 

---
### 3. Tool Outputs are prompts too (Multi Surface Leakage)
Beginners think only the system prompt steers an AI. In reality, **every string returned by a tool goes straight into the LLM's context and acts as a prompt** — often with _stronger_ weight than the system prompt because it's right at the end of the context window (recency bias).

### 4. Don't Blame the Model When the Data/Guidelines Are Rigid
When an AI gives repetitive, robotic answers, beginners immediately try to "prompt engineer" harder (_"BE CREATIVE! DO NOT REPEAT YOURSELF!"_).

Senior AI engineers **inspect the inputs first**. If a brand guideline says _"Always include X"_ and your system prompt says _"Vary your captions"_, you've created an impossible tug-of-war.

**Step 1 (Guideline hygiene):** Rewrite rigid `"always"` rules into **rotation pools** (e.g., _"pick 1 closer from this list; don't repeat the last 3"_), approved per brand by the SMM.

**Step 2 (Recent-captions digest):** Only _after_ removing the rigid templates, pass a short digest of recent captions — placed in the **dynamic tail** (not the cached prefix, so it doesn't bust the cache!).

### 5. Deterministic Code vs. Probabilistic LLMs (Knowing When _Not_ to Use AI)

This is the single biggest difference between a hobbyist demo and production AI engineering: 
**Use LLMs for ambiguity and generation; use deterministic code and direct UI for safety, state, diffs, and surgical edits.**

## **A**. Safety Gates and Intent Parsing 
We should never let an LLM decide on its own whether it should publish a social media post or just call admin tools

Approval should happen via a deterministic code 
Example: The SMM wrote "the captions looks good change this"
But because the message contained an approval phrase ("looks good") mixed with an edit , the approval inspector fired in 0 seconds 

what should happen is the apprvoal-vs-edit boundary and intent understanding so that any mixed approval + edit signals are then routed to editing not approved

**B. Direct UI Manipulation Beats Chat** 
In one of the brands the SMM wanted to remove a line from the proposed AI caption and that triggered a full LLM turn 9 times and and what happend was that the LLM changed things "silentely" without saying or showing what is removed or what is done

Fix was:
1. an inlne edit / strike a line directly on the Chat Postcard
2. instead of asking the llm to explain what is changed it then make a diff bet old and new (0 tokens and 100% accurate)
3. The proposed quick reply suggestion are **Never generated freely by the LLM".** They should come for a strict server allow list based on the conversation state
---
### 6. Agent Memory Arch (Working vs Brand vs Workspace memory)

Because LLMs forget everything when a chat ends, production agents organize memory into **scopes**:

1. **Working memory:** The current conversation (bounded by token windowing + rolling summaries — already on via `AGENT_TOKEN_WINDOW_ENABLED`).
2. **Entity/Brand memory:** Rules specific to one client (Brand Guidelines).
3. **Workspace/Agency memory:** House rules that apply across _every_ client.

**Critical safety rule for agent memory:** **Never auto-save memories silently.** If an AI silently writes rules into its own system prompt based on one-off remarks, a single misunderstood sentence permanently corrupts future outputs (_memory poisoning_).

**What went wrong in Bannerabia:** There was no workspace-level memory layer, and the assistant never offered to remember recurring feedback. As a result, the SMM had to type `"don't name the dishes/plates"` **10 separate times across 8 brands on 7 different days**.

Fixes: 
- Add a **Workspace House Style** table alongside per-brand guidelines.
- Offer a `"Save as rule?"` chip/flow when the user gives a standing correction — routed through the existing **preview → human approval → server save** gate.

---
### 7. Multimodel State and Visual Memory (Photo Blindness)
Sending raw images to an LLM on every single turn of a long chat is expensive and hits payload limits. Yet if you strip images from older turns without replacing them, the model goes **blind** during follow-up revisions.

What was wrong in the prodcution was :
We already resize and send phot cleanly on the 1st run , but on the turn 2+ , chat history replays the attachment only as `managed:<id> (photo "1.png") … already handled`

So when the SMM replied "focus on the wings only" or "read the photo correctly its about Kenner" , the model couldnt see the photo anymore and either guessed or burned extra turns calling `get_image_preview`

Fix:
Visual persistence on the first sight: When the model views an uploaded photo/video on turn 1, save a rich text description into `managed_media_alt_text` and replay that lightweight text on follow up turns. Cheap, fast and keeps revisions visually