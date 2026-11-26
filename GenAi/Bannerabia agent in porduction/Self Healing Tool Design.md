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

Pattern 1: Actionable Errors (Attach the Recovery Data)
Never return a bare "Invalid X" or "Not found" when you safely know the valid choices