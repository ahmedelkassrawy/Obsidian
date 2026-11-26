---
tags: [genai, ai-engineering, bannerabia, tools, error-handling]
---

## The big idea

A **self-healing tool** is a tool that, when the AI sends it a wrong or slightly-off request, answers with everything the AI needs to fix it on the very next try. The fix happens automatically and quietly, and the user never gets bothered.

> [!definition] Tool
> An action the AI is allowed to ask for, like "get this brand's guidelines" or "save this draft". The AI only asks. Your code actually does it and sends back an answer.

Why this matters when an AI uses tools:

- **Every extra back-and-forth is slow and costs money.**
- **Errors that lead nowhere confuse the AI.** It either gets stuck, or it tells the user about the internal error, which makes no sense to them.

So when a tool says "that didn't work", that message shouldn't be a crash report. It should tell the AI what to do next.

---

## The librarian example

Imagine the AI walks up to a librarian (the tool) to look something up in Smash City's brand binder.

**AI:** *"Can I get the **Wing Hashtags** section?"*

The librarian can answer in two ways.

### 1. The stubborn librarian (what the tool did before)

> *"That doesn't exist. Go ask me for the Table of Contents first."*

Now the AI is stuck. It has two options, and both are bad:

- Make an **extra trip** to get the Table of Contents, read it, then make a **third trip** to ask for chapter 2.
- Give up and go back to the social media manager (SMM) saying: *"Hey, the system told me 'Wing Hashtags' doesn't exist..."*

The second one is exactly what happened. The SMM replied: **"cant understand what u want"**.

### 2. The helpful librarian (the fix)

> *"I file chapters by number, not by name. Here's the Table of Contents:*
>
> - `0`: Intro
> - `1`: Brand Voice
> - `2`: Wing Hashtags
> - `3`: Locations
>
> *Just tell me which number you want."*

The AI says *"Give me `2`!"*, gets the hashtags, and writes the caption. **The SMM never even knows a mistake happened.**

---

## Why this mix-up happened in Bannerabia

Bannerabia stores each brand's guidelines in sections (see `src/guidelines/sections.ts`, line 16). It splits the document at every heading and gives each part a number:

```text
What's written in the doc     What Bannerabia uses as the ID
─────────────────────────     ──────────────────────────────
# Intro                   ──► "0"
# Brand Voice             ──► "1"
# Wing Hashtags           ──► "2"
# Locations               ──► "3"
```

People and AIs think in **names** (`"wing_hashtags"`). The tool only accepted **numbers** (`"2"`).

The frustrating part is in `src/tools/get_brand_guidelines.ts`, lines 44–57:

1. On line 44, the server **already loaded all of Smash City's guidelines from the database.**
2. On line 56, it checks whether `"wing_hashtags"` matches `"0"`, `"1"`, `"2"` or `"3"`. It doesn't.
3. On line 57, even though the Table of Contents is **already loaded and ready**, the tool ignores it and replies:

> `"Unknown section. Read section=index first."`

---

## Why every wasted trip hurts

In normal software, one extra function call takes about a millisecond and costs nothing.

In an AI app, **every extra tool call means another full round with the AI.** The server has to send the whole chat plus all the rules again (around 89,000 tokens), wait several more seconds, and pay again.

> [!definition] Token
> The unit AI providers count and charge by. Roughly a piece of a word. 89,000 tokens is roughly the length of a short novel, sent again on every trip.

Here are the two versions side by side:

| | Before (dead-end error) | After (self-healing tool) |
| --- | --- | --- |
| **Trip 1** | AI asks for `"wing_hashtags"`. Tool says *"Unknown section. Read index first."* | AI asks for `"wing_hashtags"`. Tool says *"Use a number. Here's the list: `0: Intro`, `1: Voice`, `2: Wing Hashtags`."* |
| **Trip 2** | AI has to ask for `"index"` just to see the list (or gives up and tells the user) | AI asks for `"2"` and **gets the hashtags and writes the post** |
| **Trip 3** | AI finally asks for `"2"` and gets the hashtags | Not needed |
| **What the user sees** | A slower, more expensive reply, or a confusing error | **Just a finished caption** |

### Before: the dead-end tool (what actually happened)

```text
Step 1: AI calls get_brand_guidelines(brand="smash-city", section="wing_hashtags")
Tool  → ERROR: "Unknown section. Read section=index first."   ◄── Dead end. Gives no valid IDs.

Then one of two bad things happens:
  Path A (wasteful):
    Step 2: AI calls get_brand_guidelines(section="index")  ◄── Extra trip + ~89K tokens
    Step 3: AI calls get_brand_guidelines(section="2")      ◄── Finally gets the section
  Path B (confusing for the user, what happened with Smash City):
    AI stops and tells the SMM: "I asked for a section name the system doesn't have..."
    SMM replies: "cant understand what u want"
```

### After: the self-healing tool

```text
Step 1: AI calls get_brand_guidelines(brand="smash-city", section="wing_hashtags")
Tool  → No match, so it sends the list of valid sections inside the reply:
        {
          "error": "unknown_section",
          "requested": "wing_hashtags",
          "available_sections": "0: Preamble (~120 tokens)\n1: Voice (~350 tokens)\n2: Wing Hashtags (~210 tokens)",
          "hint": "Retry with one of the numeric section ids above (e.g. section=\"2\"), or omit section for full text."
        }

Step 2: AI sees "2: Wing Hashtags" and calls get_brand_guidelines(section="2")
        → Gets the exact rules → writes the caption.
        The user never knows a mistake happened.
```

One small change turns a confusing error (or three wasted steps) into a quiet, reliable two-step recovery.

---

## The 5 patterns of self-healing tools

### Pattern 1: Helpful errors (include how to fix it)

Never reply with just "Invalid X" or "Not found" when you already know what the valid choices are.

Every error the AI can recover from should include three things:

1. **What went wrong** (`requested: "wing_hashtags"`)
2. **What's allowed** (`available_sections: ...`, valid platform names, the right date format, the allowed values)
3. **Exactly what to do next** (`"Retry with section='2'"`)

More examples:

- The AI sends `platform: "ig"` instead of `"instagram"`. Reply with `valid_platforms: ["facebook", "instagram", "bluesky"]`.
- The AI sends `timezone: "Central"`. Reply with *"Expected a timezone like 'America/Chicago' (this brand's timezone is 'America/Chicago')."*

### Pattern 2: Stop the mistake before it happens

The best fix is making the mistake hard to make in the first place.

> [!definition] Schema
> The description of what a tool accepts: which inputs, what type each one is, and what they mean. The AI reads it to decide what to send.

- A plain `z.string().optional()` input is like an empty text box with no hints, so the AI guesses names like `"wing_hashtags"`.
- When there's a fixed list of valid values (platforms, post types, chart types), lock the input to that list (a JSON Schema `enum`), and give clear examples in `.describe(...)`. For example: *"Numeric section id like '0', '1', '2' from the index, NOT a name."*
- If the data is small (brand guidelines of 12 KB or less, for example), **put it straight into the prompt** so the tool doesn't need to be called at all.

> [!definition] Enum
> A fixed list of allowed values. If the input isn't on the list, it's rejected, so the AI can't make up new ones.

### Pattern 3: Quietly fix harmless slips in code

When there's zero doubt about what the AI meant, just fix it in code:

- Trim extra spaces (`" 2 "` → `"2"`)
- Fix harmless type mix-ups (the number `2` → the text `"2"`)
- Lowercase known values (`"Facebook"` → `"facebook"`)
- Remove a stray `#` if the database stores hashtags without it

> [!tip] The test
> Could two reasonable people disagree about what the AI meant?
> - **No** → fix it automatically.
> - **Yes** → don't guess. Use Pattern 1 and send back the valid options.

### Pattern 4: Send fresh data when the AI is out of date

Sometimes the AI is working from old information: an old version number of a draft, a page link that expired, an outdated draft. A self-healing tool sends back the **current information right away** (for example, the latest version number or the first page), so the AI doesn't need an extra call just to find out what's current.

### Pattern 5: Never show the user the internal details

Combine self-healing tools with a clear rule in the system prompt:

- Fixing tool mistakes stays **inside** the AI's own back-and-forth. The user doesn't see it.
- If a tool still fails after retrying (for example, Meta's servers are actually down), explain it in calm, plain language: *"Instagram isn't responding right now. Want me to try again in a minute?"* Never show raw error codes, field names, or messages like `"Unknown section"`.

---

## Who decides what

> [!abstract] The rule
> Let plain code supply the **facts and the valid options**. Let the AI make the **choices that need understanding**, like which section fits what the user asked for.

## Security can't self-heal

Watch out for **prompt injection**: someone hiding instructions inside normal-looking text, hoping the AI will follow them. Security checks must never be "helpfully" worked around.

---

## Quick checklist before shipping any AI tool

Before releasing a new tool (an MCP tool or one inside the app), ask these 6 questions:

1. **Can the schema stop the mistake?** Use fixed value lists, clear formats, and real examples in the input descriptions.
2. **Is the mistake just a harmless formatting slip?** If there's no doubt what was meant, fix it automatically in code.
3. **When the input is wrong, does the error list the valid options and the next step?** Then the AI recovers in one step instead of two or more, or giving up.
4. **Could the error show data from another client, or data this user isn't allowed to see?** If so, remove it, and refuse by default.
5. **Does the tool change something in the real world** (publish, delete, send)? If so, never guess. Ask the user, or prepare it for human approval.
6. **Is there a limit on retries?** So a confused AI can't keep looping forever.

---

## The 4-step order every self-healing tool follows

Build every tool in exactly this order:

```text
1. SECURITY CHECK  ──► Check who the user is and which brand/workspace they can touch. FIRST.
                       If anything is wrong, refuse. NEVER self-heal past this step.
2. CLEAN UP        ──► Fix harmless, obvious slips (spaces, capital letters, empty text).
3. CHECK + GUIDE   ──► If the input is still wrong, send back a clear reply with:
                       (what went wrong) + (the valid options) + (how to retry).
4. NORMAL ANSWER   ──► Send back the requested data.
```

### Step 1: Fix the schema first

The old description was vague, so the AI guessed `"wing_hashtags"`:

```typescript
// ❌ BEFORE: vague description; invites the AI to guess "wing_hashtags"
section: z
  .string()
  .optional()
  .describe("Section id from index, or index/core. Omit for full rendered text, paged."),
```

The new description shows real examples and warns against the common mistake:

```typescript
// ✅ AFTER: tells the AI exactly what valid IDs look like
section: z
  .string()
  .optional()
  .describe(
    'Numeric section id from the index (for example "0", "1", "2"), or "index" / "core". ' +
    'Do not guess heading slugs like "wing_hashtags". Omit to read the full guidelines.',
  ),
```

> [!note] Why this matters
> The text inside Zod's `.describe(...)` is sent to the AI as part of the tool's description. One clear example (`"0", "1", "2"`) prevents about 80% of bad calls before the tool's code even runs.

### Step 2: Rewrite the handler

*(Not written yet.)*

### Step 3: Turn it into a reusable helper for all tools

*(Not written yet.)*

### Step 4: Test a self-healing tool without calling the AI

*(Not written yet.)*
