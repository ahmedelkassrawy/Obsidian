Where a tool's response when a bad or imperfect input -> **gives the LLM everything it needs to recover on its very next step — automatically, silently, and without bothering the user.**

LLM calling a tool  problems:
- Every extra round trip is expesive and slow 
- Dead-end errors make the models panic or leak plumbing 

So a tool error is not a crash report — it is a steering prompt for the model's next turn.

---
### The Librarian Analogy

Imagine your AI assistant walks up to a librarian (your **tool**) to look up a page in Smash City’s brand binder.

- **AI:** _"Can I get the **Wing Hashtags** section?"_

Now look at two ways the librarian can answer:

**1. The Stubborn Librarian (Dead-end tool — what your code does today)**

> _"That doesn’t exist. Go ask me for the Table of Contents first."_

Now the AI is stuck. It either has to:

- Make an **extra trip** to ask for the Table of Contents, read it, then make a **third trip** to ask for Chapter 2 — **or**
- Give up and walk back to your social media manager saying: _"Hey, the system told me 'Wing Hashtags' doesn't exist..."_ (which is literally what happened — your SMM replied: **`"cant understand what u want"`**).

**2. The Helpful Librarian (Self-healing tool — the fix)**

> _"I file chapters by number, not by name. Here’s the Table of Contents right now:_
> 
> - `0` — Intro
> - `1` — Brand Voice
> - `2` — Wing Hashtags
> - `3` — Locations
> 
> _Just tell me which number you want."_

The AI immediately says _"Give me `2`!"_, grabs the hashtags, and writes the caption. **Your SMM never even knows a mistake happened.**

---

### Why This Exact Mismatch Happened in Bannerabia

When Bannerabia stores a brand’s guidelines in sections ([sections.ts · L16](/Users/shutterabiamedia/bannerabia-dev/src/guidelines/sections.ts:16)), it chops the document up and numbers every heading:

```
What's written in the doc     What Bannerabia actually uses as the ID
─────────────────────────     ───────────────────────────────────────
# Intro                   ──► "0"
# Brand Voice             ──► "1"
# Wing Hashtags           ──► "2"
# Locations               ──► "3"
```

Humans and AIs think in **names** (`"wing_hashtags"`). Your tool only accepts **numbers** (`"2"`).

And here is the crazy part in get_brand_guidelines.ts:44-57 [get_brand_guidelines.ts · L44](/Users/shutterabiamedia/bannerabia-dev/src/tools/get_brand_guidelines.ts:44):

1. On line 44, your server **already loaded Smash City’s entire guidelines from the database into memory.**
2. On line 56, it checks if `"wing_hashtags"` equals `"0"`, `"1"`, `"2"`, or `"3"`. It doesn’t.
3. On line 57, even though the Table of Contents is **already sitting right there in memory**, your tool throws it away and snaps back:
    
    > `"Unknown section. Read section=index first."`
    

---

### Why Every Wasted Trip Hurts in AI Engineering

In normal software, making one extra function call takes 1 millisecond and costs nothing.

In an AI app, **every extra tool call forces another full LLM turn** — meaning your server has to send the entire chat + rules (~89,000 tokens) to the AI model all over again, wait several more seconds, and pay again.

Compare the two flows side by side:

||Today (Dead-End Error)|Fixed (Self-Healing Tool)|
|---|---|---|
|**Trip 1**|AI asks for `"wing_hashtags"` → Tool says _"Unknown section. Read index first."_|AI asks for `"wing_hashtags"` → Tool says _"Use a number. Here’s the list: `0: Intro`, `1: Voice`, `2: Wing Hashtags`."_|
|**Trip 2**|AI has to ask for `"index"` just to see the list _(or panics & tells the user)_|AI immediately asks for `"2"` → **Gets the hashtags and writes the post!**|
|**Trip 3**|AI finally asks for `"2"` → Gets the hashtags|_(Not needed!)_|
|**User sees**|Either slower + more expensive, or a confusing error message|**Nothing went wrong — just a finished caption.**|

---
### Before: Dead-End Tool Design (What Actually Happened)

```
Step 1: Model calls get_brand_guidelines(brand="smash-city", section="wing_hashtags")
Tool  → ERROR: "Unknown section. Read section=index first."   ◄── Dead end! Gives 0 valid IDs.

Now one of two bad things happens:
  Path A (Wasteful):
    Step 2: Model calls get_brand_guidelines(section="index")  ◄── Extra round-trip + ~89K tokens
    Step 3: Model calls get_brand_guidelines(section="2")      ◄── Finally gets the section
  Path B (Broken UX — what happened with Smash City):
    Model stops and tells the SMM: "I asked for a section name the system doesn't have..."
    SMM replies: "cant understand what u want"
```

### After: Self-Healing Tool Design

```
Step 1: Model calls get_brand_guidelines(brand="smash-city", section="wing_hashtags")
Tool  → Does NOT match any ID, so it returns the valid index RIGHT INSIDE the response:
        {
          "error": "unknown_section",
          "requested": "wing_hashtags",
          "available_sections": "0: Preamble (~120 tokens)\n1: Voice (~350 tokens)\n2: Wing Hashtags (~210 tokens)",
          "hint": "Retry with one of the numeric section ids above (e.g. section=\"2\"), or omit section for full text."
        }

Step 2: Model immediately sees "2: Wing Hashtags", calls get_brand_guidelines(section="2")
        → Gets the exact rules → drafts the caption.
        The user NEVER even knows a mistake happened!
```

One tiny change turns a user-facing crash (or 3-step waste) into an invisible, reliable 2-step recovery.

---
### The 5 Patterns of self healing tool design 

## **Pattern** 1: Actionable Errors (Attach the Recovery Data)
Never return a bare "Invalid X" or "Not found" when you safely know the valid choices

Pack 3 things into every recoverable error:
1. **What failed** (`requested: "wing_hashtags"`)
2. **What IS valid** (`available_sections: ...`, valid platform names, valid date format, valid enum values)
3. **The exact next action** (`"Retry with section='2'"`)

_Other examples:_

- Model passes `platform: "ig"` instead of `"instagram"` → return `valid_platforms: ["facebook", "instagram", "bluesky"]`.

- Model passes `timezone: "Central"` → return `"Expected IANA timezone like 'America/Chicago' (this brand's timezone is 'America/Chicago')."`
## Pattern 2. Mistake-Proof the schema first

The best self-healing is **preventing the error before the tool is even called**:

- Look at z.string().optional() is a wide-open text box, so the model guesses slug names like `"wing_hashtags"`.
- Wherever valid values are fixed (platforms, post types, chart types), enforce them with **JSON Schema `enum`s** and explicit examples in `.describe(...)` (`"Numeric section id like '0', '1', '2' from the index — NOT a slug name"`).
- And if the data is small (like ≤12 KB brand guidelines), **inline it** so the tool call doesn't need to happen at all.

### Pattern 3: Safe Deterministic Normalization (Auto Fix harmless things)
When an input has zero ambiguity , just normalize it in code:
- Trimming whitespace (`" 2 "` → `"2"`)
- Coercing harmless type slips (JSON number `2` → `"2"`)
- Lowercasing known enums (`"Facebook"` → `"facebook"`)
- Stripping stray `#` prefixes if your database stores hashtags without `#`

Key Test:
Could two reasonable people disagree on what the model meant?
if no -> normalize
if yes -> do not guess and use Pattern 1 instead

### Pattern 4: State-Refresh on Stale Context
When an agent holds stale state (an old `revision`, an expired pagination cursor, or an outdated draft version)  -> a self-healing tool returns the **fresh state right away** (e.g., `current_revision` and/or page 0) instead of forcing an extra empty probe call.

### Pattern 5: Never Leak Plumbing
Pair self-healing tools with a **boundary rule** in the system prompt:

- Internal tool recoveries stay _inside_ the agent loop.
- If a tool still fails after retrying (e.g. Meta's API is genuinely down), translate it into calm, plain human language (_"Instagram isn't responding right now — want me to try again in a minute?"_) — never raw codes, schema field names, or `"Unknown section"` mechanics.

---
### 4. Subtle Senior Decision: 
**Takeaway:** Let deterministic code supply **facts and valid options**; 
let the LLM make **semantic choices**.

****### Security Can't Self Heal 
Watch out for Prompt Injection 

## **Quick** Checklist When Building Any AI Tool
Before shipping a new tool (MCP or in-app agent), ask these 6 questions:

1. **Can the schema prevent the mistake?** (Use `enum`s, clear formats, and concrete examples in parameter descriptions.)
2. **Is the mistake a harmless formatting quirk?** (If unambiguous, normalize it deterministically.)
3. **If validation fails, does the error include the valid options and next step?** (So the model recovers in 1 step instead of 2+ or giving up.)
4. **Does the error leak any cross-tenant or unauthorized data?** (If yes, strip it — fail closed.)
5. **Does the tool mutate real-world state?** (If yes, never silently guess — clarify or stage for human approval.)
6. **Is there a retry/step cap?** (So a confused model can't loop forever.)

----
4 step blueprint every self healing tool follows
Structure it in this exact order

1. SECURITY GATE   ──► Auth & tenant check FIRST. 
	Fail closed. 
	NEVER self-heal past this.
2. NORMALIZE       ──► Fix harmless, unambiguous format quirks (spaces, casing, empty string).
3. VALIDATE + CURE ──► If input still misses, return a structured JSON object with:
      (what failed) + (the valid options) + (how to retry).
4. HAPPY PATH      ──► Return the requested data cleanly.

Step 1: Fix the Schema First (Prevent Mistakes Before They Happen)

```typescript
// ❌ BEFORE — vague description; invites the model to guess "wing_hashtags"
section: z
  .string()
  .optional()
  .describe("Section id from index, or index/core. Omit for full rendered text, paged."),
```

Make the description **show concrete examples** and explicitly warn against the common mistake:

```typescript
// ✅ AFTER — tells the model the exact shape of valid IDs
section: z
  .string()
  .optional()
  .describe(
    'Numeric section id from the index (for example "0", "1", "2"), or "index" / "core". ' +
    'Do not guess heading slugs like "wing_hashtags". Omit to read the full guidelines.',
  ),
```

**Why this matters:** Zod `.describe(...)` strings become the JSON Schema sent to the LLM. One concrete example (`"0", "1", "2"`) prevents ~80% of bad calls before your handler even runs.

Step 2: Rewrite the Handler 
Step 3: Turn It Into a Reusable Helper for _All_ Your Tools
Step 4: How to Unit-Test a Self-Healing Tool (Zero LLM Calls Needed!)