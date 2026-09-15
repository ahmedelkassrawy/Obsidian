---
description: "Hub: every note about Database Indexing"
type: hub
domain: backend
tags:
  - type/hub
  - topic/database-indexing
---
# Database Indexing

> [!info] Well covered: scan types, index-only scans, covering and composite indexes, EXPLAIN ANALYZE, bloom filters. Missing: index maintenance and bloat.
> Part of [[MOC - Backend]]. Also try the tag `#topic/database-indexing`.

## Concepts
- [[Bloom Filters]] — What a Bloom filter is, how the bit array and hash functions work, why false positives happen and where to use one.
- [[Full Text Search using Elasticsearch for Blazingly Fast Search]] — Why LIKE queries stop scaling and how an inverted index plus Elasticsearch relevance scoring solves search at size.

## How-tos & recipes
- [[PostgreSQL EXPLAIN ANALYZE Notes]] — Reading PostgreSQL EXPLAIN ANALYZE output across four example queries, and the performance lessons from each plan.
- [[Indexes Concurrently]] `stub` — Short note on CREATE INDEX CONCURRENTLY: it keeps reads and writes running but is slower and can fail.

## References & cheat sheets
- [[SQL]] `raw` — A long unsectioned dump of SQL fundamentals - statement categories, schemas, joins, constraints and related concepts - in one flat run of bullets.

## Book notes
- [[Creating the Database Layer]] — Book chapter building the data layer: the three layers, the models file with Player/Performance/League/Team relationships, and the database config.
- [[SQLAlchemy CRUD And Relationships Recap]] — Closing recap of the API book's CRUD layer: SQLAlchemy read queries, pagination and filtering, eager loading, and many-to-many relationships with composite keys.

## Course notes
- [[Index Scan vs Index Only Scan]] — Course notes on PostgreSQL index scan vs index-only scan, covering indexes with INCLUDE, and leftmost-column rules for composite indexes.
- [[Key vs Non-Key Column Indexes]] — Course notes distinguishing key-column indexes (constraints, uniqueness) from non-key INCLUDE columns, with the trade-offs.
- [[MongoDB Cluster Collection]] — Course notes on MongoDB 5.3+ clustered collections: storing documents inline with the clustered index, the benefits and the limits.
- [[Multiple Indexes]] — When the planner uses both indexes, only one, or none, and how to force an index choice.
- [[PostgreSQL Scan Types Comparison]] — Compares sequential, index and bitmap index scans in PostgreSQL, when the planner picks each, and a worked plan walkthrough.
- [[SQL Indexes, Tables, Merge and Views]] — Course notes on SQL index types and tuning tools, temporary/table-variable tables, MERGE statements and views.

## Project notes
- [[RAG POC Notes]] — How a proof-of-concept retriever evolved into a 3-stage production pipeline: hybrid vector plus BM25 candidates, FlashRank cross-encoder reranking, and score-aware returns.

## Interviews
- [[InstaBug Q&A]] — InstaBug follow-up questions on how many index lookups a given SQL query performs, reasoning through clustered vs secondary index seeks.

## Related hubs
[[SQL]], [[Postgres]], [[SQLAlchemy]], [[Database Internals]], [[RAG]], [[Vector Search]]

## Notes to self (from the audit)
- [[Indexes Concurrently]]: Stub - add the failure/cleanup procedure for an invalid index.
- [[SQL]]: 685 lines with zero headings. Needs splitting into sections before it is usable; overlaps the SQL/ folder notes.
- [[InstaBug Q&A]]: Starts at Q8 - questions 1 to 7 are missing. Find the rest or say in the note that it is a fragment.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
