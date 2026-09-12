---
date: 2026-08-08
type: note
tags: [skills, agents, authoring]
description: How to author Agent Skills that trigger reliably and give the agent room to work — precise on goals, ambiguous on steps.
---
# Skill Creation Tips

Guidance for writing **Agent Skills** (the `SKILL.md` authoring layer), as distinct from the runtime that loads them. For the LangChain implementation of the skills pattern, see [[Langchain.Multi Agent - Skills]] and [[Langchain.Multi Agent - Skills Implementation]].

## The `name` + `description` are the trigger

Claude reads only the `name` and `description` when deciding whether to fire a skill, so they carry the whole triggering decision. Write the `description` as three moves:

- **First sentence — *when to read* it.** The retrieval signal: the situations, file types, or phrases that should pull this skill in.
- **Middle sentence — *when to use* it.** The narrower condition under which the skill actually applies once loaded.
- **Last sentence — *what it does*.** The capability itself.

> [!tip]
> The `name` and `description` are matched against the current task — treat them as the skill's search keywords, not a title.

## Be precise about the ends, ambiguous about the means

A good skill pins down *what* and leaves *how* open.

**Be precise about:**
- **The goal** — what needs to be done.
- **The constraints** — the boundaries and guardrails that prevent disaster.
- **The context it can't derive** — schema, IDs, or data that lives somewhere the agent can't see.

**Be deliberately ambiguous about:**
- **The steps** — let the agent sequence the work.
- **The failures** — let it recover its own way rather than scripting every branch.
- **The runtime specifics** — don't hard-code what changes per environment.

## Give the agent margin

- **Skills are a superset of code.** They can express intent and judgment that rigid code can't.
- **Don't over-specify.** Leave the agent room to develop its own approach.
- **Agents handle cases you can't foresee.** Hand over the tools and the goal, then let them find the path.
- Make the skill **less prescriptive**: supply the tools the agent needs plus the outcome you want, and let it work out the route.

## Guard against skill rot

- A skill that just **points at a URL of docs** rots the moment those docs go stale — the skill silently drifts out of date.
- **Before building the next skill, grill the docs.** Use the grill-docs skill and ask the agent directly what it *can* and *can't* do, so the skill is grounded in current, verified capability rather than assumed behavior.

## Related
- [[Langchain.Multi Agent - Skills]] — the skills pattern and progressive disclosure (concept)
- [[Langchain.Multi Agent - Skills Implementation]] — building your own skills/`load_skill` middleware (code)
