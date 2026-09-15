---
description: "Hub: every note about SQL"
type: hub
domain: backend
tags:
  - type/hub
  - topic/sql
---
# SQL

> [!info] The eleven-part T-SQL course series plus a one-page summary. Missing: a clean rewrite of the unsectioned 'Database/SQL/SQL.md' dump.
> Part of [[MOC - Backend]]. Also try the tag `#topic/sql`.

## Concepts
- [[Best Practices for SQL Table Creation]] — Whether to run CREATE TABLE IF NOT EXISTS at application startup, and what to do instead in production (migrations).
- [[Why Avoid SQL OFFSET for Paging]] — Why OFFSET paging degrades and duplicates rows, demonstrated in PostgreSQL, plus keyset (seek) pagination as the replacement.

## How-tos & recipes
- [[03 - Core CRUD (insert, select, update, delete)]] — The four Core statement builders, why not f-strings, commit for writes, and bulk inserts.
- [[09 - Querying Data]] — Querying with 2.0 select() (and legacy query()): filters, ordering, paging, aggregates and relationship loading.
- [[PostgreSQL EXPLAIN ANALYZE Notes]] — Reading PostgreSQL EXPLAIN ANALYZE output across four example queries, and the performance lessons from each plan.

## References & cheat sheets
- [[SQL Summary in ONE PAGE]] — A single-page condensed T-SQL reference covering DDL, DML, DQL, wildcards, ordering, subqueries and SSMS tips.
- [[SQL]] `raw` — A long unsectioned dump of SQL fundamentals - statement categories, schemas, joins, constraints and related concepts - in one flat run of bullets.

## Book notes
- [[Optimizing Schema and Data Types]] — Book chapter on picking optimal MySQL data types, identifier choice, schema gotchas and the normalization/denormalization trade-off.
- [[SQLAlchemy CRUD And Relationships Recap]] — Closing recap of the API book's CRUD layer: SQLAlchemy read queries, pagination and filtering, eager loading, and many-to-many relationships with composite keys.

## Course notes
- [[SQL Constraints, Rules and Defaults]] — Course notes on SQL constraints, rules, defaults and custom data types, with the emp table as the running example.
- [[SQL Cursors, Identity, Snapshots and SQLCLR]] — Course notes on SQL cursors, identity columns, insert variants, database snapshots and SQLCLR.
- [[SQL Date Formatting, Self-Joins and CTEs]] — Course notes on date formatting with CONVERT, self-joins, and common table expressions including top-N-per-group.
- [[SQL Indexes, Tables, Merge and Views]] — Course notes on SQL index types and tuning tools, temporary/table-variable tables, MERGE statements and views.
- [[SQL Ranking Functions and Conditional Logic]] — Course notes on SQL ranking functions and adhoc queries with CASE/IIF conditional logic, date conversion and CASE-driven updates.
- [[SQL Stored Procedures, Triggers and XML]] — Course notes on stored procedures, triggers with their inserted/deleted tables, the OUTPUT clause and XML output.
- [[SQL Subqueries, DML and Built-in Functions]] — Course notes on SQL subqueries, the UNION family of operators, DML statements, built-in functions and adhoc queries.
- [[SQL TOP, Execution Order and DDL]] — Course notes on TOP, NEWID(), the logical query execution order, database objects and DDL operations.
- [[SQL Variables, Functions and Window Functions]] — Course notes on local and global variables, control of flow, batches and transactions, function types, window functions and dynamic SQL.
- [[SQL Joins, Self Joins and NULL Handling]] `raw` — Pasted T-SQL exercises on cross joins, self joins, NULL handling and multiple value replacement.
- [[SQL Self Join and Aggregate Adhoc Queries]] `raw` — A handful of pasted T-SQL queries: a supervisor self join, a HAVING aggregate, an EXISTS check, an UPDATE and an INSERT.

## Project notes
- [[Project Agent Arch]] — Architecture writeup for DataPilot AI, a LangGraph Text-to-SQL agent: the graph nodes from router through schema intelligence, memory, SQL generation, approval gate and retry loop.

## Interviews
- [[InstaBug Q&A]] — InstaBug follow-up questions on how many index lookups a given SQL query performs, reasoning through clustered vs secondary index seeks.

## Related hubs
[[Database Indexing]], [[SQLAlchemy]], [[Postgres]], [[Transactions & Concurrency Control]], [[Cursors & Pagination]], [[MySQL]]

## Notes to self (from the audit)
- [[SQL]]: 685 lines with zero headings. Needs splitting into sections before it is usable; overlaps the SQL/ folder notes.
- [[SQL Joins, Self Joins and NULL Handling]]: Query dump with almost no prose - add why each query is written that way.
- [[SQL Self Join and Aggregate Adhoc Queries]]: Query dump, no explanation; smallest note in the SQL series.
- [[InstaBug Q&A]]: Starts at Q8 - questions 1 to 7 are missing. Find the rest or say in the note that it is a fragment.
- [[Project Agent Arch]]: Content is GenAI agent engineering - likely belongs in the ai-eng domain rather than ml.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
