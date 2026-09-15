---
description: "Hub: every note about MongoDB"
type: hub
domain: backend
tags:
  - type/hub
  - topic/mongodb
---
# MongoDB

> [!info] Architecture, internals, clustered collections and a FastAPI+Motor howto. Missing: the aggregation pipeline and index design.
> Part of [[MOC - Backend]]. Also try the tag `#topic/mongodb`.

## How-tos & recipes
- [[FastAPI - MongoDB]] — How to wire FastAPI to MongoDB with the async Motor driver: Docker container setup, ObjectId handling in Pydantic, models and CRUD endpoints.

## Course notes
- [[BASE Model vs ACID]] — Course notes on the BASE model used by NoSQL stores (basically available, soft state, eventually consistent) and how it contrasts with ACID.
- [[MongoDB Architecture]] — Course notes on MongoDB's architecture and storage engine evolution from MMAPv1 to WiredTiger and clustered collections.
- [[MongoDB Cluster Collection]] — Course notes on MongoDB 5.3+ clustered collections: storing documents inline with the clustered index, the benefits and the limits.
- [[MongoDB Internals]] — Course notes arguing all databases share a frontend/storage-engine split, applied to MongoDB's internals.

## Related hubs
[[Database Internals]], [[FastAPI]], [[Docker]], [[System Design]], [[Database Indexing]]

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
