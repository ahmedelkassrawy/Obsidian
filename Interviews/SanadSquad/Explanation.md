### 1. The CLI flags

There are two entry points, and they share most flags:

- `run_week.py` runs a whole plan (6 posts).
- `run_piece.py` runs a single post, for testing one idea quickly.

**Choosing what to make**

|Flag|Script|What it does|Example|
|---|---|---|---|
|`--plan`|week|Which plan file to use. Default inputs/plan.json.|`--plan inputs/plan.json`|
|`--set`|week|Overrides one slot’s topic. You can repeat it.|`--set thread_2="oracle manipulation"`|
|`--type`|piece|Which post type to make.|`--type tech-thread`|
|`--topic`|piece|The topic for that one post.|`--topic "reentrancy"`|

**Where things go**

|Flag|What it does|
|---|---|
|`--output`|The run folder. Default: `output/<UTC time>-<random 8 chars>`. If the folder already exists, the run refuses to start, so it never overwrites an old run.|
|`--root`|Where the project lives (the inputs, agents and post types). You almost never need this.|
|`--resume`|Continue an interrupted run from its folder: `--resume output/20261015T...`.|

**Models**

|Flag|What it does|
|---|---|
|`--default-model`|The model every agent uses unless its `agent.yaml` names its own.|
|`--model-override`|Forces _every_ agent onto one model, even ones with their own setting. Handy for a cheap test run.|
|`--reasoning-effort-override`|Forces thinking to `none` / `low` / `medium` / `high` for every agent.|

**Money and limits**

|Flag|What it does|
|---|---|
|`--token-budget`|The most tokens the whole run may use.|
|`--cost-budget`|The most dollars the whole run may spend.|
|`--allow-unpriced`|Lets you use a model that isn’t in any price list. The token cap still applies.|
|`--max-tweet-chars`|Can only _lower_ the 280 limit. Anything above 280 is rejected.|
|`--max-concurrency`|How many model calls can run at the same time (blank means no limit).|

**Behavior**

|Flag|What it does|
|---|---|
|`--estimate`|Prints the worst-case cost and **stops without spending anything**. This is called a “dry run”.|
|`--no-advisor`|Skips the end-of-run advisor.|

Two things to care about 
- **Where a setting comes from.** For any setting, the order is: CLI flag beats environment variable, which beats `.env`, which beats the built-in default. So `.env` says `RUN_TOKEN_BUDGET=250000`, but `--token-budget 400000` wins for that one run.
- **On `--resume`, almost everything is locked.** You can only add `--token-budget` / `--cost-budget`, and only to _raise_ them. Changing the model or plan halfway would mix two different runs into one.

---
Plan 
Its the startup work that happens before the langgraph graph begins , split betweent the `cli.py` and start of `run_pipeline()` in `pipeline.py`

```python
python run_week.py --set thread_2="oracle manipulation" --token-budget 300000
```

**A. Read the flags.** Python’s `argparse` turns that text into an object: `args.set = ["thread_2=oracle manipulation"]`, `args.token_budget = 300000`.

**B. Build the settings** (`Settings.load` in `config.py`). It starts from the defaults, layers `.env` on top, then environment variables, then your flags. **Pydantic** then checks every value. That check is where “max tweet chars must be at most 280” and “budget must be positive” actually live. A bad value stops the run here, before anything costs money.  
_Learn it as:_ “Pydantic validation”, “configuration precedence”, “12-factor app config”.

**C. Load the plan** (`load_plan`). This reads `plan.json`: 6 slots, where `thread_1` has focus `"reentrancy"` and the other five are empty. It checks that slot ids are unique and that each slot’s post-type folder exists.

**D. Apply `--set`** (`parse_sets`). It splits `thread_2=oracle manipulation` at the `=`, then sets `thread_2.focus = "oracle manipulation"` and clears any topic id. The slot name must exist and the topic can’t be blank. Remember from section 6.1: this is only a **topic**, not evidence. Research still has to find real sources for it.

**E. The preflight check** (`validate_inputs`). Before spending anything, it checks that every file the run will need exists and makes sense:

- Slot ids are unique, even ignoring upper and lower case. On Windows, `Thread_1` and `thread_1` would be the same filename.
- Names only use safe characters, and aren’t Windows-reserved words like `CON` or `NUL`. Names become file paths, so a name like `../../secrets` must never get through.
- The brand colors are real colors, and the knowledge base loads.
- Each post type’s rubric must include `unsupported_claim` as an automatic fail. The grounding rule is enforced at startup.
- Each agent’s `agent.yaml` and `system.md` exist, writers have no search skills, and each model name is in a valid format.

The idea is to **fail fast**: it’s much better to stop at second 1 with “missing file” than at minute 4, after paying for research.  
_Learn it as:_ “fail-fast”, “preflight checks”, “input validation”, “path traversal”.

**F. Estimate the worst case** (`estimate`). For every agent call the run _might_ make, it assumes the maximum (big input, maximum output, every retry) and prices it with `genai-prices`. It compares the total with your budget and warns if it’s over. With `--estimate`, it prints this and exits.  
One honest warning: as we saw in the code review, this estimate is currently **about 45 times too high** (11.2M tokens against 250k), so the warning fires on every run. It’s on the fix list.

**G. Create the run folder.** For example `output/20261015T091500-a1b2c3d4`: UTC time plus 8 random characters, so two runs never collide. If the folder exists, the run refuses.

**H. Lock the folder** (`RunLock`). It takes an operating-system file lock, so if you accidentally start the same resume twice, the second one is refused.  
_Learn it as:_ “file locking”, “mutual exclusion”.

**I. Take a snapshot** (`snapshot`). It copies **every input file this run uses** into `run_dir/snapshot/`: brand voice, knowledge base, post types, agent prompts and skills. It also saves the plan _with your `--set` already applied_, and the final settings. Why: if you edit `brand-voice.md` tomorrow and then resume today’s run, the resumed run still uses today’s rules. One run, one set of rules.  
_Learn it as:_ “reproducibility”, “immutable inputs”.

**J. Record the run’s identity** (`run_identity.json`). It holds:

- a random **thread id**, which is the name LangGraph files this run’s saved progress under;
- a **SHA-256 fingerprint** of every snapshot file. On resume, the fingerprints are recomputed. If anyone changed a snapshot file, resume refuses.

_Learn it as:_ “UUID”, “cryptographic hash / SHA-256”, “tamper detection”.

**K. Start the bookkeeping files.** These are `runtime-settings.json`, `external-usage.json` (search and image call counts) and an empty `usage.jsonl` (one line per model call, added later). They’re written with `atomic_json`: write to a temporary file, then rename it into place. A crash mid-write can never leave a half-written JSON file.  
_Learn it as:_ “atomic file write”, “write-then-rename”.

**L. Hand over to the graph.** Each of the 6 slots becomes a starting `SlotState`, and LangGraph begins at its first real node, `focused_research`. That’s where Plan ends.

### The short version

Plan = **read the flags, build the settings, load the plan, apply `--set`, check everything, estimate the cost, create the folder, lock it, snapshot it, fingerprint it, start the bookkeeping, hand over to the graph**. Not a single LLM call happens in the Plan step. That’s deliberate: it’s pure code, so it’s free, fast and predictable.

### Why a resumed run keeps the old rules

Your instinct makes sense. The key is that **resume doesn’t mean “run again”. It means “finish a run that stopped halfway.”**

Picture this. You start the week’s run on Monday. Three posts get written, checked against the rules, approved and saved. Then your API quota runs out and the run stops.

On Tuesday you edit `brand-voice.md` and ban the word “crucial”. Then you resume.

**If resume used the new rules:**

- `thread_1`, `thread_2` and `marketing_1` were approved on Monday. One of them says “crucial”, and it’s already approved and saved.
- The other three posts are checked against Tuesday’s rules.
- Your final `posts.csv` now mixes posts checked by two different rulebooks. One contains a banned word, and the run’s own records say it passed. Nobody reading the output can tell which rules applied to which post.

It’s like a teacher who changes the answer key after grading half the exams. Each grade looks fine on its own, but the class results mean nothing together.

**What you do when you’ve changed the rules:** start a **new run**. A new run snapshots the new rules and applies them to all 6 posts. Resume is only for **recovering from an accident**: quota ran out, laptop slept, network died. It’s not for editing.

There’s a technical reason too. Every saved step remembers a fingerprint of exactly what it was given (the `input_sha256` you’ll see in the code). If the rules changed underneath it, the saved steps would no longer match, and the code would refuse, or worse, quietly mix the two.

A different design could say “on resume, re-check the finished posts against the new rules”. That’s possible, but it’s more complicated, and it isn’t really resuming anymore. It’s a new run that reuses some old drafts.

### K. The bookkeeping files, in simple words

Think of the run as a trip, and these files as the trip’s notebooks:

|File|What it’s like|What goes in it|
|---|---|---|
|`runtime-settings.json`|The trip’s rules card|The settings this run is using right now: models, budgets. If you raise the budget on resume, the new number is written here.|
|`usage.jsonl`|A stack of receipts|**One line per AI call**: which step, which model, how many tokens, how much it cost. Starts empty. The summary adds these up at the end.|
|`external-usage.json`|A counter for everything that isn’t AI|How many web searches, page downloads and images. Not priced in dollars, just counted.|

**What “atomic write” means.** Writing a file isn’t instant. The computer writes it piece by piece. If the power cuts halfway, you can be left with a broken file like:

{"run_token_budget": 3000

Next time the program reads it, it crashes, because that’s not valid JSON.

Atomic write avoids this with a simple trick:

1. Write the whole new content to a **separate temporary file** (`ledger.json.tmp`).
2. When it’s completely finished, **swap** it into place with one rename.

A rename is a single step for the operating system: it either happened or it didn’t. So at any moment the real file is either the complete old version or the complete new version, never half of each. It’s like writing a letter on scratch paper and only swapping it in once you’re done, instead of erasing and rewriting the original in place.

---
Research 
First real station after Plan
First place an LLM is called

In the Langgraph its two Langgraph nodes in a row
`focus_research` then `topic selection`

Here’s our running example (`plan.json` plus `--set thread_2="oracle manipulation"`):

|Slot|Focus|Handled by|
|---|---|---|
|thread_1|“reentrancy”|node 1, focused research|
|thread_2|“oracle manipulation”|node 1, focused research|
|thread_3|empty|node 2, topic selection|
|marketing_1–3|empty|node 2, topic selection|

### Node 1: focused research
