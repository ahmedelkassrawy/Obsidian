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

