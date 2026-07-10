
```POSTGRESQL
create index concurrently g on grades(g);
```

This will allow reading and writing while creating the index , which doesn't stop the production. It just takes some much longer since it depends on multiple scans to the table and may fail due to duplicates writing for example.