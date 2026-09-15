---
description: "Hub: every note about Pydantic"
type: hub
domain: backend
tags:
  - type/hub
  - topic/pydantic
---
# Pydantic

> [!info] Models, validation, serialization and settings. Missing: custom validators and v1-to-v2 migration gotchas.
> Part of [[MOC - Backend]]. Also try the tag `#topic/pydantic`.

## Concepts
- [[01 - Overview and Project Layout]] — Maps which of the three libraries owns which job and traces one POST request end to end through the project layout.
- [[06 - Request vs Response Models Explained]] — Explains why request and response models are separate: filtering secrets out, transforming data and better auto-docs.
- [[API Validations & Transformations]] — Why you validate and transform every incoming payload at the controller layer, with the syntactic/semantic/type validation split and a pipeline example.
- [[Data Modeling]] — Why a class and why an enum: a type is the set of values a slot may hold, so pick types that make illegal states unrepresentable and validate once at the boundary.

## How-tos & recipes
- [[03 - Pydantic Schemas (Request and Response Models)]] — Defines the Pydantic request and response schemas that sit in front of the ORM models.
- [[Langchain.Structured Output]] `stale` — Chatbot and chain code for getting structured output out of LangChain, including parallel chains and text splitting.

## References & cheat sheets
- [[07 - Full Source Listing (copy-paste ready)]] — The complete working source for the integrated app in two file layouts, ready to copy.
- [[09 - Cheatsheet]] — One-screen condensed setup, schema and endpoint templates for the FastAPI + SQLAlchemy stack.
- [[Pydantic]] — Pydantic v2 in practice: when to use it and when not to, BaseModel basics, enums to close a value set, field_validator for one field vs model_validator across fields.
- [[FastAPI Users - Schemas]] `raw` — The read/create/update Pydantic schemas FastAPI Users expects, and how to add your own fields to them.
- [[Pydantic Settings]] `raw` — A pasted config.py snippet showing pydantic-settings BaseSettings reading values from a .env file.

## Book notes
- [[Ch2.Getting Started with FastAPI]] — Ch2 notes on FastAPI: first server setup, dependency injection, Pydantic v2 validation, auto docs, project structure and onion architecture.

## Course notes
- [[FastAPI - Pydantic]] — FastAPI course notes on Pydantic models: field validation and metadata, nested models, lists of submodels, special types and request-body examples.
- [[FastAPI - Response Models and Status Codes]] — FastAPI course notes on response models and return types, multiple models for different purposes, and choosing HTTP status codes.
- [[Pydantic]] — Study guide to Pydantic: defining models, nested models, validation and serialization, and settings management.

## Meta
- [[00 - Index]] — Index for the FastAPI + Pydantic + SQLAlchemy folder: reading order, look-up notes and a 'I want to find' table.

## Clippings (raw)
- [[AI Engineering Specific Use Cases]] `raw` — Verbatim copy of section 8 of the h9-tec/AI_deployment README on serving ML models and validating data pipelines with FastAPI.
- [[Clipping - Validation and Transformation Pipelines (YouTube)]] `raw` — Raw YouTube transcript on where validation and transformation belong in a backend request pipeline and what each layer should reject.

## Related hubs
[[FastAPI]], [[API Design]], [[SQLAlchemy]], [[Python Language]], [[LangChain]], [[Auth & Security]]

## Notes to self (from the audit)
- [[Langchain.Structured Output]]: Uses pre-1.0 imports (langchain.schema, langchain.text_splitter) - port to langchain_core before reusing.
- [[Pydantic Settings]]: Snippet only - no prose; worth expanding into a real settings note.
- [[AI Engineering Specific Use Cases]]: Copied README section - not rewritten.
- [[Clipping - Validation and Transformation Pipelines (YouTube)]]: Digest into API/FastAPI/Pydantic.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
