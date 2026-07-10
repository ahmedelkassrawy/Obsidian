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