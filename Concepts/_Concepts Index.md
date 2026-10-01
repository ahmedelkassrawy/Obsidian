---
description: "Entry point for the Concepts layer: one-idea notes in my own words, linked to each other with reasons, each ending in an interview answer."
type: meta
tags:
  - type/meta
---
# Concepts Index

This folder holds **one idea per note**, in my own words. The rest of the vault is source material (courses, books, clippings, how-tos). This folder is where I write down what I actually understood.

## Rules
1. **Title = a claim or question.** "Indexes speed up reads by slowing down writes", not "Indexes".
2. **Own words only.** If I can't explain it without copying, I haven't learned it yet.
3. **At least 2 links to other concepts, each with a reason.** The reason is where the understanding lives.
4. **List the sources.** Link the course or book notes it came from.
5. **End with a 30-second answer.** That's my interview answer and recall card.
6. New note: create it in `Concepts/`, then run "Templates: Insert template" and pick `Concept`.

## Where new concepts come from
- Finishing a lesson or chapter → write 1-3 concepts from it.
- A `#status/raw` note becomes `digested` once it has produced at least one concept here.
- Interview question I fumbled → write the concept I was missing.

## Review
Weekly: open a few notes, read only the title, say the 30-second answer out loud, then check. If it's shaky, rewrite the note.

## Concepts
### Backend & data
- [[Caching trades freshness for speed]]
- [[Indexes speed up reads by slowing down writes]]
- [[Replication scales reads, sharding scales writes]]
- [[Locks trade concurrency for correctness]]
- [[Async helps with waiting, not with computing]]

### AI engineering
- [[Prompt caching only pays off when the prefix stays identical]]
- [[The context window is a budget, not a bucket]]
- [[A RAG answer is only as good as its retrieval]]
- [[Embeddings turn meaning into distance]]
- [[Exact nearest-neighbour search doesn't scale, so vector databases approximate]]

### ML & deep learning
- [[Attention lets every token decide what to look at]]
- [[Regularization trades training fit for generalization]]

## Patterns I keep seeing
- **Most good answers are trade-offs.** Caching (speed vs freshness), indexes (reads vs writes), locks (correctness vs throughput), ANN (speed vs recall), regularization (training fit vs generalization). In an interview, naming the trade-off is half the answer.
- **Pay once up front so every later read is cheap.** Indexes, ANN indexes, caches and prompt caching all do this.

## All concepts (live list)
Search `tag:#type/zettel`, or open the Graph view filtered to `path:Concepts`.
