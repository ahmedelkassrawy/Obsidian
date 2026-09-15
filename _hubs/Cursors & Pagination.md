---
description: "Hub: every note about Cursors & Pagination"
type: hub
domain: backend
tags:
  - type/hub
  - topic/cursors-and-pagination
---
# Cursors & Pagination

> [!info] Server-side vs client-side cursors and why OFFSET paging fails. Missing: cursor pagination expressed in an actual API response format.
> Part of [[MOC - Backend]]. Also try the tag `#topic/cursors-and-pagination`.

## Concepts
- [[Why Avoid SQL OFFSET for Paging]] — Why OFFSET paging degrades and duplicates rows, demonstrated in PostgreSQL, plus keyset (seek) pagination as the replacement.

## Course notes
- [[Intro Cursors]] — Course notes on PostgreSQL cursors: fetching a huge result set incrementally, the SQL to do it, and the pros and cons.
- [[Server-Side vs. Client-Side]] — Course notes comparing server-side and client-side cursors in PostgreSQL from Python, with a one-million-row demo.

## Related hubs
[[Postgres]], [[SQL]]

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
