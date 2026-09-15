---
description: "A handful of Redis environment variables for persistence, memory limit, eviction policy and protected mode."
domain: ai-eng
type: reference
status: empty
tags:
  - domain/ai-eng
  - type/reference
  - status/empty
  - topic/redis
aliases:
  - "Redis"
hubs:
  - "[[Redis]]"
---
```c
REDIS_PASSWORD=minirag_redis

#Persistence
REDIS_APPENDONLY=yes

#Memory Management
REDIS_MAXMEMORY=512mb
REDIS_MAXMEMORY_POLICY=allkeys-lru
 
#Security
REDIS_PROTECTED_MODE=yes
```