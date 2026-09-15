---
description: "Pasted SQL and Docker commands for spinning up two PostgreSQL shards behind a hash-based URL table."
domain: backend
type: howto
status: raw
tags:
  - domain/backend
  - type/howto
  - status/raw
  - topic/database-replication-and-sharding
  - topic/postgres
  - topic/docker
aliases:
  - "sharding"
  - "pgshard"
hubs:
  - "[[Database Replication & Sharding]]"
  - "[[Postgres]]"
  - "[[Docker]]"
---
```sql
CREATE TABLE url_table (
    id SERIAL PRIMARY KEY,
    url TEXT,
    url_id CHAR(5)
);
```

```dockerfile
FROM postgres
COPY init.sql /docker-entrypoint-initdb.d
```

```terminal
docker build -t pgshard .

docker run --name pgshard1 -p 5432:5432 -d pgshard
docker run --name pgshard2 -p 5433:5432 -d pgshard
docker run --name pgshard3 -p 5434:5432 -d pgshard
```