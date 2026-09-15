---
description: "Short note on CREATE INDEX CONCURRENTLY: it keeps reads and writes running but is slower and can fail."
domain: backend
type: howto
status: stub
tags:
  - domain/backend
  - type/howto
  - status/stub
  - topic/database-indexing
  - topic/postgres
aliases:
  - "CREATE INDEX CONCURRENTLY"
hubs:
  - "[[Database Indexing]]"
  - "[[Postgres]]"
---

```POSTGRESQL
create index concurrently g on grades(g);
```

This will allow reading and writing while creating the index , which doesn't stop the production. It just takes some much longer since it depends on multiple scans to the table and may fail due to duplicates writing for example.