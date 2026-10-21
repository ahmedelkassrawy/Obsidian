---
tags: [interview, sanadsquad, langgraph, multi-agent, pipeline]
---

> [!abstract] What this note is
> A simple guide to the SanadSquad pipeline, written to help me explain it in the interview.
>
> It follows one run from start to end:
> **plan → research → write and review → image → collect**
>
> All code paths are inside `D:\me\SanadSquad`.
> The examples come from a real run saved in `output/sample-week`.

## 0. The big picture

The pipeline takes a weekly plan with **6 slots** and turns each slot into a finished post with an image.

Some parts are AI agents. Some parts are normal code. Some parts are both.

| Kind | Parts |
|---|---|
| **AI agent** (the model decides) | Writer, Reviewer, Advisor |
| **Mixed** (the model decides, code checks) | Research, Visual |
| **Code only** | Plan, Validator, Export, Summary |

```text
plan.json
   │
   ▼
PLAN PHASE (code only)
   │
   ▼
Node 1: focused_research
   │
   ▼
Node 2: topic_selection
   │
   ▼
6 lanes, one per slot, at the same time
   write → validate → review → visual → collect
   │
   ▼
export → advisor → summary
```

> [!tip] The main idea
> **The AI makes the choices. The code checks them.**
>
> Every AI answer has a fixed shape, and code checks it before it is used.
>
> - Research must point to real evidence.
> - Topic picks must come from the allowed list.
> - Image text must be copied from the post or the evidence.

---

## 1. Plan phase

No AI is used here. It is all normal code.

### 1.1 The steps

1. **Read the command.** `argparse` reads the flags you typed.

2. **Build the settings.** The flags become a `Settings` object. Pydantic checks it.

3. **Load the plan.** It reads `inputs/plan.json`, which has 6 slots.

4. **Preflight checks.** It checks that everything is valid **before** spending money. If something is wrong, the run stops early.

5. **Make the run folder.**

6. **Take the run lock.** (See 1.3)

7. **Take a snapshot.** It copies all inputs and instructions into `snapshot/`.

8. **Estimate the cost.** (See 1.5)

9. **Create the starting state.** Each slot gets an empty `SlotState`.

### 1.2 What preflight checks

The code is `validate_inputs` in `pipeline.py:121`.

**The plan**

- The plan is not empty.

- Slot ids are unique. `Thread_1` and `thread_1` count as the same.

**The brand and the knowledge base**

- The brand has **at least 3 colors**, and each one is a real color.

- `kb.json` loads without errors.

**Each slot**

- Its post type exists.

- If it uses angles, `angles.yaml` loads.

- Its rubric must fail any post with an `unsupported_claim`.

**Each agent** (writer, research, reviewer, visual, and advisor if it is on)

- `agents/<name>/system.md` exists.

- For each skill, both `skills/<skill>.md` and `skills/<skill>.py` exist.

### 1.3 The run lock

> [!definition] Run lock
> A lock on the file `run.lock`.
>
> Only **one** program can own a run at a time.
>
> If another program already has it, the second one stops right away. It does not wait.

> [!question] Is this like a lock in SQL?
> Same idea: only one owner at a time.
>
> But it is much simpler. It locks the whole run folder, not single rows. And it never waits.

**Why we need it**

A run writes many files.

If two programs worked on the same run at once, both would spend money, and they would overwrite each other's files.

### 1.4 Bookkeeping files and safe writes

These files save the **state** of the run, not the posts.

| File | What it saves |
|---|---|
| `run_identity.json` | The run's id and a fingerprint of every snapshot file. A resume uses it to check nothing changed. |
| `runtime-settings.json` | The settings, including budgets. On resume, budgets can only go up. |
| `external-usage.json` | Use of outside services (search, images). Starts at zero. |
| `usage.jsonl` | One line for each AI call. Starts empty. |

`ledger.json` and `state.json` are saved the same way later.

> [!definition] Atomic write (safe write)
> A way of saving a file so it is **never half-written**.
>
> Anyone who reads it sees either the full old version or the full new version.

How it works (`atomic_json` in `durability.py`):

```python
# durability.py
def atomic_json(path, value):
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")
    temp.replace(path)
```

1. Write everything into a temporary file first, for example `run_identity.json.tmp`.

2. Then swap the temporary file into the real file's place. The swap happens in one single step.

> [!warning] Why this matters
> Imagine the program crashes while writing a file the normal way.
>
> The file would be cut in half, like `{"thread_id": "ab`.
>
> Next time, the run could not read it and could not continue, even though money was already spent.
>
> With a safe write, the worst case is a leftover `.tmp` file. The real file is still fine.

### 1.5 The cost estimate

> [!definition] Estimate
> A guess at the **highest possible** cost of the run, in tokens and dollars.
>
> It only reads the settings. It does not call any AI.
>
> Code: `estimate()` in `pipeline.py:178`.

**How it is calculated**

**Step 1 — Check the inputs.** It runs the same preflight checks first.

**Step 2 — List the agents the run will use.**

- 1 research call to pick topics for the week.

- For each slot: research, writer, reviewer, visual.

- 1 advisor, if it is on.

**Step 3 — Count the calls for each agent.**

| Agent | Calls |
|---|---|
| research | 5 |
| writer | 2 |
| reviewer | 2 |
| visual | 1 |
| advisor | 1 |

**Step 4 — Reserve tokens.**

```text
output   = max_output_tokens × 1.5
reserved = (16,000 + output) × calls × 8
```

- **16,000** is a fixed guess at how big each input is. Real prompts are not measured.

- **× 1.5** adds extra room to the output limit from `agent.yaml`.

- **× 8** adds room for searches, fixes and retries.

**Step 5 — Turn tokens into dollars.**

- Prices come from `config/prices.yaml` or the `genai-prices` library.

- If a model has no price, it adds a warning, and the total cost becomes `null`.

**Step 6 — Compare with the budget.**

- If the worst case is over budget, it adds the warning `worst_case_exceeds_budget`.

**What happens after**

- **With `--estimate`:** it prints the result and stops. Nothing runs.

- **Without it:** it prints a warning and keeps going. The estimate **never** stops a run.

- **Real limits** are checked during the run by the `Ledger`.

**Example with the current settings**

| Agent | Math | Tokens |
|---|---|---|
| research | 20,500 × 5 × 8 | 820,000 |
| writer | 25,000 × 2 × 8 | 400,000 |
| reviewer | 20,500 × 2 × 8 | 328,000 |
| visual | 20,500 × 1 × 8 | 164,000 |
| advisor | 20,500 × 1 × 8 | 164,000 |

- One slot = **1,712,000** tokens.

- Whole run (6 slots + topic call + advisor) ≈ **11.26 million** tokens.

- The default budget is only **250,000**, so the warning **always** shows.

- That is fine. It is a ceiling, not a real prediction.

> [!warning] Weak spots in the estimate
> - The 16,000 and the × 8 are fixed guesses.
>
> - Writer and reviewer are probably counted twice: the × 8 already covers a second try.
>
> - Cache discounts are ignored, so the cost looks higher than it is.
>
> - Most slots really need **0** research calls (see 2.5), not 5.

---

## 2. Research phase

### 2.1 The data that moves between steps

> [!definition] Contract
> A fixed data shape (a Pydantic model) that one step hands to the next.
>
> Agents never share a chat. They only pass these objects.

| Contract | In simple words |
|---|---|
| `ResolvedSlot` | One line of the plan: id, type, focus, topic |
| `SlotState` | Everything we know about one slot as it moves through the pipeline |
| `ResearchRequest` | The slot + some hints about the post type |
| `ResearchTurn` | The request + the evidence found so far + searches left |
| `ResearchAction` | The AI's answer: search the KB, search the web, or finish |
| `ResearchPack` | The final evidence for one slot |
| `SourceRecord` | One piece of evidence (see below) |

```python
# models.py:48
class ResolvedSlot(Contract):
    slot_id: str
    type: str
    focus: str | None = None
    topic_id: str | None = None        # filled during research
    angle_source: str | None = None    # only for pick-one angles
```

> [!definition] Evidence card (`SourceRecord`)
> One piece of evidence.
>
> - **id:** starts with `KB-`, `STAT-` or `WEB-`
> - **kind:** `kb`, `stat` or `web`
> - **title, url, text:** web text is cut at 12,000 characters
> - **status:** `ok`, `snippet_only` or `fetch_failed`
>
> Only `ok` evidence can be used in a post.

A `ResearchPack` is only valid if:

- no evidence id appears twice, and

- at least one piece of evidence is `ok`.

### 2.2 Two kinds of slots

| Slot | Has a focus? | Who picks the topic | Cost |
|---|---|---|---|
| **Focused** | Yes, you wrote it in the plan | The research loop | KB search + AI turns (+ web if needed) |
| **Empty** | No | Node 2 picks from a list | **Free** — no search, no AI |

### 2.3 Node 1: focused research

Only **focused** slots run here. They all run at the same time.

**Step 1 — First search (code, no AI)**

It searches the KB using the focus words.

The search (BM25) matches **words**. It always returns the top 5, even if some are not relevant.

**Step 2 — The loop (AI)**

- Up to **5 turns**.

- Up to **4 searches** in total.

- Each turn, the AI answers with one of:
  - `search_kb` — search the KB again
  - `web_search` — search the web
  - `finish` — "I'm done, use these sources"

**Step 3 — Code checks the answer**

- Every source the AI picked must really exist and be `ok`. The AI can't invent a source.

- The topic must be one of those sources.

- The topic's title must really match the focus (`focus_matches`). The AI can't switch to a similar topic.

**Step 4 — Keep only what was picked**

- The pack only has the sources the AI chose.

- The others are still saved in `research_log.json`, so you can see them.

> [!note] The AI does not see everything
> The full `SlotState` is **not** sent to the AI.
>
> Code builds a small `ResearchRequest` (slot + hints), then wraps it in a `ResearchTurn` with the evidence.

**Example: `thread_1`, focus "reentrancy"**

The first search returned 5 entries:

```text
KB-01  Reentrancy
KB-20  Business logic errors
KB-02  Integer overflow and underflow
KB-03  Unchecked call return value
KB-04  Unprotected Ether withdrawal
```

Only KB-01 is really about reentrancy.

The AI got two messages:

- **system:** the research prompt + `loop.md`
- **user:** the `ResearchTurn` as JSON

`loop.md` says: *"a matching word is not enough — the text must explain the focus."*

The AI answered:

```json
{"action": "finish", "source_ids": ["KB-01"], "topic_id": "KB-01"}
```

- **Who picked 1 out of 5?** The AI. Code only checked it.

- **Cost:** 1 KB search + 1 AI turn.

> [!question] Why do KB entries have aliases?
> The search matches **words**, not meaning.
>
> Aliases are other names for the same bug. They help the search find the right entry, and they help `focus_matches` check the topic.

### 2.4 Node 2: topic selection

This node gives a topic to every **empty** slot.

```text
1. AI    one call suggests a topic for each empty slot
2. CODE  assign_topics checks the suggestions and fills any gaps
3. CODE  picks a source for "pick-one" angles
4. CODE  builds the evidence pack for free (the shortcut)
5.       saves plan.resolved.json and sends each slot to its lane
```

**Step 1 — One AI call for all slots**

It sends:

- `choices` — the allowed topics for each slot. That's 20 KB ids for tech threads, or 3 angles for marketing posts.

- `exclude` — topics already used this week, and topics from the last 4 runs.

If this call fails, the run goes on and code picks everything.

**Step 2 — Code has the final say** (`assign_topics`)

- It keeps a suggestion **only if** the topic is allowed, not used this week, and not used in the last 4 runs.

- Bad suggestions are thrown away quietly.

- Empty gaps get the best free topic from a ranked list.

- If every topic was used recently, it reuses the oldest one and warns `history_exhausted`.

- If there is nothing left at all, only that slot fails. The others continue.

> [!example] Small example
> KB has topics A to F. A and B were used last week.
>
> The AI suggests **B** for slot 1 and **D** for slot 2.
>
> - B is rejected → slot 1 gets the best free topic, maybe **C**.
> - D is fine → slot 2 keeps **D**.

> [!definition] History
> The topics used in the **last 4 runs**, read from the 4 newest run folders.

**Step 3 — Pick-one angles**

Some marketing angles (like `ANGLE-education`) use one KB entry per week.

Code picks the first one that no other slot is using.

### 2.5 The shortcut (assigned pack)

> [!definition] Assigned pack
> If a slot has a topic but **no** focus, code builds its evidence pack directly from your files.
>
> No search. No AI.
>
> Code: `assigned_pack` in `post_types.py:199`.

| Topic type | What goes in the pack |
|---|---|
| **KB topic** | That one KB entry (description + root cause) |
| **Angle** | The brand's approved stats for that angle |
| **Pick-one angle** | The chosen KB entry + its stats |

> [!tip] Why this is good
> Most slots never search at all.
>
> Only slots with a focus do real research.
>
> Slots you didn't plan stay inside safe, checked material: your KB and your brand stats.

### 2.6 The real run (`output/sample-week`)

| Slot | Node | Topic | Evidence | Cost |
|---|---|---|---|---|
| thread_1 | 1 | KB-01 | KB-01 | 1 search + 1 AI turn |
| thread_2 | 1 | KB-18 | KB-18 | 1 search + 1 AI turn |
| thread_3 | 2 | KB-07 | KB-07 | free |
| marketing_1 | 2 | ANGLE-service | STAT-04, STAT-05 | free |
| marketing_2 | 2 | ANGLE-credibility | STAT-01, STAT-05 | free |
| marketing_3 | 2 | ANGLE-education | KB-04 | free |

- **AI calls in research:** only **3** (2 loop turns + 1 topic call). The estimate planned for 31.

- **Cost:** about 10,400 tokens, or $0.022.

- **Warnings:** `history_exhausted` × 3. There are only 3 angles, and all were used in the last 4 runs.

- **Why KB-04 for marketing_3?** Its first choice, KB-01, was already taken by thread_1.

---

## 3. The lane: write → check → review → image → collect

After node 2, each slot goes into its own **lane**. All 6 lanes run at the same time.

```text
Already failed? ───────────────────────────► collect
write → validate → review → visual ────────► collect
           │          │
           │          └ rejected → retry → write again (or give up → collect)
           └ broke a rule → retry → write again
```

### 3.1 Visual (making the image)

**Step 1 — Gather what's needed:** the approved post, the evidence, the post type, and the severity from the KB.

**Step 2 — Reuse it** if this image was already made in an earlier try (resume).

**Step 3 — The AI writes a plan for the image**, not the image itself.

The plan has: idea, scene, colors, the text on the image, alt text and severity.

**Step 4 — Code checks the plan**

- The text on the image must be **copied word for word** from the post or the evidence.

- It can't contain new numbers.

- The colors must be the brand colors.

**Step 5 — One fix.** If the check fails, the AI gets one more try with the errors.

If it still fails, code makes a simple card using the topic name or a title.

**Step 6 — Draw the image**

1. First try Cloudflare Flux (an AI background), with the text drawn on top.

2. If that fails → a simple local card (Pillow).

3. If that fails too → save just the plan as a JSON file.

**Step 7 — Mark the slot as shipped** and save the record in `visuals.json`.

> [!example] In the sample run
> - 6 image plans, no fixes needed.
> - Every Flux call was blocked (HTTP 429, too many requests). So all 6 images are simple local cards.
> - marketing_1's image text, *"its severity, its root cause and a recommended fix"*, is copied exactly from STAT-04.

### 3.2 Collect (the end of every lane)

Every lane ends here, whether the slot shipped or failed.

- If the slot has no final result, it raises an error. A slot can't leave unfinished.

- If the slot shipped, it saves a `FinalPiece` to `final.json`.

- It sends the slot back so the week can join all 6 lanes together.

> [!warning] Things to watch
> - A slot can ship **without a real image** (the JSON fallback).
>
> - Marketing posts never get a severity badge.
>
> - Flux failures don't show in `run.log`. Look in `visuals.json` or `external-usage.json`.

---

## 4. How the agents work

### 4.1 Agents don't talk to each other

> [!important] Key point
> Each agent is **one AI call**: a fixed shape goes in, a fixed shape comes out.
>
> There is no shared chat. LangGraph passes the slot from step to step, and code checks each handoff.

| Agent | Job | Model |
|---|---|---|
| research | Find evidence, pick topics | Sonnet 5.5 |
| thread_writer / marketing_writer | Write the post | Sonnet 5.5 |
| reviewer | Score the post | **Opus 5.5** |
| visual | Plan the image | Sonnet 5.5 |
| advisor | Suggest better instructions | Sonnet 5.5 |

### 4.2 How an agent is built

Each agent is a folder with two files:

- `system.md` — the agent's instructions
- `agent.yaml` — its settings

```yaml
# agents/thread_writer/agent.yaml
model: anthropic:claude-sonnet-5-5   # which AI model
max_output_tokens: 6000              # max answer length
reasoning_effort: low                # how hard it thinks
skills: [brand_rules]                # extra instructions added to the prompt
```

The full prompt is built in this order:

1. The agent's `system.md`
2. The post type's writing guide or rubric
3. Each skill's `.md` file
4. The brand voice file

> [!definition] Skill
> Just a markdown file added to the prompt.
>
> Only research's two skills (search KB, search web) are real tools, and **code** runs them, not the AI.

### 4.3 How an agent is called

Every agent uses the same function, `Agent.invoke`:

```python
messages = [
    {"role": "system", "content": self.prompt + instructions},
    {"role": "user", "content": payload.model_dump_json()},
]
return await self.client.call(schema, messages, slot_id, node, attempt, max_output_tokens)
```

- **System message** = the agent's prompt.

- **User message** = the request as JSON.

- **The answer** must match a fixed shape (`schema`).

### 4.4 The tools we use

| Tool | What it does for us |
|---|---|
| **LangChain** | Talks to any AI provider. Forces the answer into our shape. |
| **ModelClient** (our code) | Checks the budget **before** each call. Retries on errors. Gives more room if the answer was cut off. Asks again if the JSON was broken. Logs every call. |
| **LangGraph** | Runs the steps in order, runs the 6 lanes at once, and saves progress so a run can resume. |
| **Pydantic** | Defines every data shape between steps. |

> [!note] The AI asks, code does
> Research never runs a search itself.
>
> It answers "I want to search the web for X". Code runs the search, counts it, logs it, and gives the result back on the next turn.

### 4.5 Why YAML files for agents

- **Easy to change.** Switching a model is a one-line edit, with no code change. That's how the reviewer uses Opus and the rest use Sonnet.

- **Checked when loaded.** A typo fails right away. Writers are **not allowed** to have search skills.

- **Same every time.** The files are copied into the snapshot, so a resumed run uses the exact same settings.

- **Cheap estimates.** The cost estimate reads them without calling any AI.

---

## 5. Design questions for the interview

### Q1. What if the AI suggests a brand new topic?

**It can't get through.** There are 3 safety layers:

1. The AI is only shown allowed topic ids, and told not to invent any.

2. Its answer can only be an id, not a description.

3. Code keeps an answer **only if** it is in the allowed list.

**New topics come from `focus`.** A focused slot can search the web and use a new source.

This is on purpose:

- Slots you didn't plan stay safe.
- Slots you did plan can go wider.

**Downside:** less variety (only 20 KB topics + 3 angles).

### Q2. Why let an AI choose from a list? Why not pick randomly?

> [!warning] The weak spot I found
> The topic AI only sees **ids** like `KB-07`, with no titles or descriptions.
>
> So it is choosing blind. The code backup actually knows more: it ranks topics by how well they match.
>
> Used topics are already blocked twice, so random picking would only change the **order**.

| Option | Idea | Good | Bad |
|---|---|---|---|
| **1. Code only** | Remove the AI call. Code picks. | One less call. Same result every time. | Removes a feature. |
| **2. Smarter AI** ✅ | Show the AI titles and summaries | It can make real choices, like avoiding overlap | A bit more code and tokens |
| **3. Random** | Pick any free topic | Very simple | Ignores how good the topic is |

### Q3. Isn't option 2 more complicated?

Not really.

- Only 4 files change.
- Code still makes the final decision, so a bad pick is still caught.

### Decision: option 2, plus these improvements

1. **Only show allowed topics** to the AI.

2. **Show titles and summaries**, plus this week's topics that are already taken.

3. **Log rejected picks** so we can see them.

4. **Add a one-line reason** for each pick.

5. **Fix the old line in `topics.md`.**

6. **Write it up** in `ARCHITECTURE.md` with the other options I considered.

> [!tip] Why this is good for the interview
> An AI choosing from ids it can't read looks pointless.
>
> Option 2 fixes that, and it matches the rest of the design: **the AI chooses, code checks**.
>
> Writing down the other options shows I thought it through.

**Known limit (written down, not fixed yet)**

- If the run crashes in node 2 and resumes, the topic AI is called again.

- If it gives a different answer, that slot **fails** instead of quietly swapping topics.

- Later fix: save the AI's answer and reuse it.

> [!note] Status
> The work was given to a separate thread.
>
> Sonnet 5.5 writes the code, and Opus 5.5 reviews it.
>
> Branch: `feat/topic-selection-catalog`. It opens a PR and waits for my approval before merging.

---

## 6. Things that can surprise you

- **The AI's topic suggestions are never saved.** Only the final choice is.

- **`exclude` is only a hint** to the AI. Code enforces its own rules.

- **History reads every folder in `output/`**, including example folders. A fresh copy of the repo may show warnings it didn't cause.

- **Topic AI failures all look the same.** Budget, login and format errors all become one `code_fallback` warning.

- **Only 3 marketing angles**, so `history_exhausted` shows up almost every time.

- **If an angle had no stat list**, it would get all 5 stats, but only 2 are allowed. Nothing stops this early.

- **A missing id** gives a confusing error message.

---

## 7. Where things live

| What | File |
|---|---|
| The main flow, nodes, preflight, estimate | `content_pipeline/pipeline.py` |
| Topic checking | `content_pipeline/research.py` |
| Agents and the research loop | `content_pipeline/agents.py` |
| Topic lists, shortcut packs | `content_pipeline/post_types.py` |
| AI calls and retries | `content_pipeline/model_client.py` |
| Agent settings, prompt building | `content_pipeline/config.py` |
| Data shapes | `content_pipeline/contracts.py`, `content_pipeline/models.py` |
| Safe writes, run lock | `content_pipeline/durability.py` |
| Resume | `content_pipeline/stage_replay.py` |
| Images | `content_pipeline/images.py`, `content_pipeline/image_backends.py` |
| Agent prompts and settings | `agents/<name>/` |
| Post types | `post_types/<type>/` |
| Example run | `output/sample-week/` |
