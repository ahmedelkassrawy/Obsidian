Component Classification
 •  Agents: Advisor, Reviewer, Writer
 •  Mixed: Research, Visual
 •  Code: Plan, Validator, Export, Summary
Plan Execution Flow
 •  CLI & Flags: Inspects CLI arguments and flags, parsed via argparse.
 •  Settings Validation: Uses the parsed values to build the configuration settings and validates them using pydantic.
 •  Load Plan: Loads plan.json (contains 6 slots).
 •  Preflight Checks: Runs a set of validation checks before the content plan starts. It confirms that inputs and settings are valid so the run fails early instead of failing midway through execution.
Preflight Validation & Setup Steps
 •  Validate Inputs:
   •  Ensure slots in plan.json are not empty.
   •  Verify the Brand configuration has 3 colors.
   •  Confirm kb.json loads properly.
   •  Agent Verification: For each agent, check that system.md, each skill.md, and .py files exist.
 •  Output Directory: Create the run output folder.
 •  Run Lock: Acquire a non-blocking OS lock so that two processes cannot own the same run simultaneously.
   > Why: A run writes many files. If two processes resumed the same run at once, both would spend tokens and money while overwriting each other's output.
   > 
 •  Cost/Token Estimation: Estimate worst-case numbers by passing the --estimate flag.

## The bookkeeping files

These files record the run's state rather than its content:

|File|Holds|
|---|---|
|`run_identity.json`|Thread ID, run ID, and a hash of every snapshot file; resume checks the snapshot against this|
|`runtime-settings.json`|Current settings, including budgets; resume compares against it so budgets can only go up|
|`external-usage.json`|Usage from outside the model calls (search, image backends), starting at zero|
|`usage.jsonl`|One line per model call, starting empty|

`ledger.json` and `state.json` are written the same way later in the run.

## What "atomic write" means

The helper is `atomic_json` in [durability.py](D:\me\content_pipeline\durability.py):

```
def atomic_json(path, value):
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")
    temp.replace(path)
```

1. It writes the full JSON to `run_identity.json.tmp`.
2. It renames the temp file over the real file with `Path.replace`, which calls `os.replace`.

On the same filesystem, that rename happens as a single step. Anyone reading `run_identity.json` sees either the complete old version or the complete new version, never a mix.

## Why it matters here

If the process were killed halfway through a plain `write_text`, the file would be cut off, for example `{"thread_id": "ab`. On the next resume, the read-only preflight would fail to parse `run_identity.json` or `ledger.json`, and the run could not be recovered, even though tokens and money had already been spent. With atomic writes, a crash leaves at worst a stray `.tmp` file, and the real file still holds its last good version.

The estimate is a deliberately pessimistic upper bound on tokens and dollars, worked out from the config alone. It makes no model calls and creates no clients. The code is `estimate()` at [pipeline.py · L178](D:\me\content_pipeline\pipeline.py:178), and the CLI wiring is in `content_pipeline/cli.py:107-125`.

## Step by step

**1. Validate first.** It runs the same `validate_inputs` preflight, so a broken config fails here too.

**2. List every agent the run will use** (`_estimate_agent_names`):

- one `research` for the batch topic-selection call;
- for each slot: `research`, that slot's writer, `reviewer`, `visual`;
- one `advisor`, if enabled.

**3. Count calls per agent** (`_estimated_agent_calls`):

|Agent|Base calls|
|---|---|
|research|5|
|writer, reviewer|`MAX_CONTENT_ATTEMPTS` = 2|
|visual, advisor|1|

**4. Reserve tokens for each agent** using three constants (`pipeline.py:64-66`):

```
output   = max_output_tokens × 1.5              # ESTIMATED_OUTPUT_MULTIPLIER
reserved = (16,000 + output) × calls × 8        # ESTIMATED_INPUT_TOKENS, ESTIMATED_CALL_ALLOWANCE
```

- **16,000** is a flat guess at input tokens per call. Prompts aren't actually measured.
- **× 1.5** pads the agent's `max_output_tokens` from its `agent.yaml`.
- **× 8** is a blanket allowance for search turns, parsing/truncation repairs and transient retries.

**5. Price each agent:**

- It finds the agent's model with `resolve_model`: `--model-override`, then the agent's `model:`, then `default_model`.
- `Prices.quote` prices one call of 16,000 input + `output` tokens. It uses [prices.yaml](D:\me\config\prices.yaml) if the model is listed there, otherwise the `genai-prices` library. `update=False` means it doesn't download fresh price data.
- That price is multiplied by `calls × 8`.
- If a model has no price, that agent adds an `unpriced_model:<agent>` warning and the total cost becomes `null`.

**6. Compare with the budgets:** if tokens exceed `run_token_budget` or cost exceeds `run_cost_budget_usd`, it adds `worst_case_exceeds_budget`.

## What happens next

- **With `--estimate`:** it prints the `Estimate` JSON to stdout and exits with code 0. No run folder is created and no model is called.
- **Without it:** it prints the same JSON to stderr as `startup_budget_warning: …` and the run continues. This happens on every run, not only when a budget is exceeded. The estimate never blocks a run; the real limits are enforced during the run by the `Ledger`.
- **When resuming:** the estimate is computed from the saved snapshot after the run lock is taken (`warn_resume`). With `--resume --estimate`, it's computed read-only and the run isn't started.

## Worked example with the current config

Research, reviewer, visual and advisor have `max_output_tokens: 3000`, so output is 4,500 and each call reserves 20,500 tokens. Writers have 6,000, so output is 9,000 and each call reserves 25,000.

|Agent|Calculation|Tokens|
|---|---|---|
|research|20,500 × 5 × 8|820,000|
|writer|25,000 × 2 × 8|400,000|
|reviewer|20,500 × 2 × 8|328,000|
|visual|20,500 × 1 × 8|164,000|
|advisor|20,500 × 1 × 8|164,000|

Per slot that's 1,712,000 tokens. With the 6 slots in [plan.json](D:\me\inputs\plan.json), plus the batch research call and the advisor:

**6 × 1,712,000 + 820,000 + 164,000 ≈ 11.26M tokens.**

The default `run_token_budget` is 250,000 ([config.py · L17](D:\me\content_pipeline\config.py:17)), so with default settings **`worst_case_exceeds_budget` will always appear**. That's expected: the estimate is a worst-case ceiling, not a forecast. Real runs usually use a small fraction of it.

## Caveats

- The 16k input figure and the ×8 allowance are fixed guesses. Actual prompt size, KB size and search results aren't measured.
- The ×8 already includes "two content attempts", but writer and reviewer are also counted at 2 calls. So those two agents are probably counted twice over.
- Prompt-cache discounts aren't included, so cost is overstated for models that use caching.

### Research
each slot is researched by looking first time at BM25 search and getting top 5
and then the 5 turns finish , search_kb or web search
runs each search max 4 and checks every cited sources was found with status ok 

Node 2 is we have to select a topic for an empty slots and get topics
llm is on batch call for getting the topics per slot and excluding taken topics and last 4 runs , assign_topics valudiates and fills any gap itself

Node 2 fills every slot that the plan left open. The model suggests a topic for each slot, then code checks those suggestions and has the final say. Once a slot has a topic, research for it is free, because the evidence comes straight from your own KB or brand file. Everything is in `D:\me\SanadSquad`, which is now on `main`.

**Which slots count as empty.** A slot is empty when it has no `focus` in `inputs/plan.json`. If a slot does have a focus, you chose its subject, so it skips this node and goes through full research (search plus LLM) later.

**1. LLM: one batch call** (`_propose_topics`, `pipeline.py:705`). This is a single call to the `research` agent with slot id `_batch`. That single call is why the cost estimate adds one extra research agent. The request contains two things:
- `choices`: for each empty slot, the list of ids that slot may use. That's every KB entry id, or the angle ids if the post type draws from angles (`topic_pool`, `post_types.py:154`).
- `exclude`: topics already taken this week by focused slots, plus every topic used in the last 4 runs. `history()` (`pipeline.py:271`) finds the 4 most recently modified run folders that have a `run_summary.json` and reads their `topic_id`s (`HISTORY_RUN_LIMIT = 4`).

The prompt in `agents/research/topics.md` tells the model to pick one id per slot from that slot's own list, skip excluded ids, give each slot a different topic, and never invent ids. If the call fails for any reason, the run continues. It logs `topic_selection_failed:code_fallback` and step 2 does all the picking.

**2. CODE: `assign_topics` checks and fills gaps** (`research.py:20`). The model's suggestions are only advice, and this function enforces the rules:
- It records the focused slots' topics first and warns `explicit_duplicate` if two of them collide.
- It keeps a suggestion only if it's in that slot's list, not used yet this week, and not in the last 4 runs. Otherwise it drops it silently.
- For any slot still without a topic, it takes the top id from a list ranked by keyword relevance (`kb.search` against the post type's hints) that is neither used nor recent.
- If everything left was used recently, it lets recent topics back in, oldest first, and warns `history_exhausted`. If nothing is left at all, that slot is marked `failed_research` with `topic_pool_exhausted` and the other slots continue.

For example, with KB ids A to F, where A and B were used last week and the model suggests B for slot 1 and D for slot 2: slot 1's B gets rejected and slot 1 gets the best-ranked free id (say C), while slot 2 keeps D.

**3. CODE: the shortcut** (`assigned_pack`, `post_types.py:199`, called first thing in `ResearchAgent.__call__`, `agents.py:151`). Every slot still goes through `research_slot`. But a slot whose topic came from step 2 (has a topic, no focus) gets its `ResearchPack` built directly:
- **KB topic:** the pack is that one KB entry, used as the source.
- **Angle topic:** the pack is the brand's approved stats (filtered by the angle's `stat_ids`) plus the angle's KB sources. A "pick-one" angle gets just one source, chosen by `_choose_angle_sources` so no other slot covers it this week.

So there are no web searches and no research-loop LLM turns. That's why the estimate's 5 research calls per slot are an overcount for these slots: they really cost 0.

One small mismatch: `topics.md` still says "the research step finds the evidence afterwards", which isn't true anymore for these slots because of the shortcut. It doesn't change any behavior, but it's out of date.

Why aliasses because BM25 matches words and not meaning so the alieases makes them reach better 

**Evidence card (SourceRecord):** `source_id` (`KB-18`, `STAT-01`, `WEB-3f9a…`), kind, title, url, `evidence_text` (max 12,000 chars), status `ok` or `fetch_failed`.

So node 1 is the focused research where we get the name of the topics inside the plan 
if the second node where the empty slots have no focus (empty topcics) so the llm has to choose one

topic selection is handling all the remaining slots without an expliciti focus through  a hybrid LLM and python pipeline
1. Proposal -> Invokes TopicsSeelctor via a signle batch request from TopicChoiceReuqest, the model then is given candidate topics from topic pool and instrcuted to avoid collisons with a focused topics or topics from the last 4 runs , if the llm call failes it logs that `topic_selection_failed:code_fallback` and proceeds.

2. Determinsitics Validation 
- Rejects proposals that collide with curr wek topics or appear int he 4 run history 
- Fill empty slots with the highest ranked free topic from the kb saearch tool
- If histoical entries must be recycled it pulls the oldest used topic and warns "history exhausted"
- if no topic remain the slot is marked with outcome `SlotOutcome.failed_research` and reason `topic_pool_exhausted`.

- **Angle Source Assignment (`_choose_angle_sources`)**: For post types utilizing marketing angles (`pick_one: true`), assigns candidate KB sources to ensure no two slots cover the same subject in the same week.

- **Execution**: Dispatches `research_slot` [pipeline.py · SanadSquad/content_pipeline](D:/me/SanadSquad/content_pipeline/pipeline.py) across all assigned empty slots and writes the snapshot to `plan.resolved.json`.