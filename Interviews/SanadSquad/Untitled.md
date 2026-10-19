Step 1: Plan
1. Read flags with `argparse`
2. Build settings: default < `.env` < env var < flag, checked by Pydantic
3. Load `plan.json` (6 slots) and apply `--set`
4. Preflight 
What is the preflight 
- set of checks that runs before a content plan starts
- It confirms the inputs and settings are valid
- so the run fails early and for free instead of partway through 
